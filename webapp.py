#!/usr/bin/python
# Webapp and main program for the facial access control system

# Program to run a network-exposed webserver on the Raspberry Pi: 'flask run --host=0.0.0.0'
# Credit to Eduardo Cuducos for the flask_simplelogin library and flask code example

from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required
from flask import Response, Flask, render_template

app = Flask(__name__)

my_users = {
    "person1": {"password": "password1", "roles": ["admin"]},
    "person2": {"password": "password2", "roles": ["admin"]},
    "person3": {"password": "password3", "roles": ["admin"]},
}

# Check if the given user exists in the my_users array and if the provided password matches the stored password.
def check_my_users(user):
    user_data = my_users.get(user["username"])
    if not user_data:
        return False
    elif user_data.get("password") == user["password"]:
        return True
    return False

simple_login = SimpleLogin(app, login_checker=check_my_users)

# Direct people to index.html at root of site
@app.route("/")
def index():
    return render_template("index.html")

# Direct people to the secret.html page at the /webapp url path
@app.route("/webapp")
@login_required(username=["user", "pass"])
def secret():
    return render_template("secret.html")


# Create an access point at /api that accepts POST requests
@app.route("/api", methods=["POST"])
@login_required(basic=True)
def api():
    return jsonify(data="You are logged in with basic auth")

# Check if user has admin privileges. (This is not necessary for our program but is useful for heirarchal access control)
def be_admin(username):
    user_data = my_users.get(username)
    if not user_data or "admin" not in user_data.get("roles", []):
        return "User does not have admin role"

def have_approval(username):
    return

@app.route("/complex")
@login_required(must=[be_admin, have_approval])
def complexview():
    return render_template("secret.html")

class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())

app.add_url_rule("/protected", view_func=ProtectedView.as_view("protected"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=True, debug=True)
