from flask import Flask
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode

#################################################################################################################
#Código basado en https://medium.com/@ashiqgiga07/deploying-rest-api-based-flask-app-on-heroku-part-1-cb43a14c50c
#################################################################################################################

app = Flask(__name__)
api = Api(app)

# Setting the location for the sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'

# Adding the configurations for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Instantiating sqlalchemy object
db = SQLAlchemy()


class Artists(db.Model):
 
    id     = db.Column(db.String(22), primary_key=True)    
    name   = db.Column(db.String(50), unique=True, nullable=False)                                               
    age    = db.Column(db.Integer, unique=False, nullable=True)
    albums = db.Column(db.String(100), unique=False, nullable=False)
    tracks = db.Column(db.String(100), unique=False, nullable=False)
    self_  = db.Column(db.String(100), unique=False, nullable=False)
    
    def __init__(self, name, age):
        self.id = b64encode(name.encode()).decode('utf-8')[:22]     
        self.name = name
        self.age = age
        self.albums = f"?/artists/{self.id}/albums"
        self.tracks = f"?/artists/{self.id}/tracks"
        self.self_ = f"?/artists/{self.id}"
    
    # Method to show data as dictionary object
    def json(self):
        return {'id': self.id,
                'name': self.name,
                'age': self.age,
                'albums': self.albums,
                'tracks': self.tracks,
                'self': self.self_}
 
    # Method to find the query movie is existing or not
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    # Method to save data to database
    def save_to(self):        
        db.session.add(self)        
        db.session.commit()
    
    # Method to delete data from database
    def delete_(self):        
        db.session.delete(self)        
        db.session.commit()


class Albums(db.Model):

    id        = db.Column(db.String(22), primary_key=True)    
    artist_id = db.Column(db.String(22), unique=True, nullable=False)
    name      = db.Column(db.String(50), unique=False, nullable=False)
    genre     = db.Column(db.String(50), unique=False, nullable=False)
    artist    = db.Column(db.String(100), unique=False, nullable=False)
    tracks    = db.Column(db.String(100), unique=False, nullable=False)
    self_     = db.Column(db.String(100), unique=False, nullable=False)
    
    def __init__(self, artist_id, name, genre):
        self.artist_id = artist_id
        self.id = b64encode((name + ':' + artist_id).encode()).decode('utf-8')[:22]
        self.name = name
        self.genre = genre
        self.artist = f"?/artists/{self.artist_id}"
        self.tracks = f"?/albums/{self.id}/tracks"
        self.self_ = f"?/albums/{self.id}"
    
    # Method to show data as dictionary object
    def json(self):
        return {'id': self.id,
                'artist_id': self.artist_id,
                'name': self.name,
                'genre': self.genre,
                'artist': self.artist,
                'tracks': self.tracks,
                'self': self.self_}   
 
    # Method to find the query movie is existing or not
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_artist_id(cls, artist_id):
        return cls.query.filter_by(artist_id=artist_id)
    
    # Method to save data to database
    def save_to(self):        
        db.session.add(self)        
        db.session.commit()
    
    # Method to delete data from database
    def delete_(self):        
        db.session.delete(self)        
        db.session.commit()


