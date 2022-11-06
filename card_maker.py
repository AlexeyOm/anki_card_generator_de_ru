import bs4 as bs
import requests
import genanki
from model import my_model

input_word = "Erde"

def main(input:str) ->dict:
    verbformen_not_found = "Немецкие существительные не были найдены"
    #base_url_pons = "https://en.pons.com/translate/german-russian/"
    base_url_vebformen = "https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w="
    page_text = requests.get(base_url_vebformen + input).text
    if verbformen_not_found in page_text:
        #TODO реализовать вставку ненайденного слова файл для ручной обработки
        return {"status": 2}
    soup = bs.BeautifulSoup(page_text, features="html.parser")
    main_word = soup.find("p", class_="vGrnd rCntr").find("b").text
    if main_word != input:
        #TODO реализовать вставку ненайденного слова в файл для ручной обработки
        return {"status": 3}

    question = soup.find("p", class_="r1Zeile rU3px rO0px").text
    #если у нас существительное
    if soup.find("p", class_="rInf").find("span", {"title" : "существительное"}):
        translation = soup.find("p", class_="vGrnd rCntr").contents[2].text[1:] + soup.find("p", class_="vGrnd rCntr").find("b").text
        #если есть форма множественного числ
        if len(soup.find("p", class_="vStm rCntr").findAll("b")) == 2:
            translation += " die " + soup.find("p", class_="vStm rCntr").findAll("b")[1].text
    #TODO добавление глагола
    #TODO добавление прилагательного
    #TODO добавление местоимения
    #если есть озвучка слова
    if soup.find("p", class_="vGrnd rCntr").find("a"):
        print("нашли звук")
        sound_url = soup.find("p", class_="vGrnd rCntr").find("a").get("href")
        response = requests.get(sound_url)
        mp3_file = f"C:\\Users\\Пользователь\\AppData\\Roaming\\Anki2\\Benutzer 1\\collection.media\\{input.lower()}.mp3"
        sound_field = f"[sound:{input.lower()}.mp3]"
        with open(mp3_file, "wb") as _:
            _.write(response.content)
    print({"status": 1, "question": question, "translation": main_word, "sound_url": mp3_file, "sound": sound_field})
    return {"status": 1, "question": question, "translation": main_word, "sound_url": mp3_file, "sound": sound_field}


if __name__ == "__main__":
    result = main(input_word)
    my_deck = genanki.Deck(
        2059400110,
        'Russian > Deutcsh vocab'
    )
    my_package = genanki.Package(my_deck)
    my_package.media_files = []
    match result["status"]:
        case 1:
            my_note = genanki.Note(
                model=my_model,
                fields=[result["question"], result["translation"], result["sound"]]
            )
            my_deck.add_note(my_note)
            my_package.media_files.append(result["sound_url"])
            genanki.Package(my_deck).write_to_file('output/result.apkg')
        case 2:
            print("слово не найдено")
        case 3:
            print("слово найдено в другой форме")
