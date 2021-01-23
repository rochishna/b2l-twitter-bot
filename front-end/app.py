from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
q=[]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#app.secret_key = 'somesecretkeythatonlyishouldknow'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def login():
    o=0
    conn = sqlite3.connect('db.sqlite')
    p= conn.execute("select * from admin")
    p=list(p)
    conn.close()
    for i in range(len(p)):
        q.append(p[i])
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i in range(len(q)):
            if(username==q[i][1] and password==q[i][0]):
                o=1
        if o==1:
            return redirect(url_for('home'))
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/home")
def home():
    users_list = Users.query.all()
    return render_template("admin.html", users_list=users_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_users = Users(title=title)
    db.session.add(new_users)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:users_id>")
def delete(users_id):
    users = Users.query.filter_by(id=users_id).first()
    db.session.delete(users)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
