from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')



@api.route('/books', methods = ['POST'])
@token_required
def create_book_data(current_user_token):
    isbn = request.json['isbn']
    author_name = request.json['author_name']
    book_title = request.json['book_title']
    book_length = request.json['book_length']
    hc_pb = request.json['hc_pb']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, author_name, book_title, book_length, hc_pb, user_token=user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_single_book(current_user_token):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.isbn = request.json['isbn']
    book.author_name = request.json['author_name']
    book.book_title = request.json['book_title']
    book.book_length = request.json['book_length']
    book.hc_pb = request.json['hc_pb']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)