import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdf_to_wordcloud",
    version="0.0.2",
    author="Matt Rybin",
    author_email="mxr2011@miami.edu",
    description="Generates a word cloud from a given PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rybinmj/pdf_to_wordcloud",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'pdf_to_wordcloud': ['data/stopwords.txt', 'data/mask.png']},
    entry_points={
        'console_scripts': ['pdf = pdf_to_wordcloud.pdf_to_wordcloud:pdf'],
    },
    install_requires=[
        'pdfplumber',
        'nltk',
        'pandas',
        'numpy',
        'matplotlib',
        'wordcloud',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
