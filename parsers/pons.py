import requests

#curl -v --header "X-Secret: c5281d337e0e1c101b4a60ad8f26f710abf7bc6ce71c574ab3f00a42fc406885" "https://api.pons.com/v1/dictionary?l=deru&q=dazu"

def parse_pons(input: str):
    base_url_pons = "https://api.pons.com/v1/dictionary?l=deru&q="
    pons_similar = "You are viewing results spelled similarly"
    pons_not_found = "No translations were found in the PONS Dictionary"
    headers = {'X-Secret': 'c5281d337e0e1c101b4a60ad8f26f710abf7bc6ce71c574ab3f00a42fc406885'}
    response = requests.get(base_url_pons + input, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        print("не 200")
        return {"status": 5}

    page_json = response.json()
    parts_of_speech = page_json[0]['hits'][0]['roms']
    full_translation = set()
    for part_of_speech in parts_of_speech:
        #print(f"{part_of_speech=}")
        for headword in part_of_speech['arabs']:
            for translation in headword['translations']:
                if "headword" in translation["source"]:
                    #print(f"{translation['target']=}")
                    full_translation.add(translation['target'])
    full_translation = ", ".join(list(full_translation))
    print(full_translation)
    return {"status": 1, "question": full_translation, "translation": input}