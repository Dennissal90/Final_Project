from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    page_count = db.Column(db.Integer)
    average_rating = db.Column(db.Float)

    def __repr__(self):
        return f'<Book {self.title}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        isbn = request.form['isbn']
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url)
        data = response.json()
        if 'items' in data:
            book_info = data['items'][0]['volumeInfo']
            title = book_info.get('title', 'No Title Available')
            authors = book_info.get('authors', ['No Author Available'])[0]
            page_count = book_info.get('pageCount', 0)
            average_rating = book_info.get('averageRating', 0.0)
            new_book = Book(isbn=isbn, title=title, author=authors, page_count=page_count, average_rating=average_rating)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "No book found with that ISBN."
    return render_template('search.html')

@app.route('/delete/<int:book_id>', methods=['GET'])
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
