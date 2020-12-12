# pdf_to_wordcloud

Generates a word cloud from a given PDF

## Installation

```zsh
$ pip install pdf_to_wordcloud
```

## Arguments

**Positional:** \
PDF: Name of PDF file from which to geneate the wordcloud

**Optional:** \
--remove (-r): Removes word from wordcloud. Accepts multiple arguments (one per flag) \
--save (-s): Saves wordcloud as PDF to current directory (no additional argument needed) \
--saveto (-st): Saves wordcloud to specified directory \
--mask (-m): PNG file to use as shape of wordcloud \

## Usage

Display wordcloud of file.pdf:
```zsh
$ pdf file.pdf
```

Save image of wordcloud as PDF:
```zsh
$ pdf file.pdf -s
```

Remove "this" and "that" from wordcloud and save:
```zsh
$ pdf file.pdf -r this -r that -s
```



