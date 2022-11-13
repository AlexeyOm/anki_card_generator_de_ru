import requests
import bs4 as bs

def parse_duden_get_sound(input:str):
    base_url_duden = "https://www.duden.de/suchen/dudenonline/"
    duden_not_found = "keine Treffer"
    page_text = requests.get(base_url_duden + input).text
    if duden_not_found in page_text:
        print("выходим 2")
        return {"status": 2}
    soup = bs.BeautifulSoup(page_text, features="html.parser")
    if soup.find("h2", class_="vignette__title"):
        final_page = soup.find("h2", class_="vignette__title").a.get("href")
        page_text = requests.get("https://duden.de" + final_page).text
        soup = bs.BeautifulSoup(page_text, features="html.parser")
        if soup.find("a", class_="pronunciation-guide__sound"):
            sound_url = soup.find("a", class_="pronunciation-guide__sound").get("href")
            print(f"{sound_url=}")
            response = requests.get(sound_url)
            mp3_file = f"C:\\Users\\Пользователь\\AppData\\Roaming\\Anki2\\Benutzer 1\\collection.media\\{input.lower()}.mp3"
            with open(mp3_file, "wb") as _:
                _.write(response.content)
            sound_field = f"[sound:{input.lower()}.mp3]"
            print({"status": 1, "translation": input, "sound_url": mp3_file, "sound": sound_field})
            return {"status": 1, "translation": input, "sound_url": mp3_file, "sound": sound_field}
    return{"status": 5}