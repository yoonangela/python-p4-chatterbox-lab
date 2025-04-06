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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method=='GET':
        messages = Message.query.order_by(Message.created_at).all()
        messagelist =[message.to_dict() for message in messages]
        return make_response(messagelist, 200)
    elif request.method=='POST':
        data = request.json
        newMessage = Message(body=data['body'], username=data['username'])
        db.session.add(newMessage)
        db.session.commit()
        return make_response(newMessage.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id==id).first()
    # message = db.session.execute(db.select(Message).filter_by(id=id)).scalar_one()
    if request.method=='PATCH':
        data = request.json
        message.body=data['body']
        db.session.commit()
        return make_response(message.to_dict())
    elif request.method=='DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response('deleted', 204)
    

if __name__ == '__main__':
    app.run(port=5555)
