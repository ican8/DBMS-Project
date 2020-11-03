from flask import Flask, render_template, url_for,redirect,flash,redirect,request
from form import RegistrationForm, LoginForm
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'startcode'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

def get_earning():
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.order_id, SUM(od.quantity*p.unit_price) as amount\
                FROM orders o, `order details` od, products p\
                WHERE o.order_id = od.order_id\
                AND od.product_id = p.product_id\
                AND  o.order_id\
                AND o.order_id IN\
					( SELECT order_id FROM orders )\
                GROUP BY o.order_id;")
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
@app.route("/home")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  COUNT(customer_id) FROM customers")
    customer_data = cur.fetchall()
    cur.execute("SELECT  COUNT(product_id) FROM products")
    product_data = cur.fetchall()
    cur.execute("SELECT  COUNT(order_id) FROM orders")
    order_data = cur.fetchall()
    cur.execute("SELECT  COUNT(shipper_id) FROM shippers")
    shipper_data = cur.fetchall()
    cur.close()
    earning_data = get_earning()
    return render_template('home.html',customer_data=customer_data,product_data=product_data,order_data=order_data,shipper_data=shipper_data,earning_data=earning_data)


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

@app.route("/insert/customer",methods = ['GET','POST'])
def insert_customer():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        first_name = request.form['first name']
        last_name = request.form['last name']
        dob = request.form['dob']
        phone = request.form['phone']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers (first_name,last_name, birth_date,phone,address) VALUES (%s, %s, %s, %s, %s)", (first_name,last_name,dob,phone,address))
        mysql.connection.commit()
        return redirect(url_for('customers'))

    return render_template('insert.html', title='insert')

@app.route("/insert/note",methods = ['POST'])
def insert_note():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        order_id = request.form['order_id']
        text = request.form['text']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes (order_id,text) VALUES (%s,%s)", (order_id,text))
        mysql.connection.commit()
        return redirect(url_for('notes'))

    return render_template('insert.html', title='insert')

@app.route("/insert/shipper",methods = ['POST'])
def insert_shipper():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO shippers (name) VALUES (%s)", (name,))
        mysql.connection.commit()
        return redirect(url_for('shippers'))

    return render_template('insert.html', title='insert')

@app.route('/update/customer',methods=['POST','GET'])
def update_customer():

    if request.method == 'POST':
        id_data = request.form['id']
        first_name = request.form['first name']
        last_name = request.form['last name']
        dob = request.form['dob']
        phone = request.form['phone']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE customers
               SET first_name=%s, last_name=%s,birth_date=%s, phone=%s, address=%s
               WHERE customer_id=%s
            """, (first_name, last_name, dob,phone, address,id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('customers'))
    
    return render_template('home.html')

@app.route("/insert/product",methods = ['GET','POST'])
def insert_product():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        quantity = request.form['quantity']
        unit_price = request.form['unit_price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name,quantity,unit_price) VALUES (%s, %s, %s)", (name,quantity,unit_price))
        mysql.connection.commit()
        return redirect(url_for('products'))

    return render_template('insert.html', title='insert')

@app.route('/update/product',methods=['POST','GET'])
def update_product():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        unit_price = request.form['unit_price']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE products
               SET name=%s, quantity=%s,unit_price=%s
               WHERE product_id=%s
            """, (name,quantity, unit_price,id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('products'))
    
    return render_template('home.html')

@app.route('/delete/customer/<string:id_data>', methods = ['GET'])
def delete_customer(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE customer_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('customers'))

@app.route("/orders")
def orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM orders")
    data = cur.fetchall()
    cur.close()
    return render_template('orders.html', title='orders',data=data)

@app.route("/order_details",methods = ['GET','POST'])
def order_details():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM `order details` WHERE order_id = (%s)",(1,))
    data = cur.fetchall()
    cur.close()
    return render_template('order_details.html', title='order details',data=data)

@app.route("/shippers")
def shippers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM shippers")
    data = cur.fetchall()
    cur.close()
    return render_template('shippers.html', title='shippers',data=data)

@app.route("/pending")
def pending():
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.order_id,o.customer_id,c.first_name,c.last_name FROM customers c, orders o WHERE c.customer_id  = o.customer_id AND o.shipped_date IS NULL")
    data = cur.fetchall()
    cur.close()
    return render_template('pending.html', title='pending orders',data=data)

@app.route("/earning")
def earning():
    data = get_earning()
    return render_template('earning.html', title='earnings',data=data)

@app.route("/notes")
def notes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from notes")
    data = cur.fetchall()
    cur.close()
    return render_template('notes.html', title='notes',data=data)


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