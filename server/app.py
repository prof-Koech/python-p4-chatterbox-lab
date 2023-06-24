from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = [message.to_dict() for message in Message.query.all()]
        print(messages)
        
        response = make_response(jsonify(messages), 200)
        response.headers["Content-Type"] = 'application/json'

        return response
    
    elif request.method == "POST":
        request_data = request.get_json()

        message = Message(
            username = request_data.get("username"),
            body = request_data.get("body"),
        )

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(message_dict, 201)
        response.headers["Content-Type"] = 'application/json'

        return response

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE", "GET"])
def messages_by_id(id):
    if request.method == "GET":
        message = Message.query.filter_by(id=id).first()

        if message:
            message_dict = message.to_dict()
            
            response = make_response(jsonify(message_dict), 200)

            return response
        
    elif request.method == "PATCH":
        message = Message.query.filter_by(id=id).first()
        
        for attr in request.get_json():
            setattr(message, attr, request.get_json().get(attr))

        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(jsonify(message_dict), 200)

        return response
    
    elif request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()
        
        if message:
            db.session.delete(message)
            db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Baked Good Deleted"
        }

        response = make_response(jsonify(response_body), 200)
        response.headers["Content-Type"] = 'application/json'


        return response

if __name__ == '__main__':
    app.run(port=5555)
