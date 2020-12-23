# markdown-anki-decks

![PyPI](https://img.shields.io/pypi/v/markdown-anki-decks)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/markdown-anki-decks)
![PyPI - License](https://img.shields.io/pypi/l/markdown-anki-decks)

Markdown anki decks is a simple program to convert markdown files into anki decks.

```md
# The h1 tag is the deck title

## The h2 tags are the questions

The markdown content between h2 tags are the answers.
```

Markdown anki decks uses the question to uniquely identify the card.
You can change the card contents without losing your progress on the card.
Markdown anki decks can be reimported without creating duplicates.

## Installation

Make sure you have a python version of 3.7 or greater installed.

`pip install markdown-anki-decks`

This will install the `mdankideck` cli tool.

## Usage

Run `mdankideck input output` to convert the markdown files in the input directory to `apkg` files in the output directory.

## Tutorial

Markdown anki decks converts all markdown files in an input directory to `apkg` files.
The `apkg` files are stored in an output directory.

1. Create the input directory `mkdir input`.
2. Create the output directory `mkdir output`.
3. Create a markdown file in the input directory.

   ```md
   <!-- input/deck.md -->

   # Deck Title

   ## Card Title

   card contents.

   ## Second Card Title

   card contents 2.
   ```

4. Run `mdankideck input output` to convert the markdown files in the input directory to `apkg` files in the output directory.
5. Import `apkg` files as decks into anki.

## Images

Markdown anki decks support images which are stored in the same folder as the markdown file they are referenced by.

`![my-image](image.jpg)` will work because it is in the same folder as the markdown file.

`![my-image](./images/image.jpg)` will not work because it is in a different folder than the markdown file.

All images must have unique filenames even if they are stored in different folders.

These are limitations of anki not Markdown anki decks.

## Questions

All questions in a single deck must be unique.
Two questions in the same deck which are identical will have the same id and will lead to a collision.

## Design

The markdown files are parsed with [commonmark](https://pypi.org/project/commonmark/). The resulting html is then parsed with [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
Finally the cards are created with [genanki](https://github.com/kerrickstaley/genanki).
The cli is implemented using [typer](https://github.com/tiangolo/typer) and the program is packaged using [poetry](https://github.com/python-poetry/poetry).

## Contributing

Happy to discuss additional features if you open up an issue.

We use commitizen for commits.
Run `poetry run cz commit` to make a commit.

### Releases

Run `poetry run cz bump --check-consistency` to update the changelog and create a tag.

Create the build with `poetry build`.

Publish the build with `poetry publish`.
