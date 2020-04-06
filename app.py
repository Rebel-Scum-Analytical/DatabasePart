# Dependencies
import os
import sqlalchemy
from flask import Flask, render_template, jsonify, request, make_response, session, abort, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pymysql
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextField, PasswordField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, EqualTo
# from passlib.hash import sha256_crypt
import datetime as dt
from Query_Visual import createJson, creatUserPersonalJson, creatplotdata
import json
import plotly
import plotly.graph_objects as go



#################################################
# Flask Setup
#################################################

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'usda'

# Intialize MySQL
# mysql = MySQL(app)

#################################################
# Set up the database
#################################################
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "uv9y9g5t"
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "usda"

# Connect to DB in DB Server
db_connection_string = (
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
)

#FOLLOWING CODE IS FOR HEROKU######
# #################################################
# # Database Setup
# #################################################

# # The database URI
###################################################

app.config['SQLALCHEMY_DATABASE_URI'] = (
     os.environ.get("JAWSDB_URL","") or db_connection_string
 )
db = SQLAlchemy(app)

class Meal_record(db.Model):
    __tablename__ = "meal_record"

    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(50))
    type = db.Column(db.String(50))
    meal_date = db.Column(db.String(15))
    meal_item_code = db.Column(db.Integer)
    meal_desc = db.Column(db.String(256))    
    amount = db.Column(db.Float)

    def __repr__(self):
        return "<Meal_record %r>" % (self.name)

class User_account(db.Model):
    __tablename__ = "user_account"

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    confirm_password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    physical_activity_level = db.Column(db.String(50))

    def __repr__(self):
        return "<User_account %r>" % (self.name)


@app.before_first_request
def setup():
    db.create_all()

#ABOVE CODE IS FOR HEROKU######
###################################################

#commented as using a different method for Heroku
engine = create_engine(db_connection_string)
inspector = inspect(engine)
table_names = inspector.get_table_names()
# print("Table names are: ", table_names)

# commented as using a different method for Heroku
Base = automap_base()
Base.prepare(db.engine, reflect=True)
# print(Base.classes.values)

# create classes by mapping with names which match the table names
User_account = Base.classes.user_account
Meal_record = Base.classes.meal_record
Nutrition = Base.classes.nutrition

# # commented as using a different method for Heroku
# session_db = Session(bind=engine)
# print("session_db is: ", session_db)






#############################################################################################
# Route #1("/")
# Home Page
#############################################################################################
@app.route("/index.html")
@app.route("/")
def main():
    session['page']=' '
    if(checkLoggedIn() == True):
        session['page']='dashboard'
        return redirect('/dashboard')

    session['page']=' '
    return render_template("index.html")
#############################################################################################
# Route #2(/login)
# Design a query for the existing user to login
#############################################################################################
    
@app.route('/login', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    msg = ''
    print("Start of stuff")
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST': #and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        request_username = request.form['username']
        request_password = request.form['password']
        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user_accounts WHERE username = %s AND password = %s', (username, password))
        if request_username and request_password:   
        # Fetch one record and return result
            print("request_username: "+request_username+" | request_password: "+request_password)
            account = loginsys(request_username, request_password)
                # If account exists in accounts table in out database
            if account:
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['username'] = account[3]
            # Redirect to home page
                session['page']='dashboard'
                return redirect('/dashboard')
            else:
            # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
    session['page']=' '
    return render_template('index.html', msg=msg)
    
def loginsys(username, password):
    print("Username: "+username+" Password: "+password)
    user_ls = db.session.query(User_account.first_name, User_account.last_name, User_account.gender, User_account.username)\
                        .filter(User_account.username == username)\
                        .filter(User_account.password == password)\
                        .first()           
    print("user_ls: " + str(user_ls))                 
    return user_ls


##############################################################################################
# Route #3(/register)
# Design a query for the register a new user
#############################################################################################

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired()])
    confirm_password = PasswordField('confirm_password', validators=[InputRequired(), EqualTo('password')])
    first_name = StringField('first_name', validators=[InputRequired(),Length(min=2, max=50)])
    last_name = StringField('last_name', validators=[InputRequired(),Length(min=2, max=50)])
    gender = SelectField(u'gender', choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = DateField('date_of_birth', format='%Y-%m-%d')
    height = DecimalField('height', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=0, max=500, message='Blah')])
    weight = DecimalField('weight', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=0, max=2000, message='Blah')])
    physical_activity_level = SelectField(u'physical_activity_level', choices=[('sedentary', 'Sedentary'), ('lightly active', 'Lightly Active'), ('moderately active', 'Moderately Active'), ('very active', 'Very Active'), ('extra active', 'Extra Active')])  
    submit = SubmitField('Get Started')

