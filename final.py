import re
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from fpdf import FPDF

# Downloading NLTK data
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Shelf Numbers", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def greetingFunction(inputStatement):
    greetingsPhrases = [
        "hi",
        "hello",
        "good morning",
        "good afternoon",
        "good evening",
        "hey",
        "howdy",
        "greetings",
        "salutations",
        "what's up",
        "hiya",
        "hey there",
        "how's it going",
        "yo",
        "good day",
        "hi there",
    ]
    for greeting in greetingsPhrases:
        if greeting in inputStatement.lower():
            return True
    return False


def farewellFunction(inputStatement):
    farewellPhrases = [
        "bye",
        "goodbye",
        "see you",
        "take care",
        "farewell",
        "later",
        "see ya",
        "adios",
        "ciao",
        "au revoir",
        "peace",
        "catch you later",
    ]
    for farewell in farewellPhrases:
        if farewell in inputStatement.lower():
            return True
    return False


def preProcessingFunction(inputStatement):

    # word tokenization
    tokens = nltk.word_tokenize(inputStatement.lower())

    # Removal of stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatization and stemming
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    tokens = [stemmer.stem(word) for word in tokens]
    return tokens


def goodsSearch(tokens, inventory):
    finds = []
    for token in tokens:
        if token in inventory:
            finds.append(token)
    return finds


def main():
    # Goods list
    inventory = {
        "apple": 1,
        "banana": 2,
        "bread": 3,
        "milk": 4,
        "egg": 5,
        "cheese": 6,
        "orange": 7,
        "grapes": 8,
        "carrot": 9,
        "tomato": 10,
        "potato": 11,
        "onion": 12,
        "lettuce": 13,
        "cucumber": 14,
        "chicken": 15,
        "beef": 16,
        "pork": 17,
        "fish": 18,
        "shrimp": 19,
        "rice": 20,
        "pasta": 21,
        "cereal": 22,
        "flour": 23,
        "sugar": 24,
        "salt": 25,
        "pepper": 26,
        "butter": 27,
        "yogurt": 28,
        "ice cream": 29,
        "bread": 30,
        "crackers": 31,
        "chips": 32,
        "soda": 33,
        "juice": 34,
        "water": 35,
        "coffee": 36,
        "tea": 37,
        "honey": 38,
        "jam": 39,
        "ketchup": 40,
        "mustard": 41,
        "mayonnaise": 42,
        "vinegar": 43,
        "olive oil": 44,
        "canola oil": 45,
        "toilet paper": 46,
        "paper towels": 47,
        "soap": 48,
        "shampoo": 49,
        "toothpaste": 50,
    }

    stemmer = PorterStemmer()
    inventoryAfterStemming = {
        stemmer.stem(parameter): value for parameter, value in inventory.items()
    }

    # Initialization of PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    print(" Welcome to the Supermarket. I'm the supermarket chatbot")
    while True:
        userInputText = input("\nHow can I help you? ").strip()
        if farewellFunction(userInputText):
            print("Thank you for your visit. Have a nice day!")
            break
        if greetingFunction(userInputText):
            print("Hello, nice to meet you!")
            continue

        tokens = preProcessingFunction(userInputText)

        neededGoods = goodsSearch(tokens, inventoryAfterStemming)
        if not neededGoods:
            print("Not sure about this. ")
        else:
            # Getting shelf number
            for good in neededGoods:
                noOfShelf = inventoryAfterStemming.get(good)
                if noOfShelf:
                    realGood = [
                        parameter
                        for parameter, value in inventory.items()
                        if stemmer.stem(parameter) == good
                    ][0]
                    displayText = f"Shelf number for {realGood.title()} is {noOfShelf}"
                    print(displayText)
                    pdf.cell(0, 10, displayText, 0, 1)
                else:
                    print(f"Sorry, {good.title()} is out of stock")

        moreTask = input("\nNeed any additional assistance?  ").strip().lower()
        responses = [
            "yes",
            "yeah",
            "ye",
            "yep",
            "sure",
            "yup",
            "ok",
            "okay",
        ]
        if moreTask not in responses:
            print("Thank you for your visit. Have a nice day!")
            break

    # Saving to the PDF
    pdf.output("Shelf_Numbers.pdf")


if __name__ == "__main__":
    main()
