from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        recipes = get_recipes(ingredients)
    return render_template('index.html', recipes=recipes)

def get_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

if __name__ == "__main__":
    app.run(debug=True)
