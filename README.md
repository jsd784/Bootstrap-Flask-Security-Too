# 🔐 Flask Security with Bootstrap Integration

A secure and extensible Flask web application using [Flask-Security-Too](https://flask-security-too.readthedocs.io/en/stable/) for user authentication, role-based authorization, and email-based registration and password recovery.

This project includes:
- User and role models backed by SQLAlchemy
- Custom registration form
- Email support for registration and password reset
- Trackable user activity
- Role-based access control (`@roles_required`)
- Login-protected views (`@auth_required`)
- Configurable with environment variables

---

## 🚀 Features

- ✉️ **Registration and password recovery** via email (SendGrid)
- 🔑 **Role-based access** using decorators
- 📬 **SMTP email setup** with `flask-mail`
- 🔒 **Password hashing and salt**
- 📊 **User login tracking**: IPs, login timestamps, and count
- 🧱 **SQLite DB schema** with normalized role/user tables
- 📃 **Custom Registration Form** (`ExtendedRegisterForm` from `customforms.py`)

---

## 📁 Project Structure

```bash
.
├── app.py                     # Main application
├── customforms.py             # Custom registration form (must be created)
├── templates/
│   ├── index.html             # Default authenticated page
│   └── protected.html         # Admin-only page
├── data/
│   └── test.db                # SQLite database (auto-created)
````

---

## ⚙️ Setup Instructions

### 1. Install Requirements

```bash
pip install Flask Flask-SQLAlchemy Flask-Mail Flask-Security-Too
```

> Optionally install `python-dotenv` to load environment variables from `.env`.

### 2. Set Environment Variables

```bash
export AZURE_MAIL_USER='apikey'  # or your SendGrid username
export AZURE_MAIL_PASS='your-sendgrid-api-key'
export SECRET_KEY='your-random-secret-key'
export SECURITY_PASSWORD_SALT='your-random-salt'
```

### 3. Run the App

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🔐 User & Role Management

* The app uses `User` and `Role` models with a join table `app_roles_users`
* You can pre-create an admin user using the commented `@before_first_request` block

---

## 🧪 Access Control Demo

| Endpoint     | Protection Type            | Description           |
| ------------ | -------------------------- | --------------------- |
| `/`          | `@auth_required()`         | Requires login        |
| `/protected` | `@roles_required('admin')` | Requires 'admin' role |

---

## 📬 Email Settings (SendGrid Example)

```python
app.config['MAIL_SERVER'] = "smtp.sendgrid.net"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get("AZURE_MAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("AZURE_MAIL_PASS")
app.config['MAIL_DEFAULT_SENDER'] = "no-reply@yourdomain.com"
```

---

## 🧱 Database Tables

* `app_user`: Stores user data
* `app_role`: Stores roles
* `app_roles_users`: Many-to-many relationship between users and roles

---

## 📌 Notes

* Email confirmation, change password, and trackable login activity are enabled
* All views use Jinja templates with Bootstrap (not included—add your own layout)
* Customize `customforms.py` to extend user registration fields

---

## 📜 License

MIT License

---

## 🙌 Acknowledgements

* [Flask-Security-Too](https://flask-security-too.readthedocs.io/en/stable/)
* [SendGrid](https://sendgrid.com/) for email delivery
* [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