@app.route("/register", methods=["GET", "POST"])
def register():

        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')

            new_user = User_account(username = form.username.data,\
                                    password = form.password.data,\
                                    confirm_password = form.confirm_password.data,\
                                    first_name = form.first_name.data,\
                                    last_name = form.last_name.data,\
                                    gender =  form.gender.data,\
                                    date_of_birth = form.date_of_birth.data,\
                                    height = form.height.data,\
                                    weight = form.weight.data,\
                                    physical_activity_level = form.physical_activity_level.data
                                    )
            db.session.add(new_user)
            db.session.commit()

            return redirect('/dashboard')
        return render_template("New_user.html", form=form)


##############################################################################################
# Route #4(/home)
# This will be the home page, only accessible for loggedin users
#############################################################################################

class AddMeal(FlaskForm):
    inputdate = DateField('inputdate', format='%Y-%m-%d')
    meal_category = StringField(u'meal_category', validators=[InputRequired()]) 
    food_desc = StringField('food_desc', validators=[InputRequired()])
    servings_count = DecimalField('servings_count', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=0, max=20)])
    foodNameId = DecimalField('foodNameId')
    submit = SubmitField('Add')
# Code to display daily statistics on dashboard
# daily_goal_list = [1800, 130, 25, 2200, 25, 25.2]

@app.route('/dashboard',methods=["GET", "POST"])
def dashboard():
    if(checkLoggedIn() == False):
        return redirect('/login')

    session['page']='dashboard'

    # Code to display daily statistics on dashboard
    
    daily_goal_list = [1800, 130, 25, 2200, 25, 25.2]
    form = AddMeal(request.form)
    if form.validate_on_submit():
        # flash(f'Meal Added for {form.meal_category.data}!', 'successfully')

        new_meal = Meal_record(username = session['username'],\
                                    meal_date = form.inputdate.data,\
                                    type = form.meal_category.data,\
                                    meal_desc = form.food_desc.data,\
                                    amount = form.servings_count.data,\
                                    meal_item_code = form.foodNameId.data
                                    )
        db.session.add(new_meal)
        db.session.commit()
        
        print("Adding meal")
        return redirect("/dashboard")

    cmd = db.session.query(func.sum(Nutrition.Energy).label('cal'), func.sum(Nutrition.Carbohydrate).label('carbs'),\
                                func.sum(Nutrition.Lipid_Total).label('fats'), func.sum(Nutrition.Sodium).label('sodium'),\
                                func.sum(Nutrition.Sugar_Total).label('sugar'), func.sum(Nutrition.Fiber).label('fiber'),\
                                func.count().label('cnt')).\
                                filter(Meal_record.username == session['username']).\
                                filter(Meal_record.meal_item_code == Nutrition.NDB_No).\
                                filter(Meal_record.meal_date == dt.date.today())
    daily_stats = cmd.first()                            
    results = [daily_stats.cal, daily_stats.carbs, daily_stats.fats, daily_stats.sodium, daily_stats.sugar, daily_stats.fiber]                                  
    print("daily stats are: ", daily_stats)
    print("daily stats cnt: ",daily_stats.cnt)
   

    return render_template("dashboard.html", form=form, results = results, daily_goal_list = daily_goal_list)



# @app.route('/analysis')
# def analysis():
#     if(checkLoggedIn() == False):
#         return redirect('/login')
#     session['page']='analysis'
#     return render_template("Daily_vizualization_new.html")

