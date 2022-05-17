from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
import requests
import random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


app = Flask(__name__)
Bootstrap(app)
app.secret_key = "JedxCLUB"


class MyForm(FlaskForm):
    name = StringField(label="Pokemon name")
    submit = SubmitField(label="Search")


@app.route('/')
def home():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
    response.raise_for_status()
    data = response.json()['results']
    return render_template('index.html', poke=random.choice(data))


@app.route('/pokemons', methods=["GET", "POST"])
def database():
    name_form = MyForm()
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
    response.raise_for_status()
    data = response.json()
    data_length_4 = int(len(data) / 4)
    if request.method == "POST":
        try:
            return redirect(url_for('details', name=name_form.name.data))
        except requests.exceptions.HTTPError:
            return redirect(url_for('database'))
    return render_template('database.html', pokemons=data, pokemons_len=data_length_4, form=name_form)


@app.route('/pokemon/<name>')
def details(name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    response.raise_for_status()
    data = response.json()
    if len(data) < 1:
        return redirect(url_for('database'))
    return render_template('pokemonDetails.html', pokemon=data)


if __name__ == "__main__":
    app.run()



