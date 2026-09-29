import json
import requests
import subprocess

FLASHCARDS_FILE = "flashcards.json"


def clearScreen():
    subprocess.run(["clear"])


def menu():
    print("\nDeutschVokabelCLI\n")
    print("Choose:")
    print("1. Translate word (German to Italian/English)")
    print("2. View flashcards")
    print("3. Exit\n")


def req(word: str, language: str):
    response = requests.get(
        "https://api.mymemory.translated.net/get",
        params={
            "q": word,
            "langpair": f"de|{language}"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["responseData"]["translatedText"]


def loadFlashcards():
    try:
        with open(FLASHCARDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def saveFlashcards(flashcards):
    with open(FLASHCARDS_FILE, "w", encoding="utf-8") as file:
        json.dump(flashcards, file, indent=4, ensure_ascii=False)


def createFlashCard(word: str, italian: str, english: str):
    flashcards = loadFlashcards()

    flashcard = {
        "german": word,
        "italian": italian,
        "english": english
    }

    flashcards.append(flashcard)

    saveFlashcards(flashcards)

    print("Flashcard added!")


def viewFlashcards():
    flashcards = loadFlashcards()

    if not flashcards:
        print("No flashcards yet.")
        return

    print("\nYour flashcards:\n")

    for flashcard in flashcards:
        print(f"German:  {flashcard['german']}")
        print(f"Italian: {flashcard['italian']}")
        print(f"English: {flashcard['english']}")
        print("-" * 30)