@app.route('/analysis')
def analysis():
    if(checkLoggedIn() == False):
         return redirect('/login')
    session['page']='analysis'
    desired_date = request.args.get("date")
    # plot_type = request.args.get("selectnutrients")
    plot_type = "All"     

    if(desired_date and plot_type):
       
        
        cmd = db.session.query(func.round(func.coalesce(func.sum((Nutrition.Energy/100)*(Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('cal'),\
        func.round(func.coalesce(func.sum((Nutrition.Water/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('water'), func.round(func.coalesce(func.sum((Nutrition.Carbohydrate/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('carbs'),\
        func.round(func.coalesce(func.sum((Nutrition.Fiber/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('fiber'),func.round(func.coalesce(func.sum((Nutrition.Protein/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('protein'), \
        func.round(func.coalesce(func.sum((Nutrition.Calcium/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('calcium'),func.round(func.coalesce(func.sum((Nutrition.Copper/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('copper'), \
        func.round(func.coalesce(func.sum((Nutrition.Iron/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('iron'),func.round(func.coalesce(func.sum((Nutrition.Magnesium/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('magnesium'), \
        func.round(func.coalesce(func.sum((Nutrition.Manganese/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('manganese'),func.round(func.coalesce(func.sum((Nutrition.Phosphorus/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('phosphorus'), \
        func.round(func.coalesce(func.sum((Nutrition.Selenium/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('selenium'),func.round(func.coalesce(func.sum((Nutrition.Zinc/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('zinc'), \
        func.round(func.coalesce(func.sum((Nutrition.Potassium/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('potassium'),func.round(func.coalesce(func.sum((Nutrition.Sodium/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('sodium'), \
        func.round(func.coalesce(func.sum((Nutrition.Vitamin_A/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_A'), func.round(func.coalesce(func.sum((Nutrition.Vitamin_C/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_C'),\
        func.round(func.coalesce(func.sum((Nutrition.Vitamin_D/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_D'), func.round(func.coalesce(func.sum((Nutrition.Vitamin_E/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_E'),\
        func.round(func.coalesce(func.sum((Nutrition.Vitamin_K/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_K'), func.round(func.coalesce(func.sum((Nutrition.Thiamin/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('thiamin'),\
        func.round(func.coalesce(func.sum((Nutrition.Riboflavin/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('riboflavin'), func.round(func.coalesce(func.sum((Nutrition.Niacin/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('niacin'),\
        func.round(func.coalesce(func.sum((Nutrition.Vitamin_B6/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_B6'), func.round(func.coalesce(func.sum((Nutrition.Folate_Total/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('folate'),\
        func.round(func.coalesce(func.sum((Nutrition.Vitamin_B12/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('vitamin_B12'), func.round(func.coalesce(func.sum((Nutrition.Panto_Acid/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('panto_acid_VB5'),\
        func.round(func.coalesce(func.sum((Nutrition.Choline_Tot_mg/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('choline'), func.round(func.coalesce(func.sum((Nutrition.Lipid_Total/100)* (Meal_record.amount)*(Nutrition.Weight_grams)),0),2).label('fats'))\
        .join(Meal_record, Nutrition.NDB_No == Meal_record.meal_item_code)\
        .filter(Meal_record.username == session['username'])\
        .filter(Meal_record.meal_date == desired_date)
        
        daily_stats = cmd.first()
                                
        userdata_nutrition_data = createJson(daily_stats)
        cmd1 = db.session.query(User_account.height.label('height'), User_account.weight.label('weight'),\
            User_account.physical_activity_level.label('phy'),User_account.gender.label('gender'), User_account.date_of_birth.label('dob'))\
            .join(Meal_record, User_account.username == Meal_record.username)\
            .filter(User_account.username == session['username'])
        user_info = cmd1.first()
        user_personal_data = creatUserPersonalJson(user_info)
       
        user_info = {"userdata_nutrition_data": userdata_nutrition_data,"user_personal_data":user_personal_data, "plot_type":plot_type }
        graphJSON =creatplotdata(user_info)
        ids = ['plot1', 'plot2', 'plot3']
        return render_template("Daily_vizualization.html",ids=ids, graphJSON=graphJSON)
    return render_template("Daily_vizualization.html")


def checkLoggedIn():
    if 'loggedin' in session:
        if session['loggedin'] == True:
            return True
    return False 

@app.route('/nutrition')
def nutrition():
    if(checkLoggedIn() == False):
        return redirect('/login')
    session['page']='nutrition'
    return render_template("nutrition.html")

# @app.route('/register')
# def register():
#     session['page']='register'
#     return render_template("New_user.html")

@app.route('/intake')
def intake():
    if(checkLoggedIn() == False):
        return redirect('/login')
    session['page']='intake'
    return render_template("intake.html")

@app.route('/logout')
def logout():
    if(checkLoggedIn() == False):
        session['page']=' '
        return render_template('login.html', msg="Already logged out!")
    else:
        session['loggedin'] = False
        messages = "loggedout"
        session['messages'] = messages
        session['page']=' '
        return redirect("/")  


@app.route('/nutriquicksearch', methods=['GET'])
def nutriquicksearch():
    searchkey=request.args.get('term')
    if not searchkey:
        return '{  "data": [] } '
    resultSet = db.session.query(Nutrition.NDB_No, Nutrition.Shrt_Desc, Nutrition.Energy)\
        .filter(Nutrition.Shrt_Desc.ilike('%'+searchkey+'%')).all()
    return jsonify(data=resultSet)


def plot():
    x1=[1,2,3]
    y1=[1,2,3]

    data = [go.Scatter(x=x1, y=y1,mode='markers',marker=dict(
            color='LightSkyBlue',
            size=5,
            opacity=0.5,
            line=dict(
                color='MediumPurple',
                width=2)))
            ]

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == "__main__":
    app.run(debug=True)
    #app.run() 
