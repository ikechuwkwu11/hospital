from flask import Flask,jsonify,request
from flask_login import LoginManager,login_user,logout_user,current_user
from flask_mail import Mail, Message
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from models import db,User,Hospital,BookAppointment,DoctorReview


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['UPLOAD_FOLDER'] = 'uploads'


db.init_app(app)

login_manager= LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/register',methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return jsonify({'message':'Please register properly'}),400

        new_user = User(username=username,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful. A confirmation email has been sent."}), 200
    except Exception as e:
                return jsonify({"message": "Registration successful, but there was an error sending the email.",'error':str(e)}), 500

@app.route('/api/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'message': 'incorrect details. Please try again!!'}),400

        user = User.query.filter_by(username=username).first()
        if user.password == password:
            login_user(user)
            db.session.commit()
            return jsonify({'message':'You have successfully logged in'}),200
    except Exception as e:
        jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/logout',methods=['GET'])
def logout():
    login_user()
    return jsonify({'message':'You have been logged out'})

@app.route('/api/add_hospital',methods=['POST'])
def add_hospital():
    try:
        data = request.get_json()
        name = data.get('name')
        location = data.get('location')
        specialized = data.get('specialized')
        doctor = data.get('doctor')

        if not name or not location or not specialized or not doctor:
            return jsonify({'message':'Please fill in all spaces'}),400

        new_user= Hospital(name = name,location=location, specialized=specialized,doctor=doctor)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'You have successfully added the hospital'}),200
    except Exception as e:
        return jsonify({'message':'internal sever error','error':str(e)}),500

@app.route('/api/hospital',methods=['GET'])
def hospital():
    try:
        hospital_all = Hospital.query.all()
        hospital_list =[
            {
                "id":h.id,
                "name":h.name,
                "location":h.location,
                "specialized":h.specialized,
                "doctor":h.doctor
            }
            for h in hospital_all
        ]

        return jsonify({'hospital':hospital_list}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500


@app.route('/api/image',methods=['POST'])
def image():
    try:
        if 'image' not in request.files:
            return jsonify({'message':'image not in file'}),400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'message':'file not found'}),400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        return jsonify({'message':'image has been uploaded','filename':filename}),200
    except Exception as e:
        return jsonify({'message':'internal sever error','error':str(e)}),500

@app.route('/api/book_appointment',methods=['GET'])
def book_appointment():
    try:
        book_appointment= BookAppointment.query.all()
        booking_list =[
            {
                'id':b.id,
                'name':b.name,
                'hospital_id':b.hospital_id,
                'start_time':b.start_time,
                'end_time':b.end_time
            }
            for b in book_appointment
        ]
        return jsonify({'book_appointment':booking_list})
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/single_book_appointment/<int:appointment_id>',methods=['GET'])
def single_book_appointment(appointment_id):
    try:
        appointment= BookAppointment.query.get_or_404(appointment_id)

        appointment_data = {
            'id': appointment.id,
            'name': appointment.name,
            'hospital_id': appointment.hospital_id,
            'start_time': appointment.start_time.isoformat(),  # convert datetime to string
            'end_time': appointment.end_time.isoformat()
        }
        return jsonify({'appointment':appointment_data}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/add_booking',methods=['POST'])
def add_booking():
    try:
        data = request.get_json()
        name = data.get('name')
        hospital_id = data.get('hospital_id')
        start_time = datetime.fromisoformat(data.get('start_time'))
        end_time= datetime.fromisoformat(data.get('end_time'))
        if not name or not hospital_id or not start_time or not end_time:
            return jsonify({'message':'please fill in all'})

        new_user = BookAppointment(name=name,hospital_id=hospital_id,start_time=start_time,end_time=end_time)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'You have successfully booked'})
    except Exception as e:
        return jsonify({'message':'internal sever error','error':str(e)}),500

@app.route('/api/edit_book_appointment/<int:booking_id>',methods=['PUT'])
def edit_book_appointment(booking_id):
    try:
        appointment = BookAppointment.query.get_or_404(booking_id)
        data = request.get_json()
        appointment.name = data.get('name',appointment.name)
        appointment.hospital_id = data.get('hospital_id',appointment.hospital_id)
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time:
            appointment.start_time = datetime.strptime(start_time, "%a, %d %b %Y %H:%M:%S %Z")
        if end_time:
            appointment.end_time = datetime.strptime(end_time, "%a, %d %b %Y %H:%M:%S %Z")
        db.session.commit()
        return jsonify({'message':'Your booking session has been edited'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500



@app.route('/api/delete_book_appointment/<int:booking_id>',methods=['DELETE'])
def delete_book_appointment(booking_id):
    try:
        user = BookAppointment.query.get_or_404(booking_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'This user has been deleted'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500


@app.route('/api/add_doctor_review',methods=['POST'])
def add_doctor_review():
    try:
        data = request.get_json()
        name = data.get('name')
        review = data.get('review')
        drugs = data.get('drugs')
        injections = data.get('injections')
        if not name or not review or not drugs or not injections:
            return jsonify({'message':'Please fill in all'}),400

        new_user = DoctorReview(name=name,review=review,drugs=drugs,injections=injections)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'Your report has been added, Thank you!!'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/image_drug',methods=['POST'])
def image_drug():
    try:
        if 'image' not in request.files:
            return jsonify({'message':'file not in image'}),400

        file = request.files['image']
        if file.filename =='':
            return jsonify({'message':'file not found'}),400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        return jsonify({'message':'Image has been uploaded'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/all_doctor_review',methods=['GET'])
def all_doctor_review():
    try:
        review = DoctorReview.query.all()
        review_list = [
            {
                "id" : r.id,
                "name":r.name,
                "review":r.review,
                "drugs": r.drugs,
                "injections":r.injections
            }
            for r in review
        ]
        return jsonify({'review':review_list})
    except Exception as e:
        return jsonify({'message':'internal server error', 'error':str(e)}),500


@app.route('/api/single_review/<int:review_id>',methods=['GET'])
def single_review(review_id):
    try:
        review = DoctorReview.query.get_or_404(review_id)

        review_data = {
            "id":review.id,
            "name":review.name,
            "review":review.review,
            "drugs":review.drugs,
            "injections":review.injections
        }
        return jsonify({'review':review_data}),200


    except Exception as e:
        return jsonify({'message':'internal sever error','error':str(e)}),500


@app.route('/api/edit_review/<int:review_id>',methods=['PUT'])
def edit_review(review_id):
    try:
        review = DoctorReview.query.get_or_404(review_id)
        data = request.get_json()
        review.name = data.get('name',review.name)
        review.review = data.get('review',review.review)
        review.drugs = data.get('review',review.drugs)
        review.injections = data.get('injections',review.injections)
        db.session.commit()
        return jsonify({'message':'You data has been edited'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/delete_review/<int:review_id>',methods=['DELETE'])
def delete_review(review_id):
    try:
        user = DoctorReview.query.get_or_404(review_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'You deleted your review'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500


if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
