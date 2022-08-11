from flask_app import app
from flask import render_template, request, redirect, session, url_for, jsonify
import os
from dotenv import load_dotenv
from flask_app.models.login import Login
from flask_app.models.album import Album

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def calculate_rating():
    top_rating = {}

    for album in Album.get_all():
        if sp.album(album.album_id)['id'] in top_rating:
            top_rating[sp.album(album.album_id)['id']].append(album.rating)
        else:
            top_rating[sp.album(album.album_id)['id']] = [album.rating]

    for key in top_rating:
        top_rating[key] = [sum(top_rating[key]) / len(top_rating[key])]


    sorted_rating = { k: v for k,v in sorted(top_rating.items(), key = lambda v: v[1], reverse=True)}

    count = 0
    for key in sorted_rating:
        count +=1
        sorted_rating[key].append(count)

    return sorted_rating

def calculate_pop():
    top_popularity = {}

    for album in Album.get_all():
        if sp.album(album.album_id)['id'] in top_popularity:
            top_popularity[sp.album(album.album_id)['id']][0] += 1
        else:
            top_popularity[sp.album(album.album_id)['id']] = [1]

    sorted_popularity = { k: v for k,v in sorted(top_popularity.items(), key = lambda v: v[1], reverse=True)}

    count = 0
    for key in sorted_popularity:
        count +=1
        sorted_popularity[key].append(count)

    return sorted_popularity



@app.route('/dashboard',methods = ['POST', 'GET'])
def login_sp():
	if request.method == 'POST':
		
		results = sp.search(q=request.form['nm'], type = 'album',  limit=10)
        
		songlist = results['albums']['items']
        
		return render_template('home_page.html', tracks=songlist)
		# return jsonify(results)
	else:
		user = request.args.get('nm')
		return render_template('home_page.html')

@app.route('/album/page/<id>')
def album_sp(id):
	if len(id) > 0:
		print(f'THIS IS THE ID: {id}')
		results = sp.album(id) 
		songlist = results
        
		return render_template('album_page.html', tracks=songlist, sp = sp, rating = calculate_rating(), popularity = calculate_pop())
		# return jsonify(results)
	else:
        
		return render_template('home_page.html', id = id)


@app.route('/profile')
def profile():
    
    data = {
        "id" : session['user_id']
    }
    
    return render_template("profile.html", login = Login.get_id(data), albums = Album.get_id(data), sp = sp)

@app.route('/rating/<id>', methods=['POST'])
def new_ranting(id):
    data = {
        "album_id" : id,
        "rating" : request.form['rating'],
        "registration_id" : session['user_id']
    }
    print(data)
    Album.insert(data)
    
    return redirect('/profile')

@app.route('/top/albums')
def top_albums():
    return render_template('top.html', sp = sp, rating = calculate_rating(), popularity = calculate_pop())


@app.route('/editor/<id>', methods=['POST'])
def new_edit(id):
    data = {
        'id' : session['user_id'],
        'rating' : request.form['rating']
    }

    Album.edit(data)
    return redirect('/profile')

@app.route('/delete/<id>')
def deletor(id):
    print(id)
    data = {
        "id" : id
    }
    Album.delete(data)
    return redirect('/profile')