class Tracks(db.Model):
 
    id           = db.Column(db.String(22), primary_key=True)
    artist_id    = db.Column(db.String(22), unique=True, nullable=False)
    album_id     = db.Column(db.String(22), unique=True, nullable=False)
    name         = db.Column(db.String(50), unique=False, nullable=False)
    duration     = db.Column(db.Float, unique=False, nullable=True)
    times_played = db.Column(db.Integer, unique=False, nullable=True)
    artist       = db.Column(db.String(100), unique=False, nullable=False)
    album        = db.Column(db.String(100), unique=False, nullable=False)
    self_        = db.Column(db.String(100), unique=False, nullable=False)
    
    def __init__(self, artist_id, album_id, name, duration):
        self.artist_id = artist_id
        self.album_id = album_id
        self.id = b64encode((name + ':' + album_id).encode()).decode('utf-8')[:22]
        self.name = name
        self.duration = duration
        self.times_played = 0
        self.artist = f"?/artists/{self.artist_id}"
        self.album = f"?/albums/{self.album_id}"
        self.self_ = f"?/tracks/{self.id}"
    
    # Method to show data as dictionary object
    def json(self):
        return {'id': self.id,
                'album_id': self.artist_id,
                'name': self.name,
                'duration': self.duration,
                'times_played': self.times_played,
                'artist': self.artist,
                'album': self.album,
                'self': self.self_}   
 
    # Method to find the query movie is existing or not
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_artist_id(cls, artist_id):
        return cls.query.filter_by(artist_id=artist_id)

    @classmethod
    def find_by_album_id(cls, album_id):
        return cls.query.filter_by(album_id=album_id)
    
    # Method to save data to database
    def save_to(self):        
        db.session.add(self)        
        db.session.commit()
    
    # Method to delete data from database
    def delete_(self):        
        db.session.delete(self)        
        db.session.commit()


# Link the app object to the Movies database 
db.init_app(app)
app.app_context().push()

# Create the databases
db.create_all()


class All_Artists(Resource):

    parser = reqparse.RequestParser()                      
    parser.add_argument('name', type=str, required=False, help='Nombre del Artista')
    parser.add_argument('age', type=str, required=False, help='Edad del Artista')

    def get(self): 
        return list(map(lambda x: x.json(), Artists.query.all())), 200

    def post(self): 

        args = All_Artists.parser.parse_args()
        if not args['name'] or not args['age']:
            return 'input invalido', 400
        id = b64encode(args['name'].encode()).decode('utf-8')[:22]

        item = Artists.find_by_id(id)

        if item:
            return item.json(), 409

        item = Artists(args['name'], args['age'])

        item.save_to()
        return item.json(), 201


class Artists_By_Id(Resource):

    def get(self, artist_id): 
        item = Artists.find_by_id(artist_id)
        if item:
            return item.json(), 200
        return 'artista no encontrado', 404

    def delete(self, artist_id):

        item = Artists.find_by_id(artist_id)

        if not item:
            return 'artista inexistente', 404
        
        tracks = Tracks.find_by_artist_id(artist_id)
        for track in tracks:
            track.delete_()
        
        albums = Albums.find_by_artist_id(artist_id)
        for album in albums:
            album.delete_()
        
        item.delete_()
        return 'artista eliminado', 204


class Artists_Albums(Resource):

    parser = reqparse.RequestParser()                      
    parser.add_argument('name', type=str, required=False, help='Nombre del Album')
    parser.add_argument('genre', type=str, required=False, help='Genero del Album')

    def get(self, artist_id):
        if not Artists.find_by_id(artist_id):
            return 'artista no encontrado', 404
        return list(map(lambda x: x.json(), Albums.find_by_artist_id(artist_id))), 200

    def post(self, artist_id):

        args = Artists_Albums.parser.parse_args()

        if not Artists.find_by_id(artist_id):
            return 'artista no existe', 422
        
        if not args['name'] or not args['genre']:
            return 'input invalido', 400
        
        id = b64encode((args['name'] + ':' + artist_id).encode()).decode('utf-8')[:22]
        if Albums.find_by_id(id):
            return 'album ya existe', 409
        
        item = Albums(artist_id, args['name'], args['genre'])
        
        item.save_to()
        return item.json(), 201


class Artists_Tracks(Resource):

    def get(self, artist_id):
        if not Artists.find_by_id(artist_id):
            return 'artista no encontrado', 404
        return list(map(lambda x: x.json(), Tracks.find_by_artist_id(artist_id))), 200


class Play_Artist(Resource):

    def put(self, artist_id):

        if not Artists.find_by_id(artist_id):
            return 'artista no encontrado', 404
        
        tracks = Tracks.find_by_artist_id(artist_id)
        for track in tracks:
            track.times_played += 1
            track.save_to()

        return 'todas las canciones del artista fueron reproducidas', 200


