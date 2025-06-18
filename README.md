# 🏥 Flask Hospital Management API
A simple yet powerful RESTful API built with Flask to manage core hospital operations. This backend service supports user authentication, hospital and appointment management, doctor reviews, and secure image uploads.

## 🚀 Features
👤 User Authentication
- Register and log in with secure session handling

🏨 Hospital Management
- Add and view hospitals via API endpoints

📅 Appointment Booking
- Book, view, and manage appointments

🩺 Doctor Reviews
- Add, edit, and delete reviews for doctors

🖼️ Image Upload Support
- Upload images (e.g., medical reports, drugs)
- Secure file handling with Werkzeug

🔗 RESTful Endpoints
- Consistent, scalable API design

## 🧱 Tech Stack
| Component        | Technology          |
| ---------------- | ------------------- |
| Backend          | Python (Flask)      |
| Database         | SQLite + SQLAlchemy |
| Authentication   | Flask-Login         |
| File Uploads     | Werkzeug            |
| Email (optional) | Flask-Mail          |


## 🔐 Authentication
- Login sessions are handled using Flask-Login

- Protects endpoints like booking appointments or posting reviews

## 📬 API Usage
- Test endpoints with tools like:
- Postman
- curl
- httpie

## 🧠 Future Enhancements
- Email notifications via Flask-Mail
- Admin dashboard for managing doctors and hospitals
- Analytics for appointments and reviews
- Role-based access control (RBAC)
