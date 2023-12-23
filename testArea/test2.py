import json


with open('card.json', 'r') as file:
    file = json.load(file)

    for card in file.values():
        print(card)



