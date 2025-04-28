from flask import Flask, jsonify, request

app = Flask(__name__)

# Data awal
books = [
    {"id": 1, "Penulis": "JS. Khairen", "Judul Buku": "Bungkam Suara", "Harga": 120000},
    {"id": 2, "Penulis": "Henry Manampiring", "Judul Buku": "Filosofi Teras", "Harga": 60000}
]

# GET semua buku
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# GET 1 buku berdasarkan ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({'error': 'Buku Tidak Ditemukan'}), 404

# POST untuk tambah buku baru
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    new_book['id'] = books[-1]['id'] + 1 if books else 1  # langsung increment ID
    books.append(new_book)
    return jsonify(new_book), 201

# PUT mengupdate buku berdasarkan ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_data = request.get_json()
    for book in books:
        if book['id'] == book_id:
           # Update hanya field yang dikirim
            if 'Judul Buku' in updated_data:
                book['Judul Buku'] = updated_data['Judul Buku']
            if 'Penulis' in updated_data:
                book['Penulis'] = updated_data['Penulis']
            if 'Harga' in updated_data:
                book['Harga'] = updated_data['Harga']
            return jsonify(book), 200
    return jsonify({'error': 'Buku Tidak Ditemukan'}), 404

# DELETE hapus buku berdasarkan ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for index, book in enumerate(books):
        if book['id'] == book_id:
            deleted_book = books.pop(index)
            return jsonify(deleted_book), 200
    return jsonify({'error': 'Buku Tidak Ditemukan'}), 404

if __name__ == '__main__':
    app.run(debug=True)
