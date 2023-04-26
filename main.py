import os
import openai
import random

from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    fields = prepareFields()
    
    return render_template('index.html', category=fields[0], answer=fields[1], clues=fields[2])


@app.route('/newgame', methods=['POST'])
def newgame():
    fields = prepareFields()
    
    return render_template('index.html', category=fields[0], answer=fields[1], clues=fields[2])


def cleanClues(clues):
    finalClues = []
