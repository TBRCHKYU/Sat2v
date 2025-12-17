import json
import os

def calculate(recipe, output):
    with open('recipes.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)

    def branch(parent, ingredient, amount):
        print(parent, ingredient, amount, "9")
        if ingredient in recipes:
            parent = ingredient
            for_branch = recipes[ingredient]["ingredients"]
            print(for_branch, print("13"))
            for i in for_branch:
                print(i,"15")
                branch(parent, i, for_branch[i])

    if recipe in recipes:
        parent = recipe
        for_branch = recipes[recipe]["ingredients"]
        print(for_branch, print("21"))
        for i in for_branch:
            print(i,"23")
            branch(parent, i, for_branch[i])
    else:
        print("broke 26")
