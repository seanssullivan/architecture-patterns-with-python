# Standard Imports
from datetime import datetime

# Third-Party Imports
from flask import Flask, jsonify, request

# Local Imports
from domain import model
from adapters import orm, repository
from service_layer import services, unit_of_work

app = Flask(__name__)
orm.start_mappers()


@app.route("/add_batch", methods=['POST'])
def add_batch():
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json['ref'], request.json['sku'], request.json['qty'], eta,
        unit_of_work.SqlAlchemyUnitOfWork()
    )
    return 'OK', 201


@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    try:
        batchref = services.allocate(
            request.json['orderid'],
            request.json['sku'],
            request.json['qty'],
            unit_of_work.SqlAlchemyUnitOfWork()
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'batchref': batchref}), 201
