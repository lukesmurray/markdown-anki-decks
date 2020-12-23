import hashlib
import itertools
import os
from pathlib import Path

import commonmark
import genanki
import typer
from bs4 import BeautifulSoup
from commonmark.blocks import Parser
from genanki import deck

app = typer.Typer()


@app.command("convert")
def convertMarkdown(source: Path, output: Path):
    """our first CLI with typer!"""
    parser = commonmark.Parser()

    # iterate over the source directory
    for root, subdirs, files in os.walk(source):
        for file in files:
            if is_markdown_file(file):
                deck = parse_markdown(parser, os.path.join(root, file))
                package = genanki.Package(deck)
                # add all image files to the package
                package.media_files = image_files(source)
                package.write_to_file(os.path.join(output, f"{Path(file).stem}.apkg"))


def parse_markdown(parser: Parser, file: str) -> deck:
    markdown_string = read_file(file)
    ast = parser.parse(markdown_string)
    renderer = commonmark.HtmlRenderer()
    html = renderer.render(ast)
    soup = BeautifulSoup(html, "html.parser")

    # model for an anki deck
    model = genanki.Model(
        model_id=integer_hash("Simple Model"),
        name="Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
        # TODO(lukemurray): add css?
    )

    # get the deck title
    deck_title = Path(file).stem
    h1 = soup.h1
    if h1 is not None and h1.text:
        deck_title = h1.text

    # create the deck
    deck_id = integer_hash(deck_title)
    deck = genanki.Deck(deck_id=deck_id, name=deck_title)

    # add model to deeck
    deck.add_model(model)

    # get the notes
    note_headers = soup.find_all("h2")
    for header in note_headers:
        # the question is the header
        question = header

        # the contents are everything until the next header
        contents = list(
            itertools.takewhile(lambda el: el.name != "h2", header.next_siblings)
        )

        # wrap the contents in a section tag. the section is the answer.
        answer = soup.new_tag("section")
        contents[0].wrap(answer)
        for content in contents[1:]:
            answer.append(content)

        # create the note using the simple model
        note = FrontIdentifierNote(
            deck_id,
            model=model,
            fields=[soup_to_html_string(question), soup_to_html_string(answer)],
        )
        deck.add_note(note)

    return deck


# genanki Note which has a unique id based on the deck and the question
class FrontIdentifierNote(genanki.Note):
    def __init__(self, deck_id, model=None, fields=None, sort_field=None, tags=None):
        super().__init__(
            model=model,
            fields=fields,
            sort_field=sort_field,
            tags=tags,
            guid=genanki.guid_for(fields[0], deck_id),
        )


# convert beautiful soup object to a string
def soup_to_html_string(soup):
    return soup.prettify(formatter="html5")


# convert a file to a string
def read_file(file):
    with open(file) as f:
        markdown_string = f.read()
    return markdown_string


# check if a file is a markdown file
def is_markdown_file(file):
    # TODO(lukemurray): parameterize markdown extensions?
    return file.endswith(".md")


# convert a string into a random integer from 0 to 1<<31 exclusive
# used to create model and deck ids
# from https://stackoverflow.com/a/42089311/11499360
def integer_hash(s: str):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % (1 << 31)


# get all the image files in a directory
def image_files(source: Path):
    return list(
        str(p)
        for p in itertools.chain(
            source.rglob("*.jpg"),
            source.rglob("*.jpeg"),
            source.rglob("*.png"),
            source.rglob("*.gif"),
        )
    )


def main():
    app()
