from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Model database
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return{"id": self.id, "name": self.name}
    
# MEMBUAT TABEL
with app.app_context():
    db.create_all()

# CREATE
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created", "item": new_item.to_dict()}), 201

# READ ALL
@app.route('/items', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

# READ by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.to_dict()), 200
    return jsonify({"error": "Item not found"}), 404

# UPDATE
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    
    item.name = data['name']
    db.session.commit()
    return jsonify({"message": "Item updated", "item": item.to_dict()}), 200

# DELETE
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Item with ID {item_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
# s