from flask import Flask, render_template, request, jsonify

app=Flask(__name__)

# demo dataset

data=[
    {'id':1,'name':'item 1','price':10},
    {'id':2,'name':'item 2','price':15}
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/items',methods=['GET'])
def get_items():
    return jsonify(data),200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item=next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item),200
    return jsonify({'message':'ITEM Not found'}),404

@app.route('/api/items',methods=['POST'])
def create_item():
    new_item= request.json
    new_item['id']= len(data)+ 1
    data.append(new_item)
    return jsonify(new_item),201

@app.route('/api/items//<int:item_id>', methods = ['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        updates= request.json
        item.update(updates)
        return jsonify(item),200
    return jsonify({'message': 'Item not found'}),404


@app.route('/api/items/<int:item_id>', methods = ['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id']!= item_id]
    return jsonify ({'message':"Item deleted successfully!"}),200


app.run(debug=True)
