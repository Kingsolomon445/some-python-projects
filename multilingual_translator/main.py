import requests
from bs4 import BeautifulSoup
from sys import argv

languages = [
    "Arabic",
    "German",
    "English",
    "Spanish",
    "French",
    "Hebrew",
    "Japanese",
    "Dutch",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Turkish"
]
print("Welcome to the translator")
src_lang = argv[1].strip().lower()
trg_lang = argv[2].strip().lower()
if src_lang.capitalize() not in languages or (trg_lang.capitalize() not in languages and trg_lang != "all"):
    print("The language you selected isn't supported")
    print("Supported Languages are:")
    for idx, language in enumerate(languages):
        print(f"{idx + 1}. {language}")
    exit()
word = argv[3].strip().lower()
translation_list = []
example_list = []
if trg_lang != "all":
    print(f'You chose "{trg_lang}" as the language to translate "{word}" to.')
else:
    print(f"You choose to translate to all languages.")


def request_page():
    headers = {
        'User-Agent': ""  # Add your User Agent here!
    }
    if not headers['User-Agent']:
        print("Add your user agent!")
        exit()
    url = f"https://context.reverso.net/translation/{src_lang}-{trg_lang}/{word}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Request failed!")
        exit()
    return response


# --------------------------These are for translations from one language to one language!-----------------------------#
def get_translations_and_examples_for_one_lang():
    global translation_list, example_list
    try:
        response = request_page()
        soup = BeautifulSoup(response.content, "html.parser")

        translations = soup.find(id="translations-content")
        translations = translations.find_all("span", class_="display-term")
        for trans in translations:
            translation_list.append(trans.text.strip())

        examples = soup.find_all("div", class_="example")
        for ex in examples:
            src_text = ex.find("div", class_=lambda value: value and value.startswith("src")).find("span",
                                                                                                   class_="text").text.strip()
            trg_text = ex.find("div", class_=lambda value: value and value.startswith("trg")).find("span",
                                                                                                   class_="text").text.strip()
            example_pair = {
                src_text: trg_text
            }
            example_list.append(example_pair)
    except Exception as e:
        print(f"An error {e} occurred")


def print_translation():
    print(f"{trg_lang.capitalize()} Translations:")
    if not translation_list:
        print("No translations were found")
    else:
        for translation in translation_list:
            print(translation)

    print(f"\n\n{trg_lang.capitalize()} Examples:")
    if not example_list:
        print("No examples were found")
    else:
        for example in example_list:
            for key, value in example.items():
                print(f"{key}\n{value}", end="\n" * 2)


def save_translation_to_file():
    with open(f"{word}.txt", 'w') as file:
        file.write(f"{trg_lang.capitalize()} Translations:\n")
        if not translation_list:
            file.write("No translations were found!\n")
        else:
            for translation in translation_list:
                file.write(translation + '\n')
        file.write(f"\n\n{trg_lang.capitalize()} Examples:\n")
        if not example_list:
            file.write("No examples were found\n")
        else:
            for example in example_list:
                for key, value in example.items():
                    file.write(f"{key}\n{value}\n\n\n")


# --------------------------These are for translations from one language to all language!-----------------------------#
def get_translation_and_example_for_all_languages():
    global trg_lang, translation_list, example_list

    for lang in languages:
        trg_lang = lang.lower()
        if trg_lang == src_lang:
            continue
        try:
            response = request_page()
            soup = BeautifulSoup(response.content, 'html.parser')
            translations = soup.find(id="translations-content")
            translation = soup.find_all("span", class_="display-term")[0]
            translation_list.append(translation.text.strip())
            example = soup.find_all("div", class_="example")[0]
            src_text = example.find("div", class_=lambda value: value and value.startswith("src")).find("span",
                                                                                                        class_="text").text.strip()
            trg_text = example.find("div", class_=lambda value: value and value.startswith("trg")).find("span",
                                                                                                        class_="text").text.strip()
            example_pair = {
                src_text: trg_text
            }
            example_list.append(example_pair)
        except Exception as e:
            print(f"An error {e} occurred while getting translation for {trg_lang}")
            continue


def print_all_transaltions():
    i = 0
    for lang in languages:
        if lang == src_lang.capitalize():
            continue
        print(f"{lang} Translations")
        print(translation_list[i], end="\n" * 2)
        print(f"{lang} Examples")
        for key, value in example_list[i].items():
            print(f"{key}:\n{value}", end="\n" * 3)
        i += 1


def save_all_translations_to_file():
    with open(f"{word}.txt", 'w') as file:
        i = 0
        for lang in languages:
            if lang == src_lang.capitalize():
                continue
            file.write(f"{lang} Translations\n")
            file.write(translation_list[i] + "\n\n")
            file.write(f"{lang} Examples\n")
            for key, value in example_list[i].items():
                file.write(f"{key}:\n{value}\n\n\n")
            i += 1


if trg_lang != "all":
    get_translations_and_examples_for_one_lang()
    save_translation_to_file()
    print_translation()
else:
    get_translation_and_example_for_all_languages()
    save_all_translations_to_file()
    print_all_transaltions()
