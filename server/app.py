#!/usr/bin/env python3

from flask import Flask,session, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():


    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
             "id": bakery.id,
              "name": bakery.name,
              "created_at" : bakery.created_at,
              "updated_at" : bakery.updated_at,
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers["content-Type"] = "application/json"
    return response


@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery:
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
        }

        response = make_response(jsonify(bakery_dict), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    goods_by_price = []
    for goods in baked_goods:
        goods_dict = {
            "id": goods.id,
            "name": goods.name,
            "price": goods.price,
            "bakery_id": goods.bakery_id,
            "created_at" : goods.created_at,
        }
        goods_by_price.append(goods_dict)

    response = make_response(
        jsonify(goods_by_price),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive_good:
        goods_dict = {
            "id": most_expensive_good.id,
            "name": most_expensive_good.name,
            "price": most_expensive_good.price,
            "bakery_id": most_expensive_good.bakery_id,
            "created_at":most_expensive_good.created_at,
        }

        response = make_response(
            jsonify(goods_dict),
            200
        )
        response.headers["content-Type"] = "application/json"
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
