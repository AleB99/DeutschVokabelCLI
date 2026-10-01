from functions import (
    clearScreen,
    menu,
    req,
    createFlashCard,
    viewFlashcards,
    removeFlashcard
)

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

                print(f"Italian: {italian}")
                print(f"English: {english}\n")

                addToFCs = input("Add this word to flashcards? (Y/n): ").strip().lower()

                if addToFCs == "y":
                    createFlashCard(word, italian, english)

            except Exception as e:
                print(f"Translation error: {e}")

    elif num == 2:
        viewFlashcards()
        input("\nPress Enter to continue...")

    elif num == 3:
        try:
            id = int(input("\nEnter the ID of the flashcard you'd like to remove: "))
            if removeFlashcard(id):
                print("Flashcard removed!")
            else:
                print("Flashcard not found.")
        except ValueError:
            print("Please enter a valid ID.")
    
    elif num == 4:
        break

    else:
        print("Invalid choice.")
        input("\nPress Enter to continue...")