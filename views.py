from flask import render_template, request, redirect, url_for, flash
from models import db, Playlists, Album
from werkzeug.utils import secure_filename
import uuid
import requests
import os


# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def fetch_music_data(mbid_list):
    all_data = []

    for mbid in mbid_list:
        url = f"https://musicbrainz.org/ws/2/recording/{mbid}"
        params = {
            "fmt": "json",
            "inc": "artist-credits+releases"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_data.append(data)  

    return all_data


def init_routes(app):
    
    @app.route('/', methods=['GET'])
    def get_musicb():
        artist = request.args.get('artist', '')
        title = request.args.get('title', '')
        recrel = request.args.get('recrel', 'release')
        limit = request.args.get('limit', '10')
        
        url = f"https://musicbrainz.org/ws/2/{recrel}"
        params = {
            "query": f'artist:"{artist}" AND {recrel}:"{title}"',
            "fmt": "json",
            "limit": {limit},
        }

        response = requests.get(url, params=params)
        data = response.json()

        final_data = data.get(f"{recrel}s", [])

        return render_template('musicbrainz.html', data=final_data, recrel=recrel)


    @app.route('/create', methods=['GET', 'POST'])
    def create_playlist():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                print("fail2")

                return redirect(request.url)
            if file and allowed_file(file.filename):
                extension = file.filename.split(".")[-1]
                new_filename = str(uuid.uuid4())+"."+extension
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                print("bazinga")


            new_playlist = Playlists(

                title=request.form['title'],

                creator=request.form['creator'],

                description=request.form['description'],

                songs=[],

                image=new_filename

            )

            db.session.add(new_playlist)

            db.session.commit()

            return redirect(url_for('get_playlists'))

        return render_template('create.html')
    

    @app.route('/playlists', methods=['GET'])
    def get_playlists():
        playlists = Playlists.query.all()

        return render_template('playlists.html', playlists=playlists)
    
    @app.route('/svp', methods=['GET'])
    def single_view_playlists():  
        id = request.args.get('pid', 1)
        playlist = db.session.query(Playlists).get(id)
        mbids = playlist.songs

        final_data = fetch_music_data(mbids)
        return render_template('single_view_playlist.html', playlist=playlist, data=final_data)
        
    
    

    @app.route('/search', methods=['GET'])
    def search_item():
        return render_template('search.html')

    @app.route('/update', methods=['POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.
        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        # This route should handle deleting an existing item identified by the given ID.
        return render_template('index.html', message=f'Item deleted successfully')
    











    # OLD STUFF:

    @app.route('/add', methods=['GET', 'POST'])
    def create_item():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                print("fail2")

                return redirect(request.url)
            if file and allowed_file(file.filename):
                extension = file.filename.split(".")[-1]
                new_filename = str(uuid.uuid4())+"."+extension
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                print("bazinga")


            new_album = Album(

                title=request.form['title'],

                artist=request.form['artist'],

                year=int(request.form['year']),

                rating=float(request.form['rating']),

                genre=request.form['genre'],

                image=new_filename

            )

            db.session.add(new_album)

            db.session.commit()

            return redirect(url_for('get_items'))

        return render_template('add.html')
    
    @app.route('/old', methods=['GET'])
    def get_items():
        albums = Album.query.all()

        return render_template('index.html', albums=albums)
