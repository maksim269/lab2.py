from flask import Flask,Response,url_for, render_template, redirect, request, session, abort
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin

app = Flask("page")
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY']='43532525_secret_key'

from flask import Flask, url_for, render_template, redirect
from flask_wtf import *
from wtforms import  StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

NUM_USER = 0
Users=[]
usersInfo=[]
class User(UserMixin):
    def __init__(self,id):
        self.id = id
    def set_info(self, name, password):
        self.name = name
        self.password = password
    def __str__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)
    def get_info(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

@login_manager.user_loader
def  load_user(userid):
    return User(userid)

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')

@app.route('/')
@app.route('/index/')
def index():
    user="User"
    title="Home page"
    return render_template('index.html',title=title, username=user)

@app.route('/main/')
@login_required
def main():
    result=""
    for i in range(0,len(Users)):
        result += Users[i].get_info()+'\n'
    return render_template('main.html',result=result)
@app.route("/login/",methods=["GET", "POST"])
def login():
    global NUM_USER
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        for i in range (0,len(Users)):
            current = "%d/%s/%s" % (i, username, password)
            if(Users[i].get_info()==current):

                login_user(Users[i])
                return redirect("/main/")
        return redirect("/login/")

    else:
        logout_user()
        return render_template("login.html", form = form, )

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out </p>')
@app.route("/registration/", methods=["GET", "POST"])
def registration():
    logout_user()
    global NUM_USER
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(NUM_USER)
        user.set_info(username,password)
        Users.append(user)
        login_user(user)
        NUM_USER += 1
        return redirect("/main/")
    else:
        logout_user()
        return render_template("Registration.html", form = form)

app.run(port=8088, host='127.0.0.1')