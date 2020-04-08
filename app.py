#in this project we will be submitting the form to the database(mysql)
from flask import Flask, render_template, url_for, request #rende templates helps us to render the html files
from flask_bootstrap import Bootstrap #help us to enter the css element in the website
from flask_mysqldb import MySQL
import yaml#we can not configure all the data in this file because the data is sensitive and can not be exposed so it is configured in the yaml file thereafter it is imported to this file
#instantiate the flask object...flask module expects the name of the applictaion as its first parameter which is passed through__name__
app = Flask(__name__)

#configure database
db = yaml.load(open('db.yaml'))#opening the yaml file wherein the details are saved. this statement would load all the parameter in the form of key value pair
app.config['MYSQL_HOST'] = db['mysql_host'] #passing the values which we have defined in db.yaml file
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
#instantiate the object to pass the file in mysql module
mysql = MySQL(app)
#route decorator is used to add end points(eg google.com/images here /images is the end point) to our application
#Bootstrap(bootstrap)
@app.route("/", methods=['GET', 'POST'])
def index():
	#posting the data to the mysql data base
	if request.method == 'POST':
		form = request.form
		name = form['name']#input tag text field name ="name"
		age = form['age']#input tag text field name ="name"
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
		mysql.connection.commit()
	return render_template('index.html')
#for displaying the data on the web page
@app.route("/employees")
def employees():
	cur = mysql.connection.cursor()
	result_value = cur.execute("SELECT * FROM employee")
	if result_value > 0:
		employees = cur.fetchall()
		return render_template('employees.html', employees=employees)




if __name__ == '__main__':
	app.run(debug=True) 