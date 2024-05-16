from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from models import db, User, Ticket, Movie,Session
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SECRET_KEY'] = 'eleonora'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SQLALCHEMY_ECHO = True
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/signup", methods=["POST"])
def signup():
    email = request.json["email"]
    password = request.json["password"]
    role = request.json["role"]

    print(f"Перевірка наявності користувача з електронною адресою: {email}")
    user_exists = User.query.filter_by(email=email).first() is not None
    print(f"Користувач існує: {user_exists}")

    if user_exists:
        return 'Email already exists', 401

    # hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=password, role=role )
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401

    if not user.password == password:
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'}), 200

@app.route('/listusers', methods=['GET'])
def listusers():
    all_users = User.query.all()
    users_list = [
        {"id": user.id, "email": user.email, "password": user.password, "role": user.role}
        for user in all_users
    ]
    return jsonify(users_list)

@app.route('/userdetails/<id>', methods=['GET'])
def userdetails(id):
    user = User.query.get(id)
    if user:
        user_data = {"id": user.id, "email": user.email, "password": user.password, "role": user.role}
        return jsonify(user_data)
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/userupdate/<id>', methods=['PUT'])
def userupdate(id):
    user = User.query.get(id)
    if user:
        user.email = request.json.get('email', user.email)
        user.password = request.json.get('password', user.password)
        user.role = request.json.get('role', user.role)
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/userdelete/<id>', methods=['DELETE'])
def userdelete(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/useradd', methods=['POST'])
def useradd():
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']
    user = User(email=email, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added successfully"}), 201

@app.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Session.query.all()
    return jsonify([{'id': session.id, 'movie_id': session.movie_id, 'start_time': session.start_time, 'end_time': session.end_time, 'price': str(session.price)} for session in sessions])

@app.route('/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first_or_404()
    return jsonify({'title': movie.title, 'director': movie.director, 'photo': movie.photo, 'summary': movie.summary})

@app.route('/buy_ticket/<session_id>', methods=['POST'])
def buy_ticket(session_id):
    user_id = request.form.get('user_id')
    seat_number = request.form.get('seat_number')
    ticket = Ticket(session_id=session_id, user_id=user_id, seat_number=seat_number)
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'ticket_id': ticket.id}), 201

@app.route('/return_ticket/<ticket_id>', methods=['DELETE'])
def return_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first_or_404()
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket returned successfully'}), 200
if __name__ == "__main__":
    app.run(debug=True)