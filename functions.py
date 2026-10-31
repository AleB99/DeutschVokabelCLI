import json
import subprocess
import os
import deepl
from collections import deque
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


def printExample(flashcard, translations=True):
    example = flashcard.get("example", {})
    if not example.get("german"):
        return
    print(f"Example: {example['german']}")
    if translations:
        print(f"         {example.get('italian', '')}")
        print(f"         {example.get('english', '')}")


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
        printExample(flashcard)
        print("-" * 30)
    
def removeFlashcard(id):
    flashcards = loadFlashcards()

    for flashcard in flashcards:
        if flashcard["id"] == id:
            flashcards.remove(flashcard)
            saveFlashcards(flashcards)
            return True

    return False

# rating: (minimum gap in days, how much the previous gap is multiplied by)
reviewRules = {
    1: (7, 3.0),   # very easy
    2: (4, 2.5),   # easy
    3: (2, 1.5),   # medium
    4: (1, 0),     # hard: back tomorrow
    5: (0, 0)      # very hard: again in this session
}
MAX_INTERVAL = 365


def nextInterval(previous, rating):
    minimum, multiplier = reviewRules[rating]
    return min(MAX_INTERVAL, max(minimum, round(previous * multiplier)))

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

    queue = deque(cards_to_review)

    while queue:
        flashcard = queue.popleft()
        print(f"\n[{len(queue) + 1} left]")
        print(f"German: {flashcard['german']}")
        printExample(flashcard, translations=False)
        input("Press Enter to show answer...")
        print(f"\nItalian: {flashcard['italian']}")
        print(f"English: {flashcard['english']}")
        example = flashcard.get("example", {})
        if example.get("german"):
            print(f"Example: {example.get('italian', '')}")
            print(f"         {example.get('english', '')}")

        while True:
            try:
                difficulty = int(input("\nHow difficult was it? (1-5): "))
            except ValueError:
                difficulty = None

            if difficulty in reviewRules:
                break
            print("Please enter a number from 1 to 5.")

        review = flashcard["review"]
        days = nextInterval(review.get("interval", 0), difficulty)

        review["difficulty"] = difficulty
        review["interval"] = days
        review["lastReview"] = today.isoformat()
        review["nextReview"] = (today + timedelta(days=days)).isoformat()

        if difficulty == 5:
            queue.append(flashcard)
            print("This card will come back at the end of the round.")
        else:
            print(f"Next review in {days} day(s).")

    saveFlashcards(flashcards)