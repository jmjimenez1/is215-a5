#IS215-A5 Group 2

import os
import openai
import random

from flask import Flask, render_template, redirect, request, url_for, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    fields = prepareFields()
    
    return render_template('index.html', category=fields[0], answer=fields[1], clues=fields[2])


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/newgame', methods=['POST'])
def newgame():
    fields = prepareFields()
    
    return render_template('index.html', category=fields[0], answer=fields[1], clues=fields[2])


def cleanClues(clues):
    finalClues = []
    for clue in clues:
        if( len(clue) > 0 and clue[0].isdigit() ):
            finalClues.append(clue)
            
    return finalClues

def prepareFields():
    fields = []
    
    categories = ["Philippine City", "Filipino Actor or Actress", "Philippine President", "Filipino Food", "Philippine Province", "Philippine Tourist Spot", "Filipino Dessert", "Filipino TV Show", "Filipino Band", "Filipino Snack"]
    
    category = random.choice(categories)
    fields.append(category)
    
    
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    #get suggestion
    prompt = "Give me only 1 " + category + " name. Do not explain."
    response = openai.Completion.create(engine="text-davinci-001", prompt=prompt, max_tokens=50)
    answer = response["choices"][0]["text"].strip().upper()
    fields.append(answer)
    
    #get clues
    prompt = "Suggest 10 short sentences that will serve as clues for someone to guess the " + category + " " + answer + ". Do not mention " + answer
    response = openai.Completion.create(engine="text-davinci-001", prompt=prompt, max_tokens=1000)
    clues = cleanClues( response["choices"][0]["text"].split("\n") )
    fields.append(clues)
    
    return fields

if __name__ == '__main__':
    app.run(debug=True)