pip install flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    page_count = db.Column(db.Integer)
    average_rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Book {self.title}>"