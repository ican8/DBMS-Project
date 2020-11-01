from flask import Flask, render_template, url_for,redirect,flash
from form import RegistrationForm, LoginForm
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'startcode'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/products")
def products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM products")
    data = cur.fetchall()
    cur.close()
    return render_template('products.html', title='products',data=data)

@app.route("/customers")
def customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM customers")
    data = cur.fetchall()
    cur.close()
    return render_template('customers.html', title='customers',data=data)

@app.route("/update",methods = ['GET','POST'])
def update():
    return render_template('update.html', title='update')

@app.route("/insert",methods = ['GET','POST'])
def insert():
    return render_template('insert.html', title='insert')



@app.route("/orders")
def orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM orders")
    data = cur.fetchall()
    cur.close()
    return render_template('orders.html', title='orders',data=data)



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)