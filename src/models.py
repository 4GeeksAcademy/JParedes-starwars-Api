from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(250))
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(25))
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Planet, self).__init__(**kwargs)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description" : self.description,
            "population" : self.population,
            "terrain" : self.terrain,
            "diameter" : self.diameter,
            "orbital_period" : self.orbital_period

            # do not serialize the password, its a security breach
        }
    
    def to_dict(self):
        return self.serialize()
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250))
    species = db.Column(db.String(250)) 
    height = db.Column(db.String(250))
    mass = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    hair_Color = db.Column(db.String(250))
    skin_Color = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    

    def __init__(self, **kwargs):
        super(People, self).__init__(**kwargs)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year" : self.birth_year,
            "species" : self.species,
            "height" : self.height,
            "mass" : self.mass,
            "gender" : self.gender,
            "hair_Color" : self.hair_Color,
            "skin_Color" : self.skin_Color,
            "homeworld" : self.homeworld
            # do not serialize the password, its a security breach
        }

    def to_dict(self):
        return self.serialize()
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), unique=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            "user": self.user
        }