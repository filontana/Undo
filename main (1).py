from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    con = sqlite3.connect("customer.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS customer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    mobile TEXT,
                    CustomerEmail TEXT,
                    CustomerType TEXT,
                    CustomerCity TEXT,
                    Password TEXT,
                    user_id TEXT
                )''')
    con.commit()
    con.close()

create_table()

def create_table1():
    con = sqlite3.connect("customer.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS subscription (
                    sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    plan TEXT,
                    duration TEXT 
                )''')
    con.commit()
    con.close()
create_table1()


@app.route("/")
def add_customer():
    return render_template("add_cust.html")

@app.route("/save_details", methods=["POST", "GET"])
def save_details():
    if request.method == "POST":
        try:  
            name = request.form["CustomerName"]  
            cust_mobile = request.form["CustomerMobile"]  
            Email = request.form["CustomerEmail"] 
            CustomerType = request.form["CustomerType"] 
            CustomerCity = request.form["CustomerCity"] 
            Password = request.form["Password"]  
            user_id = request.form["user_id"]  

            # Connecting to the database and inserting the customer details
            with sqlite3.connect("customer.db") as con:
                cur = con.cursor()  
                cur.execute("INSERT into customer (name, mobile, CustomerEmail, CustomerType, CustomerCity, Password, user_id) values (?,?,?,?,?,?, ?)",(name,cust_mobile, Email, CustomerType, CustomerCity, Password, user_id))  
                con.commit()  
                msg = "Customer Successfully Registered" 
        except Exception as e:  
            msg = f"We can not add the customer to the list: {str(e)}" 
    return render_template("save.html", msg=msg)  

@app.route("/view")  
def view():  
    con = sqlite3.connect("customer.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("SELECT * FROM customer")  
    rows = cur.fetchall()  
    con.close()  # Close the connection after fetching data
    return render_template("view.html", rows=rows) 

@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord", methods=["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("customer.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("DELETE FROM customer WHERE id = ?", (id,))
            con.commit()  
            msg = "Record successfully deleted" 
            
        except Exception as e:  
            msg = f"Error: {str(e)}" 
           
        return render_template("delete_record.html", msg=msg)
         

@app.route("/edit")  
def edit():  
    return render_template("edit.html") 

@app.route("/editrecord", methods=['POST'])
def editrecord():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("customer.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM customer WHERE id = ?", (id,))
            row = cur.fetchone()
            con.commit()
            con.close()
            return render_template("edit_record.html", row=row)
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template("edit_record.html")  # Render edit record template if no POST request

@app.route("/editedrecord", methods=['POST'])
def editedrecord():
    if request.method == 'POST':
        try:
            id = request.form["id"]  
            name = request.form["CustomerName"]  
            cust_mobile = request.form["CustomerMobile"]  
            Email = request.form["CustomerEmail"] 
            CustomerType = request.form["CustomerType"] 
            CustomerCity = request.form["CustomerCity"] 
            Password = request.form["Password"]  

            with sqlite3.connect("customer.db") as con:
                cur = con.cursor()  
                cur.execute("UPDATE customer SET name=?, mobile=?, CustomerEmail=?, CustomerType=?, CustomerCity=?, Password=? WHERE id=?", (name, cust_mobile, Email, CustomerType, CustomerCity, Password, id))  
                con.commit()  
                return redirect("/view")  
        except Exception as e:  
            msg = f"Error: {str(e)}"
            return render_template("new.html", msg=msg)  
    return redirect("/view") 

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logincustomer",methods=["POST", "GET"])
def loginCustomer():
    if request.method == 'POST':
        try:
            username = request.form["username"]
            password = request.form["password"]
            
            with sqlite3.connect("customer.db") as con:
                cur = con.cursor()  
                cur.execute("SELECT * FROM customer WHERE user_id=? AND Password=?", (username, password))  
                customer = cur.fetchone()  # Fetch the customer with the provided username and password
                if customer:
                    # If customer exists, redirect to subscription page
                    return render_template("subscription.html", user_id=username)
                else:
                    # If customer does not exist or password is incorrect, display error message
                    message = "Invalid username or password. Please try again."
                    return render_template("login.html", message=message)
        except Exception as e:
            # Handle any exceptions that may occur
            return f"An error occurred: {e}"
    else:
        # If request method is GET, render the login form
        return render_template("login.html")


@app.route("/save_plan", methods=["POST", "GET"])
def save_plan():
    if request.method == "POST":
        try:
            user_id = request.form["user_id"]
            subscription_plan = request.form["plan"]
            subscription_duration = request.form["duration"]
            
            with sqlite3.connect("customer.db") as con:
                cur = con.cursor()  
                
                # Insert the new subscription into the database
                cur.execute("INSERT INTO subscription (user_id, plan, duration) VALUES (?, ?, ?)", (user_id, subscription_plan, subscription_duration))  
                con.commit()
                
                msg="Subscription Choosen"
                return render_template("sub_det.html", msg=msg)
        except Exception as e:  
            msg = f"Error: {str(e)}"
            return render_template("sub_det.html", msg=msg) 
 # Render the viewplan.html template with the error message

@app.route("/sub_detail")
def sub_detail():
    try:
        con = sqlite3.connect("customer.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Select all columns from both tables
        cur.execute("""
            SELECT customer.name, customer.CustomerEmail, subscription.sub_id, subscription.user_id, subscription.plan, subscription.duration
            FROM customer
            JOIN subscription ON customer.user_id = subscription.user_id
        """)

        rows = cur.fetchall()
        con.close()

        return render_template("viewplan.html", rows=rows)
    except Exception as e:
        # Handle any exceptions that may occur
        return f"An error occurred: {e}"



if __name__ == '__main__':
   app.run(debug=True)
