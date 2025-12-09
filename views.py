from flask import render_template, request, redirect, url_for, flash
from models import db, Songs, Album
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


def init_routes(app):

    @app.route('/', methods=['GET'])
    def get_items():
        albums = Album.query.all()

        return render_template('index.html', albums=albums)


    
    @app.route('/mb', methods=['GET'])
    def get_musicb():
        artist = request.args.get('artist', '')
        title = request.args.get('title', '')
        url_rel = "https://musicbrainz.org/ws/2/release"
        params_rel = {
            "query": f'artist:{artist} AND release:{title}',
            "fmt": "json",
        }

        response_rel = requests.get(url_rel, params=params_rel)
        data_rel = response_rel.json()

        # This is the full list of recordings
        releases = data_rel.get("releases", [])

        
        url_rec = "https://musicbrainz.org/ws/2/recording"
        params_rec = {
            "query": f'artist:{artist} AND recording:{title}',
            "fmt": "json",
        }

        response_rec = requests.get(url_rec, params=params_rec)
        data_rec = response_rec.json()

        # This is the full list of recordings
        recordings = data_rec.get("recordings", [])

        return render_template('musicbrainz.html', data=releases, data2=recordings)


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

    



    @app.route('/update', methods=['POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.
        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        # This route should handle deleting an existing item identified by the given ID.
        return render_template('index.html', message=f'Item deleted successfully')