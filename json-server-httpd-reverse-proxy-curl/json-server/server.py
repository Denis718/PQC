from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert

# jwt post-quantum
from jwtpostquantum.jwt import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:1234@172.18.2.2:5432/db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # def __repr__(self) -> str:
    #     return f'"id": {self.id}, "username": {self.username} {}'
        
class Product(db.Model):    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


def initial_data():
    
    with open('db.json') as file:
        file_json = json.load(file)

        for data in file_json['produtos']:
            db.session.add(Product(
                name=data['nome'],
                description=data['descricao'],
                price=data['preco']
            ))
    
    db.session.commit()

@app.route('/register', methods=['POST'])
def register():

    if request.method == "POST":
        user = User(
            username=request.json.get('username'),
            password=request.json.get('password'),
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created'})
    
    return jsonify({'message': 'Error creating user'})

@app.route("/users", methods=['GET'])
def user_list():

    if request.method == 'GET':

        users = db.session.execute(db.select(User)).scalars()

        user_list = [{
            'id':u.id,
            'username':u.username,
            'password':u.password
            } for u in users.all()]

        return jsonify({'user_list': user_list})
        
    return jsonify({'message':'Method Not Allowed'})

@app.route('/login', methods=['POST'])
def login():
 
    if request.method == 'POST':

        user = db.session.execute(db.select(User).where(User.username == request.json.get('username'))).scalar()
        
        if user and request.json.get('password') == user.password:
            token = jwt.generate_token('Dilithium3', {'id':1, 'username':'henrique'})
            # return jsonify({"token": token})
            return token
        
        return jsonify({'message': 'User not found'})
    
    return jsonify({'message':'Method Not Allowed'})

@app.route('/products', methods=['GET'])
def product_list():
    
    if request.method == 'GET':
        try:
            if not request.headers['Authorization']:
                return jsonify({'message': 'Token not found'})
         
            bearer_token = request.headers['Authorization'].split(' ')

            if bearer_token[0] != 'Bearer': 
                return jsonify({'message': 'Token not found'})
               
            is_valid = jwt.verify_token('Dilithium3', bearer_token[1])
               
            if not is_valid:
                return jsonify({'message': 'Invalid Token'})

            products = db.session.execute(db.select(Product)).scalars()

            product_list = [{
                'id': p.id, 
                'name': p.name, 
                'description': p.description,
                'price': p.price
                } for p in products.all()]
            
            return jsonify({'product_list': product_list})

        except:
            return jsonify({'message': 'Error'})

    return jsonify({'message':'Method Not Allowed'})

            
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initial_data()

    app.run(debug=True, host='0.0.0.0')



   