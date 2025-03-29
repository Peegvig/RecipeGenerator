from flask import Flask, request, render_template, redirect, url_for, session
import requests
import os
import logging

app = Flask(__name__)
app.secret_key = 'meowmeow22'  # Change this to a secure key

logging.basicConfig(level=logging.DEBUG)

API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    no_recipes_found = False
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        logging.debug(f"Received ingredients: {ingredients}")
        session['ingredients'] = ingredients
        recipes = get_recipes(ingredients)
        if not recipes:
            no_recipes_found = True
        return render_template('index.html', recipes=recipes, no_recipes_found=no_recipes_found)
    elif 'ingredients' in session:
        logging.debug(f"Using session ingredients: {session['ingredients']}")
        recipes = get_recipes(session['ingredients'])
    if not recipes:
        no_recipes_found = True
    return render_template('index.html', recipes=recipes, no_recipes_found=no_recipes_found)


def get_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={API_KEY}"
    logging.debug(f"API URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        logging.debug("API call successful.")
        return response.json()
    else:
        logging.error(f"API call failed with status code {response.status_code}: {response.text}")
        return []

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        recipe = response.json()
        return render_template('recipe_details.html', recipe=recipe)
    else:
        return "Recipe not found or API error."

if __name__ == "__main__":
    app.run(debug=True)
