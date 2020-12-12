import pdfplumber
import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import os
import argparse


def pdf():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'pdf', help="PDF file from which word cloud will be generated")
    parser.add_argument(
        '-m', '--mask', help="PNG file to use as shape of word cloud")
    parser.add_argument(
        '-r', '--remove', action='append', help="Words to remove from wordcould. Accepts multiple arguments (one per flag)")
    parser.add_argument(
        '-s', '--save', action='store_true', help="Save plot as PDF to current directory")
    parser.add_argument(
        '-st', '--saveto', help="Save plot to given directory")

    args = parser.parse_args()

    def get_add_stopwords(txt_file):
        file = open(txt_file, 'r')
        add_stopwords = []
        for line in file:
            word = line[:-1]
            if word not in add_stopwords:
                add_stopwords.append(word)
        return add_stopwords

    stopwords_file = os.path.join(os.path.dirname(
        __file__), 'data', 'stopwords.txt')
    add_stopwords = get_add_stopwords(stopwords_file)

    if args.remove:
        extra_stopwords = args.remove
    else:
        extra_stopwords = []

    def word_freq(pdf_filename):
        """Reads PDF file, extracts words and returns Pandas DF of Words and Frequency."""
        pdf = pdfplumber.open(pdf_filename)
        page_num = pdf.pages

        punctuations = r"""!()-[]{};:'"",<>./?@#$%^&*_~"""
        quote_mark = """\""""
        stop_words = stopwords.words('english')
        cust_stopwords = stop_words + add_stopwords + extra_stopwords

        words = []
        for page in range(len(page_num)):
            word_data = pdf.pages[page].extract_words(x_tolerance=1)
            for word in word_data:
                w = word['text'].lower()
                for charact in w:
                    if charact in punctuations:
                        w = w.replace(charact, "")
                w = ''.join(
                    [charact for charact in w if not charact.isdigit()])
                if quote_mark in w:
                    w = w.replace(quote_mark, "")
                if len(w) == 1:
                    continue
                if w not in cust_stopwords:
                    words.append(w)

        freq_dist = nltk.FreqDist(words)
        df = pd.DataFrame(freq_dist.most_common(),
                          columns=['Word', 'Count'])

        total_words = df['Count'].sum(axis=0)
        df['Frequency'] = df['Count'] / total_words
        df['Percent'] = df['Frequency'] * 100

        return df

    df = word_freq(args.pdf)
    dct = dict(zip(df.Word, df.Frequency))

    def transform_format(val):
        if val == 0:
            return 255
        else:
            return val

    if args.mask:
        mask_file = args.mask
    else:
        mask_file = os.path.join(os.path.dirname(__file__), 'data', 'mask.png')

    mask_raw = np.array(Image.open(mask_file))
    mask = np.ndarray((mask_raw.shape[0], mask_raw.shape[1]), np.int32)
    for i in range(len(mask)):
        mask[i] = list(map(transform_format, mask[i]))

    wordcloud = WordCloud(
        max_words=1000,
        colormap='Greens',
        mask=mask,
        min_font_size=8,
        stopwords=stopwords,
    ).generate_from_frequencies(dct)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), dpi=500)
    plt.imshow(wordcloud, interpolation='spline36')
    plt.axis("off")
    plt.tight_layout(pad=0)

    figname = 'pdf_to_wordcloud.pdf'
    if args.save:
        plt.savefig(figname)
    elif args.saveto:
        plt.savefig(os.path.join(args.saveto, figname))
    else:
        plt.show()
