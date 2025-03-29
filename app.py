from flask import Flask, request, render_template, redirect, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'meowmeow22'  # Change this to a secure key


API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    no_recipes_found = False
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        session['ingredients'] = ingredients
        recipes = get_recipes(ingredients)
    elif 'ingredients' in session:
        recipes = get_recipes(session['ingredients'])
    if not recipes:
        no_recipes_found = True
    return render_template('index.html', recipes=recipes, no_recipes_found=no_recipes_found)


def get_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []
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
