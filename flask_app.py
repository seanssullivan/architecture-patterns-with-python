# Third-Party Imports
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Imports
import config
import model
import orm
import repository

orm.start_mapper()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
  session = get_session()
  batches = repository.SqlAlchemyRepository(session).list()
  line = model.OrderLine(
    request.json['orderid'],
    request.json['sku'],
    request.json['qty'],
  )

  batchref = model.allocate(line, batches)

  return jsonify({'batchref': batchref}), 201
