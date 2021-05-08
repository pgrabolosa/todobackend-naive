
### App Model ##################################
import uuid

todos = []


### WSGI app Object ############################
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

### Enable CORS ################################
from flask_cors import CORS
CORS(app)

### Routes #####################################

@app.route('/', methods=['GET'])
def all_items():
  """Returns all the todo items."""

  return jsonify(todos)

@app.route('/', methods=['POST'])
def new_item():
  """Creates a new todo item."""

  item = request.get_json()

  item['id'] = str(uuid.uuid4())
  item['url'] = 'http://127.0.0.1:5000/%s' % (item['id'])

  if 'completed' not in item:
    item['completed'] = False

  todos.append(item)
  return jsonify(item)

@app.route('/', methods=['DELETE'])
def delete_all_items():
  """Removes all the items."""

  todos[:] = []
  return "", 204

@app.route('/<todo_id>', methods=['GET'])
def one_item(todo_id):
  """Returns a single todo item, filtering by ID. If not found, 404."""

  for item in todos:
    if item['id'] == todo_id:
      return jsonify(item)
  return jsonify(error="Not found"), 404

@app.route('/<todo_id>', methods=['PATCH'])
def change_one_item(todo_id):
  """Alters the keys from the todo item identified by its ID."""

  for item in todos:
    if item['id'] == todo_id:

      changes = request.get_json()
      for k in changes:
        item[k] = changes[k]

      return jsonify(item)
  return jsonify(error="Not found"), 404

@app.route('/<todo_id>', methods=['DELETE'])
def remove_one_item(todo_id):
  """Removes a single todo item identified by its ID."""

  for item in todos:
    if item['id'] == todo_id:
      todos.remove(item)
      return "", 204
  return jsonify(error="Not found"), 404


### Run the debug server #######################
if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=80)
