import requests
import subprocess

def clearScreen():
    subprocess.run(["clear"])

def menu():
    print("\nDeutschVokabelCLI\n")
    print("Choose:")
    print("1. Translate word (German to Italian/English)")
    print("2. Add flashcard")
    print("3. Exit\n")


def req(word: str, language: str):
    response = requests.get(
        "https://api.mymemory.translated.net/get",
        params = {
            "q": word,
            "langpair": f"de|{language}"
        },
        timeout = 10
    )

    response.raise_for_status()
    data = response.json()

    return data["responseData"]["translatedText"]


while True:
    menu()
    num: int = int(input("Enter your choice: "))
    clearScreen()
    if num == 1:
        while True:
            word = input("Enter a German word (Enter to stop): ")

            if word == "":
                break

            try:
                italian = req(word, "it")
                english = req(word, "en")

                print(f"\nGerman:  {word}")
                print(f"Italian: {italian}")
                print(f"English: {english}\n")

            except requests.RequestException as e:
                print(f"Translation error: {e}")

    elif num == 2:
        print("Flashcard functionality coming soon!")

    elif num == 3:
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")