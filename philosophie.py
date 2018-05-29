#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
from flask import Flask, render_template, session, request, redirect, flash, get_flashed_messages
from getpage import getPage

app = Flask(__name__)

app.secret_key = "sklfjdkcjkfjclfjf"  # "TODO: mettre une valeur secrète ici"

# initatialisation du cache
cache = dict()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Si vous définissez de nouvelles routes, faites-le ici
@app.route('/new-game', methods=['POST'])
def new_game():
    if request.form['start']:
        if request.form['start'].lower() == 'philosophie':
            flash("Ne commencez pas directement avec Philosophie ! \
                  Soyez fair-play, essayez un autre article.")
            session['win'] = False
            return redirect('/')
        else:
            session['article'] = request.form['start']
            session['score'] = 0
            return redirect('/game')
    else:
        return redirect('/')  # cas où utilisateur démarre le jeu sans avoir fournit une page de départ


@app.route('/game', methods=['GET'])
def game():
    request = session['article']
    #request = request.capitalize()  # met la 1ere lettre d'un mot (ou ensemble de mots) en majuscule
    #  Retiré car dangeureux.. ex: 'Thierry Lhermite' existe mais pas 'Thierry lhermite'
    #  De même, si on utilisait title(), qui met en majuscule toutes les premières lettres des mots d'un ensemble,
    #   on aurait également des soucis : par ex. 'Langue des signes' existe mais pas 'Langue Des Signes'
    if request in cache:
        title, links = cache[request]
    else:
        title, links = getPage(request, limit=10)
        cache[request] = (title, links)
    session['title'] = title
    session['links'] = links

#    # Verif que le cache marche bien
#    session['cache'] = cache
    
    if not title:
        flash("L'article {} n'existe pas. Retentez avec un autre nom.".format(request))
        session['win'] = False
        return redirect('/')
    elif not links:
        if request != title:
            flash("Perdu ! L'article {} redirige vers {}, \
                  mais cet article ne renvoie aucun lien...".format(request, title))
        else:
            flash("Perdu ! L'article {} ne renvoie aucun lien...".format(request))
        session['win'] = False
        return redirect('/')
    elif title == 'Philosophie':
        if session['score'] == 0:
            flash("L'article {} redirige directement vers Philosophie. \
                  Essayez un autre article.".format(request))
            session['win'] = False
        else:  # en cours de jeu, choisit lien qui redirige sur Philosphie (par ex. Empirisme > Philosophique)
            if session['score'] > 1:
                coup_s = "coups"
            else : 
                coup_s = "coup"
            flash("Vous ne vous y attendiez pas, mais vous venez de gagner en {} {} !\
                  En effet, l'article {} redirige \
                  directement vers Philosophie.".format(session['score'], coup_s, request))
            session['win'] = True
        return redirect('/')
    else:
        return render_template('game.html')


@app.route('/move', methods=['POST'])
def move():
    session['score'] += 1
    selected = request.form['destination']
    if selected not in session['links']:  # if user cheat by sending a manually modified POST request
        flash("Erreur, " + selected + " a été fourni mais ne faisait pas partie des choix disponibles.")
        session['win'] = False
        return redirect('/')
    elif selected == "Philosophie":
        if session['score'] > 1:
            flash("Bravo, vous avez gagné en " + str(session['score']) + " coups !")
        else:
            flash("Bravo, vous avez gagné en " + str(session['score']) + " coup !")
        session['win'] = True
        return redirect('/')
    else:
        session['article'] = selected
        return redirect('/game')


@app.route('/quit_game', methods=['POST'])
def quit_game():
    flash("Vous venez d'abandonner une partie en cours.")
    session['win'] = False
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

