import requests
import bs4 as bs

def parse_verbformen(input:str) ->dict:
    verbformen_not_found = "Немецкие существительные не были найдены"
    base_url_vebformen = "https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w="
    page_text = requests.get(base_url_vebformen + input).text
    if verbformen_not_found in page_text:
        return {"status": 2}
    soup = bs.BeautifulSoup(page_text, features="html.parser")
    if not soup.find("p", class_="vGrnd"):
        return {"status": 2}
    main_word = soup.find("p", class_="vGrnd").find("b").text
    if main_word != input:
        #TODO реализовать вставку ненайденного слова в файл для ручной обработки
        return {"status": 3}

    question = soup.find("p", class_="r1Zeile rU3px rO0px").text.strip()
    #если нет перевода
    if not question:
        return {"status": 4}
    if soup.find("p", class_="rInf"):
        word_info = soup.find("p", class_="rInf")
    else:
        return {"status": 5}
    #если у нас существительное
    #TODO проверка существования файла при записи, генерация имени с префиксом и номером
    if word_info.find("span", {"title" : "существительное"}):
        translation = soup.find("p", class_="vGrnd rCntr").contents[2].text[1:] + soup.find("p", class_="vGrnd rCntr").find("b").text
        #если есть форма множественного числ
        if len(soup.find("p", class_="vStm rCntr").findAll("b")) == 2:
            translation += " die " + soup.find("p", class_="vStm rCntr").findAll("b")[1].text
    #если у нас прилагательное
    elif word_info.find("span", {"title" : "прилагательное"}):
        translation = soup.find("p", class_="vGrnd rCntr").contents[2].text[1:]
    elif word_info.find("span", [{"title" : "правильный"}, {"title" : "неправильный"}]):
        translation = soup.find("p", class_="vGrnd rCntr").contents[2].text[1:].strip()
    question = question.replace("\n", " ")
    question = question.replace("а́", "а")
    question = question.replace("е́", "е")
    question = question.replace("и́", "и")
    question = question.replace("о́", "о")
    question = question.replace("у́", "у")
    question = question.replace("ы́", "ы")
    question = question.replace("э́", "э")
    question = question.replace("я́", "я")

    # TODO добавление прилагательного
    # TODO добавление местоимения
    #если есть озвучка слова
    if soup.find("p", class_="vGrnd").find("a"):
        print("нашли звук")
        sound_url = soup.find("p", class_="vGrnd").find_all("a")[-1].get("href")
        print(f"{sound_url=}")
        response = requests.get(sound_url)
        mp3_file = f"C:\\Users\\Пользователь\\AppData\\Roaming\\Anki2\\Benutzer 1\\collection.media\\{input.lower()}.mp3"
        sound_field = f"[sound:{input.lower()}.mp3]"
        with open(mp3_file, "wb") as _:
            _.write(response.content)
    else:
        return{"status": 4}
    print({"status": 1, "question": question, "translation": main_word, "sound_url": mp3_file, "sound": sound_field})
    return {"status": 1, "question": question, "translation": main_word, "sound_url": mp3_file, "sound": sound_field}
