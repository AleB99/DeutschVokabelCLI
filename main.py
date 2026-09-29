from functions import (
    clearScreen,
    menu,
    req,
    createFlashCard,
    viewFlashcards
)
import requests

while True:
    clearScreen()
    menu()

    try:
        num = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a number.")
        input("\nPress Enter to continue...")
        continue

    clearScreen()

    if num == 1:

        while True:
            word = input(
                "Enter a German word (Enter to stop): "
            ).strip().lower()

            if word == "":
                break

            try:
                italian = req(word, "it")
                english = req(word, "en")

                print(f"\nGerman:  {word}")
                print(f"Italian: {italian}")
                print(f"English: {english}\n")

                addToFCs = input(
                    "Add this word to flashcards? (Y/n): "
                ).strip().lower()

                if addToFCs == "y":
                    createFlashCard(word, italian, english)

            except requests.RequestException as e:
                print(f"Translation error: {e}")

    elif num == 2:

        viewFlashcards()

        input("\nPress Enter to continue...")

    elif num == 3:

        print("Goodbye!")   
        break

    else:

        print("Invalid choice.")
        input("\nPress Enter to continue...")