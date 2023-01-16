from flask import Flask, jsonify, request
from flask_cors import CORS
import difflib


app = Flask(__name__)
CORS(app)

class Product:
    def __init__(self, name, price, category, image, keywords):
        self.name = name
        self.price = price
        self.category = category
        self.image = image
        self.keywords = keywords

products = [
    Product("Soap Dispenser", 16.90, "Kitchen", "rock.png" ,["kitchen", "soap", "cleaning", "kitchen gadget"]),
    Product("Expandable Food Container", 5, "Kitchen", "rock.png" ,["expandable food container", "expandable", "kitchen", "food", "organize", "container", "storage"]),
    Product("Outlet timer", 18.50, "Electronics", "rock.png" ,["electronics", "outlet timer", "tech", "gadget", "time"]),
    Product("Banana", 1, "Food", "rock.png", ["food", "banana", "yellow", "fruit"])
]
@app.route('/all', methods=['GET'])
def get_all_products():
    return jsonify([{'name': product.name, 'price': product.price, 'category': product.category, 'image': product.image} for product in products])

@app.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()
    keyword = data.get('keyword')
    results = []
    try:
        float(keyword)
        go = True
        keyword = float(keyword)
    except Exception:
        go = False
        pass
    if go == True:
        for product in products:
            if abs(int(keyword) - product.price) <= product.price*0.1:
                results.append({'name': product.name, 'price': product.price, 'category': product.category})
    else:
        product_matches = []
        for product in products:
            product_matches.extend([product.name] + product.keywords)
        close_matches = difflib.get_close_matches(keyword, product_matches, n=1, cutoff=0.6)
        if close_matches:
            for product in products:
                if close_matches[0] in [product.name] + product.keywords:
                    results.append({'name': product.name, 'price': product.price, 'category': product.category})
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
