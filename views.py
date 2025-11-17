from flask import render_template, request, redirect, url_for, flash
from models import db, Songs, Album

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):

    @app.route('/', methods=['GET'])
    def get_items():
        albums = Album.query.all()
        album_display = {}

        for album in albums:
            album_display[album['id']] = {album['title'], album['artist'], album['album'], album['year'], album['genre']}

        return render_template('index.html', message=f'{album_display}')



    @app.route('/add', methods=['GET', 'POST'])
    def create_item():
        if request.method == 'POST':

            new_album = Album(

                title=request.form['title'],

                artist=request.form['artist'],

                year=int(request.form['year']),

                rating=float(request.form['rating']),

                genre=request.form['genre']

            )

            db.session.add(new_album)

            db.session.commit()

            return redirect(url_for('index'))

        return render_template('add.html')



    @app.route('/update', methods=['POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.
        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        # This route should handle deleting an existing item identified by the given ID.
        return render_template('index.html', message=f'Item deleted successfully')