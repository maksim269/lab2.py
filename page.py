from flask import Flask, url_for, render_template, redirect
from flask_wtf import *
from wtforms import  StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
app = Flask("page")




@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template("login.html", form=form)


app.run(port="8088", host='127.0.0.1')

