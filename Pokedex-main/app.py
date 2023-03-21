import requests
import os
from flask import Flask, render_template,request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemon_name = requests.form = ['pokemon_name']
        respuesta = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
        datos=respuesta.json
        if respuesta.status_code == 200:
            nombre = datos["name"]
            altura = datos["height"]
            peso = datos["weight"]
            tipo = datos["tipo"]
            return (render_template("index.html"))
    else:
        return (render_template("index.html"))