class All_Albums(Resource):

    def get(self): 
        return list(map(lambda x: x.json(), Albums.query.all())), 200

class Albums_By_Id(Resource):

    def get(self, album_id): 
        item = Albums.find_by_id(album_id)
        if item:
            return item.json(), 200
        return 'album no encontrado', 404

    def delete(self, album_id):

        item = Albums.find_by_id(album_id)

        if not item:
            return 'album no encontrado', 404
        
        tracks = Tracks.find_by_album_id(album_id)
        for track in tracks:
            track.delete_()
        
        item.delete_()
        return 'album eliminado', 204


class Albums_Tracks(Resource):

    parser = reqparse.RequestParser()                      
    parser.add_argument('name', type=str, required=False, help='Nombre de la Cancion')
    parser.add_argument('duration', type=float, required=False, help='Duracion de la Cancion')

    def get(self, album_id):
        if not Albums.find_by_id(album_id):
            return 'album no encontrado', 404
        return list(map(lambda x: x.json(), Tracks.find_by_album_id(album_id))), 200

    def post(self, album_id):

        args = Albums_Tracks.parser.parse_args()

        if not Albums.find_by_id(album_id):
            return 'album no existe', 422
        
        if not args['name']:
            return 'input invalido', 400
        
        id = b64encode((args['name'] + ':' + album_id).encode()).decode('utf-8')[:22]
        if Tracks.find_by_id(id):
            return 'cancion ya existe', 409
        
        artist_id = Albums.find_by_id(album_id).artist_id
        item = Tracks(artist_id, album_id, args['name'], args['duration'])
        
        item.save_to()
        return item.json(), 201


class Play_Album(Resource):

    def put(self, album_id):

        if not Albums.find_by_id(album_id):
            return 'album no encontrado', 404
        
        tracks = Tracks.find_by_album_id(album_id)
        for track in tracks:
            track.times_played += 1
            track.save_to()

        return 'todas las canciones del album fueron reproducidas', 200


class All_Tracks(Resource):

    def get(self): 
        return list(map(lambda x: x.json(), Tracks.query.all())), 200


class Tracks_By_Id(Resource):

    def get(self, track_id): 
        item = Tracks.find_by_id(track_id)
        if item:
            return item.json(), 200
        return 'cancion no encontrada', 404

    def delete(self, track_id):

        item = Tracks.find_by_id(track_id)

        if not item:
            return 'cancion no encontrada', 404
        
        item.delete_()
        return 'cancion eliminada', 204


class Play_Track(Resource):

    def put(self, track_id):

        item = Tracks.find_by_id(track_id)

        if not item:
            return 'cancion no encontrada', 404
        
        item.times_played += 1
        item.save_to()

        return 'cancion reproducida', 200


# Adding the URIs to the api

# Artists
api.add_resource(All_Artists, '/artists')
api.add_resource(Artists_By_Id, '/artists/<string:artist_id>')
api.add_resource(Artists_Albums, '/artists/<string:artist_id>/albums')
api.add_resource(Artists_Tracks, '/artists/<string:artist_id>/tracks')
api.add_resource(Play_Artist, '/artists/<string:artist_id>/albums/play')

# Albums
api.add_resource(All_Albums, '/albums')
api.add_resource(Albums_By_Id, '/albums/<string:album_id>')
api.add_resource(Albums_Tracks, '/albums/<string:album_id>/tracks')
api.add_resource(Play_Album, '/albums/<string:album_id>/tracks/play')

# Tracks
api.add_resource(All_Tracks, '/tracks')
api.add_resource(Tracks_By_Id, '/tracks/<string:track_id>')
api.add_resource(Play_Track, '/tracks/<string:track_id>/play')

@app.route('/')
def index():
    return "<div style='text-align:center; font-family: Arial, Helvetica, sans-serif;'><br><h1>Tarea 2 - Taller de integración</h1><br><br><img src='https://www.killyourdarlings.com.au/wp-content/uploads/2017/04/pusheen4.gif'></div>"

if __name__ == '__main__':
    app.run()
