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

## Usage

`mdankideck` comes with built in documentation. Run `mdankideck --help` to see it.

```
Usage: mdankideck [OPTIONS] INPUT_DIR OUTPUT_DIR

Arguments:
  INPUT_DIR   The input directory. Contains markdown files which will be
              converted to anki decks.  [required]

  OUTPUT_DIR  The output directory. Anki .apkg files will be written here.
              [required]


Options:
  --sync                Whether or not to synchronize the output with anki
                        using anki connect.  [default: False]

  --prefix TEXT         Can be used to make your markdown decks part of a
                        single subdeck. Anki uses `::` to indicate sub decks.
                        `markdown-decks::` could be used to make all generated
                        decks part of a single root deck `markdown-decks`
                        [default: ]

  --delete              Whether to delete cards from anki during sync. If sync
                        is false this has no effect.  [default: False]

  --cloze               Whether to support cloze syntax  [default: False]
  --version             Show version information  [default: False]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.
```

### Syncing

Markdown anki decks can use [AnkiConnect](https://ankiweb.net/shared/info/2055492159) to sync the created decks immediately to anki.
First you need to install AnkiConnect as an add on in Anki.
Then you need to call `mdankideck` with the `--sync` flag.
By default if you delete a question in markdown we do not delete the question in Anki during sync.
However you can delete missing questions in Anki during sync by calling `mdankideck` with the `--delete` flag.

If you see an error message `Unable to reach anki connect. Make sure anki is running and the Anki Connect addon is installed.`, make sure you have installed anki connect and that you are running anki.

```sh
# convert markdown file in the input directory to apkg files in the output
# directory and sync the decks to anki using anki connect
mdankideck input output --sync


# convert input to output with an empty deck prefix (default)
# and delete cards from anki if the question is deleted or changed in markdown
mdankideck input output --sync --delete
```

### Subdecks

You can use the Deck title prefix option to make all your markdown decks part of a single subdeck.
Anki automatically creates subdecks based on deck names.

> Decks can contain other decks, which allows you to organize decks into a tree. Anki uses “::” to show different levels. A deck called “Chinese::Hanzi” refers to a “Hanzi” deck, which is part of a “Chinese” deck. If you select “Hanzi” then only the Hanzi cards will be shown; if you select “Chinese” then all Chinese cards, including Hanzi cards, will be shown. [Source](https://docs.ankiweb.net/#/getting-started?id=decks)

I use a prefix `md::` to store all my markdown decks in a subdeck called `md`.

```sh
# sync all cards to anki with a root deck `md`
mdankideck input output True "md::" True
```

### Images

Markdown anki decks support images which are stored in the same folder as the markdown file they are referenced by.

`![my-image](image.jpg)` will work because it is in the same folder as the markdown file.

`![my-image](./images/image.jpg)` will not work because it is in a different folder than the markdown file.

All images must have unique filenames even if they are stored in different folders.

These are limitations of anki not Markdown anki decks.

### Sounds

Use the syntax `[sound:sound-file.mp3]` to add a sound to your card.

Markdown anki decks support sounds which are stored in the same folder as the markdown file they are referenced by.

`[sound:sound-file.mp3]` will work because it is in the same folder as the markdown file.

`[sound:./sounds/sound-file.mp3]` will not work because it is in a different folder than the markdown file.

All sounds must have unique filenames even if they are stored in different folders.

These are limitations of anki not Markdown anki decks.

### Styling Cards

The cards are styled with minimal css [markdown.css](markdown_anki_decks/styles/markdown.css).
Syntax highlighting is provided via [pygments](https://github.com/pygments/pygments).
The syntax highlighting uses the pygments default theme.

### Clozes (experimental)

mdankideck supports close syntax in questions if you call `mdankideck` with the `--cloze` flag. Clozes can be specified in the question using the template `{{c#::answer::hint}}` where `#` is a number and answer and hint are words or multiple words. The hint is optional so you can also write `{{c#::answer}}`. Clozes with the same `c#` will be hidden together.

The following markdown would create two cloze cards.

```md
## The alphabet starts with {{c1::a}} {{c2::b}} {{c1::a}}
```

`The alphabet starts with [...] b [...]`

and

`The alphabet starts with a [...] c`

The `c1` clozes are blocked out together.

#### Custom Styling

You can add custom styling using yaml frontmatter. The css key takes a path to a css file as a string or an array of paths to multiple css files.

```yaml
---
css: custom-styles.css
---
```

```yaml
---
css: ["one.css", "two.css", "three.css", "four.css"]
---
```

The paths to the css files are assumed to be relative to the markdown file.
Cards have the following html structure. During processing markdown anki decks wraps your answer in a section tag. So the answer will be `<section>{{Answer}}</section>`. This extra wrapping step is performed because answers can consist of multiple sibling html elements and we need to provide a single element to Anki.

```html
<!-- the question card -->
<div class="card">
  <div class="question">{{Question}}</div>
</div>

<!-- the answer card -->
<div class="card">
  <div class="question">{{Question}}</div>
  <hr />
  <div class="answer">{{Answer}}</div>
</div>
```

You can style cards in general using the `.card` selector and you can style questions and answers using the `.question` and `.answer` selector.

```css
/* apply red background to all cards */
.card {
  background: red;
}
```

### Mathjax

[Anki supports mathjax out of the box](https://docs.ankiweb.net/#/math?id=mathjax). However you need to be careful with how markdown escapes characters. The following code snippet will not render as mathjax when you convert it because markdown will assume you are trying to escape the parentheses and will render the text `(\sqrt{x})`

```md
\(\sqrt{x}\)
```

You need to escape the backslashes by using double backslashes.
The following snippet will work to render math using mathjax.

```md
<!-- this will render inline math -->

\\(\sqrt{x}\\)

<!-- this will render block math -->

\\[\sqrt{x}\\]
```

### Markdown Features

Most commonly used markdown features should work without any issues.
If there is a Markdown feature you want to use and it is supported by one of the [official extensions for python-markdown](https://python-markdown.github.io/extensions/#officially-supported-extensions) there is good chance it can be added to the project.
Check out `cli.py` to see the list of currently enabled extensions. (Search for `extensions=`)

#### Multiline questions

You may want to render complex questions which span multiple lines.
You can use the fact that any `h2` element is assumed to be a question combined with the fact that the markdown converter supports embedding markdown in html if you use the special attribute `markdown="block"` on the html element. It's much easier to see with an example.

```md
<h2 markdown="block">
- this question
- is actually
- a markdown list

You can even add math to your questions \\(\sqrt{2}\\)

</h2>
```

Additionally you may not want `h2` styling for your multiline question. In that case you can add the `data-question` attribute to any tag to make it a question.

```md
<div data-question markdown="block">

This is a question which does not have h2 formatting!

- it can contain nested markdown such as `code`

</div>
```

For more information [see the `md_in_html` documentation](https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/md_in_html.md)

## Limitations

Markdown anki decks makes some assumptions to enable syncing.
Cards are uniquely identified by their deck name and question.
If you change the deck name or the question you will lose the card history.
All deck names must be unique.
All questions in a single deck must be unique.
Identical questions in separate decks are ok.

## Design

The markdown files are parsed with [python-markdown](https://pypi.org/project/Markdown/). The resulting html is then parsed with [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
Finally the cards are created with [genanki](https://github.com/kerrickstaley/genanki).
The cli is implemented using [typer](https://github.com/tiangolo/typer) and the program is packaged using [poetry](https://github.com/python-poetry/poetry).

## Contributing

Happy to discuss additional features if you open up an issue.

We use commitizen for commits.
Run `poetry run cz commit` to make a commit.

Run `poetry run mdankideck --prefix "test::" --sync --cloze testData/input testData/output` to convert the test data into decks.

Run `poetry run pygmentize -S default -f html -a .codehilite > ./markdown_anki_decks/styles/pygments.css` to create a pygments stylesheet.
Run `poetry run pygmentize -S monokai -f html -a ".nightMode .codehilite" > ./markdown_anki_decks/styles/pygments-dark.css` to create the dark mode stylesheet.
The `-S` flag is used to specify the style. Run `poetry run pygmentize -L style` to list the styles pygmentize can use. Replace `default` with any of the styles to use a different style.

Currently use `default` for light mode and `monokai` for dark mode.

### Releases

Run `poetry run cz bump --check-consistency` to update the changelog and create a tag.

Run `poetry publish --build` to publish the pack to pypi.

`git push --tags && git push` to update github.
