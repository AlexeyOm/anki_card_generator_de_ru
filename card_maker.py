from typing import List
import bs4 as bs
import requests
import genanki
from model import my_model
from parsers import parse_duden_get_sound, parse_verbformen, parse_pons
input_word = "machen"

if __name__ == "__main__":

    with open("input.txt", "r") as _:
        input_words = _.readlines()
    print(input_words)
    my_deck = genanki.Deck(
        2059400110,
        'Russian > Deutcsh vocab'
    )
    my_package = genanki.Package(my_deck)
    my_package.media_files = []
    failed_words = []
    got_a_card = False
    for input_word in input_words:
        print(input_word)
        result = parse_verbformen(input_word.strip())
        match result["status"]:
            case 1:
                got_a_card = True
                my_note = genanki.Note(
                    model=my_model,
                    fields=[result["question"], result["translation"], result["sound"]]
                )
                my_deck.add_note(my_note)
                my_package.media_files.append(result["sound_url"])
                print(f"{input_word};успешно добавлено")
                continue
            case 2:
                print(f"{input_word};слово не найдено")
            case 3:
                print(f"{input_word};слово найдено в другой форме")
            case 4:
                print(f"{input_word};не найден перевод")
            case 4:
                print(f"{input_word};что-то не то")
        failed_words.append(input_word.strip())

    print(f"{failed_words=}")
    for input_word in failed_words:
        result = parse_pons(input_word)
        if result["status"] == 1:
            got_a_card = True
            fields = [result["question"], result["translation"]]
            sound_result = parse_duden_get_sound(input_word)
            if sound_result["status"] == 1:
                fields.append(sound_result["sound"])
                my_package.media_files.append(sound_result["sound_url"])
            my_note = genanki.Note(
                model=my_model,
                fields=[result["question"], result["translation"], sound_result["sound"]]
            )
            my_deck.add_note(my_note)


    if got_a_card:
        genanki.Package(my_deck).write_to_file('output/result.apkg')
