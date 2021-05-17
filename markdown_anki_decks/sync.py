import json
import typing as t
import urllib.request
from pathlib import Path

from genanki import Deck, Model
from genanki.note import Note

from markdown_anki_decks.utils import print_error, print_success

anki_connect_url = "http://localhost:8765"


# helper for creating anki connect requests
def request(action, **params):
    return {"action": action, "params": params, "version": 6}


# helper for invoking actions with anki-connect
def invoke(action, **params):
    """Helper for invoking actions with anki-connect

    Args:
        action (string): the action to invoke

    Raises:
        Exception: invalid fields provided

    Returns:
        Any: the response from anki connect
    """
    global anki_connect_url
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(urllib.request.Request(anki_connect_url, requestJson))
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


def anki_connect_is_live():
    global anki_connect_url
    try:
        if urllib.request.urlopen(anki_connect_url).getcode() == 200:
            return True
        else:
            raise Exception()
    except Exception:
        print_error(
            "Unable to reach anki connect. Make sure anki is running and the Anki Connect addon is installed.",
        )

    return False


# synchronize the deck with markdown
def sync_deck(deck: Deck, pathToDeckPackage: Path, delete_cards: bool):
    if anki_connect_is_live():
        pathToDeckPackage = pathToDeckPackage.resolve()
        try:
            invoke("importPackage", path=str(pathToDeckPackage))
            print_success(f"Imported deck {deck.name}")
        except Exception as e:
            print_error(f"Unable to import deck {deck.name} to anki")
            print_error(f"\t{e}")

        if delete_cards:
            # delete removed cards
            try:
                # get a list of anki cards in the deck
                anki_card_ids: t.List[int] = invoke(
                    "findCards", query=f'"deck:{deck.name}"'
                )
                # get a list of anki notes in the deck
                anki_note_ids: t.List[int] = invoke("cardsToNotes", cards=anki_card_ids)
                # get the note info for the notes in the deck
                anki_notes_info = invoke("notesInfo", notes=anki_note_ids)
                # convert the note info into a dictionary of guid to note info
                anki_note_info_by_guid = {
                    n["fields"]["Guid"]["value"]: n for n in anki_notes_info
                }
                # get the unique guids of the anki notes
                anki_note_guids = anki_note_info_by_guid.keys()
                # get the unique guids of the md notes
                md_notes: t.List[Note] = deck.notes
                md_note_guids = set(n.guid for n in md_notes)
                # find the guids to delete
                guids_to_delete = anki_note_guids - md_note_guids
                if guids_to_delete:
                    invoke(
                        "deleteNotes",
                        notes=[
                            anki_note_info_by_guid[g]["noteId"] for g in guids_to_delete
                        ],
                    )
                    print_success("deleted removed notes")
            except Exception as e:
                print_error(f"Unable to sync removed cards from {deck.name}")
                print_error(f"\t{e}")


# synchronize the model and styling in the deck
def sync_model(model: Model):
    if anki_connect_is_live():
        try:
            invoke(
                "updateModelTemplates",
                model={
                    "name": model.name,
                    "templates": {
                        t["name"]: {
                            "qfmt": t["qfmt"],
                            "afmt": t["afmt"],
                        }
                        for t in model.templates
                    },
                },
            )
            print_success(f"\tUpdated model {model.name} template")
        except Exception as e:
            print_error(f"\tUnable to update model {model.name} template")
            print_error(f"\t\t{e}")

        try:
            invoke(
                "updateModelStyling",
                model={
                    "name": model.name,
                    "css": model.css,
                },
            )
            print_success(f"\tUpdated model {model.name} css")
        except Exception as e:
            print_error(f"\tUnable to update model {model.name} css")
            print_error(f"\t\t{e}")
