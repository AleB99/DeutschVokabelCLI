import json
import subprocess
import os
import deepl
from datetime import datetime, timedelta
from dotenv import load_dotenv

FLASHCARDS_FILE = "flashcards.json"
CONFIG_FILE = "config.json"

_translator_instance = None
def get_deepl_translator():
    global _translator_instance
    if _translator_instance is not None:
        return _translator_instance
        
    load_dotenv()
    api_key = os.getenv("DEEPL_API_KEY")
        
    if not api_key:
        print("\nDeepL API key not found or not set.")
        exit(1)
            
    _translator_instance = deepl.Translator(api_key)
    return _translator_instance

def clearScreen():
    subprocess.run(["clear"])

def menu():
    print("\nDeutschVokabelCLI\n")
    print("Choose:")
    print("1. Translate word (German to Italian/English)")
    print("2. View flashcards")
    print("3. Remove flashcard by ID")
    print("4. Train")
    print("5. Exit\n")

def req(word: str, language: str):
    translator = get_deepl_translator()
    target_lang = "IT" if language.lower() == "it" else "EN-US"
    result = translator.translate_text(word, source_lang="DE", target_lang=target_lang)
    return result.text


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
    
    if flashcards:
        id = max(card["id"] for card in flashcards) + 1
    else:
        id = 0

    flashcard = {
        "id": id,
        "german": word,
        "italian": italian,
        "english": english,
        "review": {
        "difficulty": 0,
        "lastReview": "",
        "nextReview": datetime.now().date().isoformat()
    }
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
        print(f"Id:  {flashcard['id']}")
        print(f"German:  {flashcard['german']}")
        print(f"Italian: {flashcard['italian']}")
        print(f"English: {flashcard['english']}")
        print("-" * 30)
    
def removeFlashcard(id):
    flashcards = loadFlashcards()

    for flashcard in flashcards:
        if flashcard["id"] == id:
            flashcards.remove(flashcard)
            saveFlashcards(flashcards)
            return True

    return False

reviewIntervals = {
    1: 14,
    2: 7,
    3: 5,
    4: 2,
    5: 0
}

def getCardsToReview(flashcards):
    today = datetime.now().date().isoformat()

    cards_to_review = []
    for card in flashcards:
        if card["review"]["nextReview"] <= today:
            cards_to_review.append(card)

    cards_to_review.sort(key=lambda card: card["review"]["nextReview"])

    return cards_to_review


def trainFlashcards():
    flashcards = loadFlashcards()
    cards_to_review = getCardsToReview(flashcards)

    print(f"\nYou have {len(cards_to_review)} flashcards to review today")

    today = datetime.now().date()

    for flashcard in cards_to_review:
        print(f"\nGerman: {flashcard['german']}")
        input("Press Enter to show answer...")
        print(f"\nItalian: {flashcard['italian']}")
        print(f"English: {flashcard['english']}")

        difficulty = int(input("\nHow difficult was it? (1-5): "))

        if difficulty not in reviewIntervals:
            print("Invalid difficulty.")
            continue

        days = reviewIntervals[difficulty]

        flashcard["review"]["difficulty"] = difficulty
        flashcard["review"]["lastReview"] = today.isoformat()
        flashcard["review"]["nextReview"] = (today + timedelta(days=days)).isoformat()

    saveFlashcards(flashcards)