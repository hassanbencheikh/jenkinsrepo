# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key-123'
@app.route('/add', methods=['GET'])
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide 'a' and 'b' parameters."}), 400
    return jsonify({"result": a + b})

@app.route('/subtract', methods=['GET'])
def subtract():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide 'a' and 'b' parameters."}), 400
    return jsonify({"result": a - b})

@app.route('/multiply', methods=['GET'])
def multiply():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide 'a' and 'b' parameters."}), 400
    return jsonify({"result": a * b})

@app.route('/divide', methods=['GET'])
def divide():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide 'a' and 'b' parameters."}), 400
    if b == 0:
        return jsonify({"error": "Division by zero is not allowed."}), 400
    return jsonify({"result": a / b})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
