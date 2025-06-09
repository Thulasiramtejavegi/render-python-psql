import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Get the DATABASE_URL from Render's environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# Initialize database within app context
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created!")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template("form.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
