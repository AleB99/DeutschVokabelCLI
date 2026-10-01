import json
import subprocess
import os
import deepl
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
    print("3. Exit\n")

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
