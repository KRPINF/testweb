from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Init app
app = Flask(__name__)

#Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:TPPndo33441@node8604-advweb-20.app.ruk-com.cloud:11096/CloudDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:TPPndo33441@10.100.2.200:5432/CloudDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init DB
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

#Staff Class/Model
class Staffs(db.Model):
    id = db.Column(db.String(13), primary_key=True, unique=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(25))
    company = db.Column(db.String(10))
    
    def __init__(self, id, name, type, company):
        self.id = id
        self.name = name
        self.type = type
        self.company = company
        
    # Staff Schema
class StaffSchema(ma.Schema):
    class Meta:
        fields =('id', 'name', 'type', 'company')

# Init Schema 
staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

# Get All Staffs
@app.route('/staffs', methods=['GET'])
def get_staffs():
    all_staffs = Staffs.query.all()
    result = staffs_schema.dump(all_staffs)
    return jsonify(result)

# Get Single Staff
@app.route('/staff/<id>', methods=['GET'])
def get_staff(id):
    staff = Staffs.query.get(id)
    return staff_schema.jsonify(staff)

# Update a Staff
@app.route('/staff/<id>', methods=['PUT'])
def update_staff(id):
    staff = Staffs.query.get(id)
    
    name = request.json['name']
    email = request.json['type']
    phone = request.json['company']

    staff.name = name
    staff.email = email
    staff.phone = phone

    db.session.commit()

    return staff_schema.jsonify(staff)

# Delete Staff
@app.route('/staff/<id>', methods=['DELETE'])
def delete_staff(id):
    staff = Staffs.query.get(id)
    db.session.delete(staff)
    db.session.commit()
    
    return staff_schema.jsonify(staff)

# Web Root Hello
@app.route('/', methods=['GET'])
def get():
    return jsonify({'ms': 'TEST KPOP'})
# Run Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


    
