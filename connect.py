from flask import Flask, render_template, request, redirect, url_for,flash,jsonify,session,abort
import pymysql
import mysql.connector
from mysql.connector import IntegrityError
from datetime import timedelta,date
import json


app = Flask(__name__)
app.secret_key = "hello"

# Database connection configuration
conn = mysql.connector.connect(host='localhost', username='root', password='1234', database='CarDealerShip')
my_cursor = conn.cursor()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to serve the main page
@app.route('/')
def index():
    flash("Fine", "success")
    print("Flash message: Fine")
    return render_template('index.html')

# Route to serve the before login page
@app.route('/beforeLog')
def bforelogin():
    flash("Fine", "success")
    print("Flash message: Fine")
    return render_template('beforeLog.html')

# Route to serve the salesperson login page
@app.route('/Slog')
def slogin():
    flash("Fine", "success")
    print("Flash message: Fine")
    return render_template('Slog.html')

# Route to serve the manager login page
@app.route('/Mlog')
def mlogin():
    flash("Fine", "success")
    print("Flash message: Fine")
    return render_template('Mlog.html')

# Route to serve the customer back from login page
@app.route('/indexAfter')
def indexAfter():
    flash("Fine", "success")
    print("Flash message: Fine")
    username = request.args.get('username')
    print(username)
    return render_template('indexAfter.html', username=username)

# Route to serve the book form page
@app.route('/book_form')
def book_form():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('book_form.html')

# Route to serve the salesperson page
@app.route('/salesperson')
def salesperson():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('salesperson.html')

# Route to serve the manager page
@app.route('/manager')
def manager():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('manager.html')

# Route to serve the customer page
@app.route('/customer')
def customer():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('customer.html')

# Route to serve the book page
@app.route('/book')
def book():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('book.html')

# Route to serve the vehicle page
@app.route('/vehicle')
def vehicle():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('vehicle.html')

# Route to serve the transaction page
@app.route('/transaction')
def transaction():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('transaction.html')

# Route to serve the salesperson table page
@app.route('/salespersonT')
def salespersonT():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('salespersonT.html')

# Route to serve the report page
@app.route('/report')
def report():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('report.html')

# Route to serve the customerM page
@app.route('/customerM')
def customerM():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('customerM.html')

# Route to serve the transactionM page
@app.route('/transactionM')
def transactionM():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('transactionM.html')

# Route to serve the vehicleM page
@app.route('/vehicleM')
def vehicleM():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('vehicleM.html')

# Route to serve the bookM page
@app.route('/bookM')
def bookM():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('bookM.html')

# Route to serve the Customer log page
@app.route('/Clog')
def Clog():
    flash("Hi", "info")
    print("Flash message: Hi")
    return render_template('Clog.html')


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/api/customers')
def get_customers():
    try:
        # Execute SQL query to fetch customer data
        my_cursor.execute("SELECT * FROM Customer")
        customers = my_cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        customer_list = []
        for customer in customers:
            customer_dict = {
                "CId": customer[0],
                "CFirstName": customer[1],
                "CLastName": customer[2],
                "CDateOfBirth": str(customer[3]),
                "CLicenseId": customer[4],
                "CAddress": customer[5],
                "CPhoneNumber": customer[6]
            }
            customer_list.append(customer_dict)

        # Return customer data as JSON
        return jsonify(customer_list)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        # Execute SQL query to fetch customer data based on customer_id
        my_cursor.execute("SELECT * FROM Customer WHERE CId = %s", (customer_id,))
        customer = my_cursor.fetchone()

        # Check if customer exists
        if customer:
            # Convert customer data to a dictionary
            customer_dict = {
                "CId": customer[0],
                "CFirstName": customer[1],
                "CLastName": customer[2],
                "CDateOfBirth": str(customer[3]),
                "CLicenseId": customer[4],
                "CAddress": customer[5],
                "CPhoneNumber": customer[6]
            }
            # Return customer data as JSON
            return jsonify(customer_dict)
        else:
            return jsonify({"error": "Customer not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# Route to handle customer deletion
@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # Execute SQL query to delete the customer with the specified ID
        delete_query = "DELETE FROM Customer WHERE CId = %s"
        my_cursor.execute(delete_query, (customer_id,))
        conn.commit()
        return jsonify({"message": f"Customer with ID {customer_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Route to handle the creation of a new customer
@app.route('/api/customers', methods=['POST'])
def create_customer():
    try:
        # Extract data from the JSON request body
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')
        license_id = data.get('license_id')
        address = data.get('address')
        phone_number = data.get('phone_number')

        # Insert the new customer data into the database
        insert_query = "INSERT INTO Customer (CFirstName, CLastName, CDateOfBirth, CLicenseId, CAddress, CPhoneNumber) VALUES (%s, %s, %s, %s, %s, %s)"
        customer_data = (first_name, last_name, date_of_birth, license_id, address, phone_number)
        
        my_cursor.execute(insert_query, customer_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Customer created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        # Extract data from the JSON request body
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')
        license_id = data.get('license_id')
        address = data.get('address')
        phone_number = data.get('phone_number')

        # Update the customer data in the database
        update_query = "UPDATE Customer SET CFirstName = %s, CLastName = %s, CDateOfBirth = %s, CLicenseId = %s, CAddress = %s, CPhoneNumber = %s WHERE CId = %s"
        customer_data = (first_name, last_name, date_of_birth, license_id, address, phone_number, customer_id)
        my_cursor.execute(update_query, customer_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Customer updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
        
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    
@app.route('/api/vehicle')
def get_vehicle():
    try:
        # Execute SQL query to fetch vehicle data
        my_cursor.execute("SELECT * FROM Vehicle")
        vehicles = my_cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_dict = {
                "VId": vehicle[0],
                "CId": vehicle[1],
                "VModel": vehicle[2],
                "VYear": vehicle[3],
                "VPrice": vehicle[4],
                "VMake": vehicle[5],
                "VColor": vehicle[6]  # Add VColor to the dictionary
            }
            vehicle_list.append(vehicle_dict)

        # Return vehicle data as JSON
        return jsonify(vehicle_list)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicles(vehicle_id):
    try:
        #print(vehicle_id)
        # Execute SQL query to fetch vehicle data based on vehicle_id
        my_cursor.execute("SELECT * FROM Vehicle WHERE VId = %s", (vehicle_id,))
        vehicle = my_cursor.fetchone()

        # Check if vehicle exists
        if vehicle:
            # Convert vehicle data to a dictionary
            vehicle_dict = {
                "VId": vehicle[0],
                "CId": vehicle[1],
                "VModel": vehicle[2],
                "VYear": vehicle[3],
                "VPrice": vehicle[4],
                "VMake": vehicle[5],
                "VColor": vehicle[6]  # Add VColor to the dictionary
            }
            
            # Return vehicle data as JSON
            #print(vehicle_dict)
            return jsonify(vehicle_dict)
        else:
            return jsonify({"error": "Vehicle not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to handle vehicle deletion
@app.route('/api/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        # Execute SQL query to delete the vehicle with the specified ID
        delete_query = "DELETE FROM Vehicle WHERE VId = %s"
        my_cursor.execute(delete_query, (vehicle_id,))
        conn.commit()
        return jsonify({"message": f"Vehicle with ID {vehicle_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
# Route to handle the creation of a new vehicle
@app.route('/api/vehicle', methods=['POST'])
def create_vehicle():
    try:
        # Extract data from the JSON request body
        data = request.json
        cid = data.get('customer_id')
        vmodel = data.get('vehicle_model')
        vyear = data.get('vehicle_year')
        vprice = data.get('vehicle_price')
        vmake = data.get('vehicle_make')
        vcolor = data.get('vehicle_color')  # Extract vehicle color

        # Insert the new vehicle data into the database
        insert_query = "INSERT INTO Vehicle (CId, VModel, VYear, VPrice, VMake, VColor) VALUES (%s, %s, %s, %s, %s, %s)"
        vehicle_data = (cid, vmodel, vyear, vprice, vmake, vcolor)  # Add vcolor to the vehicle data
        my_cursor.execute(insert_query, vehicle_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Vehicle created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vehicle/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        # Extract data from the JSON request body
        data = request.json
        cid = data.get('cid')
        vmodel = data.get('vmodel')
        vyear = data.get('vyear')
        vprice = data.get('vprice')
        vmake = data.get('vmake')
        vcolor = data.get('vcolor')  # Extract vehicle color
        
        # Update the vehicle data in the database
        update_query = "UPDATE Vehicle SET CId = %s, VModel = %s, VYear = %s, VPrice = %s, VMake = %s, VColor = %s WHERE VId = %s"
        vehicle_data = (cid, vmodel, vyear, vprice, vmake, vcolor, vehicle_id)  # Add vcolor to the vehicle data
        my_cursor.execute(update_query, vehicle_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Vehicle updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Route to fetch transaction data
@app.route('/api/transaction')
def get_transaction():
    try:
        # Execute SQL query to fetch transaction data
        my_cursor.execute("SELECT * FROM TransactionDetails")
        transactions = my_cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        transaction_list = []
        for transaction in transactions:
            transaction_dict = {
                "TId": transaction[0],
                "CId": transaction[1],
                "SId": transaction[2],
                "MId": transaction[3],
                "VId": transaction[4],
                "TotalPrice": transaction[5],
                "TDate": str(transaction[6]),
                "PMethod": transaction[7],
            }
            transaction_list.append(transaction_dict)

        # Return transaction data as JSON
        return jsonify(transaction_list)

    except Exception as e:
        return jsonify({"error": str(e)})
  
# Route to fetch transaction data
@app.route('/api/transaction/<int:transaction_id>', methods=['GET'])
def get_transactions(transaction_id):
    try:
        # Execute SQL query to fetch transaction data
        my_cursor.execute("SELECT * FROM TransactionDetails Where TId = %s", (transaction_id,))
        transactions = my_cursor.fetchone()
        print(transactions)

        # Convert the fetched data to a list of dictionaries
        if transactions:
            transaction_dict = {
                "TId": transactions[0],
                "CId": transactions[1],
                "SId": transactions[2],
                "MId": transactions[3],
                "VId": transactions[4],
                "TotalPrice": transactions[5],
                "TDate": str(transactions[6]),
                "PMethod": transactions[7],
            }
            return jsonify(transaction_dict)
        else:
            return jsonify({"error": "Transaction not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
    
# Route to handle transaction deletion
@app.route('/api/transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        # Execute SQL query to delete the transaction with the specified ID
        delete_query = "DELETE FROM TransactionDetails WHERE TId = %s"
        my_cursor.execute(delete_query, (transaction_id,))
        conn.commit()
        return jsonify({"message": f"Transaction with ID {transaction_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
     
# Route to handle the creation of a new transaction
@app.route('/api/transaction', methods=['POST'])
def create_transaction():
    try:
        # Extract data from the JSON request body
        data = request.json
        customer_id = data.get('customerId')
        salesperson_id = data.get('salespersonId')
        manager_id = data.get('managerId')
        vehicle_id = data.get('vehicleId')
        total_price = data.get('totalPrice')
        transaction_date = data.get('transactionDate')
        payment_method = data.get('paymentMethod')

        # Insert the new transaction data into the database
        insert_query = "INSERT INTO TransactionDetails (CId, SId, MId, VId, TotalPrice, TDate, PMethod) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        transaction_data = (customer_id, salesperson_id, manager_id, vehicle_id, total_price, transaction_date, payment_method)
        
        my_cursor.execute(insert_query, transaction_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Transaction created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transaction/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    try:
        # Extract data from the JSON request body
        data = request.json
        customer_id= data.get('customer_id')
        salesperson_id = data.get('salesperson_id')
        manager_id = data.get('manager_id')
        vehicle_id = data.get('vehicle_id')
        total_price = data.get('total_price')
        transaction_date = data.get('transaction_date')
        payment_method = data.get('payment_method')

        # Update the TransactionDetails data in the database
        update_query = "UPDATE TransactionDetails SET CId = %s, SId = %s, MId = %s, VId = %s, TotalPrice = %s, TDate = %s, PMethod = %s WHERE TId = %s"
        transaction_data = (customer_id, salesperson_id, manager_id, vehicle_id, total_price, transaction_date, payment_method, transaction_id)
        my_cursor.execute(update_query, transaction_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Transaction updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to fetch book data
@app.route('/api/book')
def get_book():
    try:
        # Execute SQL query to fetch book data
        my_cursor.execute("SELECT * FROM Book")
        books = my_cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                "BId": book[0],
                "CId": book[1],
                "VId": book[2],
                "CPhone": book[3],
                "BDate": str(book[4])
            }
            book_list.append(book_dict)

        # Return book data as JSON
        return jsonify(book_list)

    except Exception as e:
        return jsonify({"error": str(e)} )
    
# Route to handle the form submission
@app.route('/book_car', methods=['POST'])
def book_car():
    print("hi from add book")
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        car_model = request.form['carModel']
        booking_date = request.form['date']
        booking_time = request.form['time']

        insert_query = "INSERT INTO Book (CId, VId, CPhone, BDate) VALUES (%s, %s, %s, %s)"
        book_data = (1, 1210000, phone, booking_date)

        try:
            my_cursor.execute(insert_query, book_data)
            conn.commit()
            flash("Booking inserted successfully!", "success")
            print("Booking inserted successfully!")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            print(f"Error: {str(e)}")
        return redirect(url_for('index'))
    
@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_books(book_id):
    try:
        # Execute SQL query to fetch booking data based on customer_id
        my_cursor.execute("SELECT * FROM Book WHERE BId = %s", (book_id,))
        book = my_cursor.fetchone()

        # Check if booking exists
        if book:
            # Convert booking data to a dictionary
            book_dict = {
                "BId": book[0],
                "CId": book[1],
                "VId": book[2],
                "CPhone": book[3],
                "BDate": str(book[4])
            }
            # Return booking data as JSON
            print(book_dict)
            
            return jsonify(book_dict)
        else:
            return jsonify({"error": "Booking not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to handle book deletion
@app.route('/api/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Execute SQL query to delete the book with the specified ID
        delete_query = "DELETE FROM Book WHERE BId = %s"
        print(book_id)
        my_cursor.execute(delete_query, (book_id,))
        conn.commit()
        return jsonify({"message": f"Book with ID {book_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to handle the creation of a new book
@app.route('/api/book', methods=['POST'])
def create_book():
    try:
        # Extract data from the JSON request body
        data = request.json
        cid = data.get('customer_Id')
        vid = data.get('vehicle_Id')
        cphone = data.get('customer_phone')
        bdate = data.get('booking_date')

        # Insert the new book data into the database
        insert_query = "INSERT INTO Book (CId, VId, CPhone, BDate) VALUES (%s, %s, %s, %s)"
        book_data = (cid, vid, cphone, bdate)
        
        my_cursor.execute(insert_query, book_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Book created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        # Extract data from the JSON request body
        data = request.json
        customer_id = data.get('cid')
        vehicle_id = data.get('vid')
        customer_phone = data.get('cphone')
        booking_date = data.get('bdate')

        # Update the book data in the database
        update_query = "UPDATE Book SET CId = %s, VId = %s, CPhone = %s, BDate = %s WHERE BId = %s"
        book_data = (customer_id, vehicle_id, customer_phone, booking_date, book_id)
        print(book_data)
        my_cursor.execute(update_query, book_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "Booking updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to handle the salesperson login submission
@app.route('/saleslogin', methods=['POST'])
def saleslogin():
    print("hi from sales method")
    if request.method == 'POST':
        print("hi from post method")

        salesId = request.form['SId']
        password = request.form['pass']
        print(password)
        print(salesId)
        
        # Query the database to check if the salesperson ID exists
        check_query_Id = "SELECT * FROM SalesPerson WHERE SId = %s"
        my_cursor.execute(check_query_Id, (salesId,))

        salesperson = my_cursor.fetchone()
        print(salesperson)
        
        if salesperson:
            # Check if the password matches
            if password == '0000':
                print("hi from correct pass")
                # Password is correct, redirect to the salesperson section
                return redirect(url_for('salesperson'))
            else:
                flash('Incorrect password. Please try again.', 'error')
                return redirect(url_for('index'))  # Redirect to login page with error message
        else:
            flash('Salesperson ID does not exist.', 'error')
            return redirect(url_for('index'))  # Redirect to login page with error message


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to handle the customer login submission
@app.route('/customerlogin', methods=['POST'])
def customerlogin():
    print("hi from customer method")
    if request.method == 'POST':
        print("hi from post method")

        customerName = request.form['name']
        password = request.form['pass']
        print(password)
        print(customerName)
        
        # Check if the account valid
        if password == '2222':
            print("hi from correct pass")
            # Password is correct, redirect to the customer section
            return redirect(url_for('indexAfter', username=customerName))
        else:
            flash('Incorrect username or password. Please try again.', 'error')
            return redirect(url_for('Clog'))  # Redirect to login page with error message
    


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to handle the manager login submission
@app.route('/managerlogin', methods=['POST'])
def managerlogin():
    print("hi from manager method")
    if request.method == 'POST':
        print("hi from post method")

        managerId = request.form['MId']
        password = request.form['pass']
        print(password)
        print(managerId)


        
        # Query the database to check if the salesperson ID exists
        check_query_Id = "SELECT * FROM Manager WHERE MId = %s"
        my_cursor.execute(check_query_Id, (managerId,))

        manager = my_cursor.fetchone()
        print(manager)
        
        if manager:
            # Check if the password matches
            if password == '1111':
                print("hi from correct pass")
                # Password is correct, redirect to the salesperson section
                return redirect(url_for('manager'))
            else:
                flash('Incorrect password. Please try again.', 'error')
                return redirect(url_for('index'))  # Redirect to login page with error message
        else:
            flash('Manager ID does not exist.', 'error')
            return redirect(url_for('index'))  # Redirect to login page with error message

 #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to fetch salesperson data
@app.route('/api/salesPerson')
def get_salesPerson():
    try:
        # Execute SQL query to fetch salesperson data
        my_cursor.execute("SELECT * FROM SalesPerson")
        SalesPersons = my_cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        SalesPerson_list = []
        for SalesPerson in SalesPersons:
            #print(SalesPerson)
            SalesPerson_dict = {
                "SId": SalesPerson[0],
                "EHireDate": str(SalesPerson[1]),
                "EFirstName": SalesPerson[2],
                "ELastName": SalesPerson[3],
                "EEmail": SalesPerson[4],
                "EPhoneNumber": SalesPerson[5],
                "ESalary": SalesPerson[6],
                "EAddress": SalesPerson[7],
                "EDateOfBirth": str(SalesPerson[8]),
                "CommissionRate": SalesPerson[9],

            }
            SalesPerson_list.append(SalesPerson_dict)
        #print("Hi")
        # Return salesperson data as JSON
        return jsonify(SalesPerson_list)

    except Exception as e:
        return jsonify({"error": str(e)})
    
# Route to handle the creation of a new salesperson
@app.route('/api/salesPerson', methods=['POST'])
def create_salesPerson():
    try:
        # Extract data from the JSON request body
        data = request.json
        hire_date = data.get('EHireDate')
        first_name = data.get('EFirstName')
        last_name = data.get('ELastName')
        email = data.get('EEmail')
        phone_number = data.get('EPhoneNumber')
        salary = data.get('ESalary')
        address = data.get('EAddress')
        date_of_birth = data.get('EDateOfBirth')
        commission_rate = data.get('CommissionRate')

        # Insert the new salesperson data into the database
        insert_query = "INSERT INTO SalesPerson (EHireDate, EFirstName, ELastName, EEmail, EPhoneNumber, ESalary, EAddress, EDateOfBirth, CommissionRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        salesperson_data = (hire_date, first_name, last_name, email, phone_number, salary, address, date_of_birth, commission_rate)
        my_cursor.execute(insert_query, salesperson_data)
        conn.commit()

        # Return a success message with status code 201
        return jsonify({"message": "Salesperson created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to handle SalesPerson deletion
@app.route('/api/salesPerson/<int:SId>', methods=['DELETE'])
def delete_salesPerson(SId):
    try:
        # Execute SQL query to delete the book with the specified ID
        delete_query = "DELETE FROM SalesPerson WHERE SId = %s"
        my_cursor.execute(delete_query, (SId,))
        conn.commit()
        return jsonify({"message": f"SalesPerson with ID {SId} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/api/salesPerson/<int:salesPerson_id>', methods=['PUT'])
def update_salesPerson(salesPerson_id):
    try:
        # Extract data from the JSON request body
        data = request.json
        hire_date = data.get('EHireDate')
        first_name = data.get('EFirstName')
        last_name = data.get('ELastName')
        email = data.get('EEmail')
        phone_number = data.get('EPhone')
        salary = data.get('ESalary')
        address = data.get('EAddress')
        date_of_birth = data.get('EDateOfBirth')
        Commission_rate = data.get('CommissionRate')
        print(first_name)
        print(phone_number)
        # Update the salesPersn data in the database
        update_query = "UPDATE SalesPerson SET EHireDate = %s, EFirstName = %s, ELastName = %s, EEmail = %s, EPhoneNumber = %s, ESalary = %s, EAddress = %s, EDateOfBirth = %s, CommissionRate = %s WHERE SId = %s"
        salesPerson_data = (hire_date, first_name, last_name, email, phone_number, salary, address,date_of_birth, Commission_rate, salesPerson_id)
        my_cursor.execute(update_query, salesPerson_data)
        conn.commit()

        # Return a success message
        return jsonify({"message": "SalesPerson updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/salesPerson/<int:salesPerson_id>', methods=['GET'])
def get_salesPersons(salesPerson_id):
    try:
       
        # Execute SQL query to fetch salesPerson data based on salesPerson_id
        my_cursor.execute("SELECT * FROM SalesPerson WHERE SId = %s", (salesPerson_id,))
        salesPerson = my_cursor.fetchone()
        print(salesPerson)

        # Check if salesPerson exists
        if salesPerson:
            # Convert salesPerson data to a dictionary
            salesPerson_dict = {
                "SId": salesPerson[0],
                "EHireDate": str(salesPerson[1]),
                "EFirstName": salesPerson[2],
                "ELastName": salesPerson[3],
                "EEmail": salesPerson[4],
                "EPhoneNumber": salesPerson[5],
                "ESalary": salesPerson[6],
                "EAddress": salesPerson[7],
                "EDateOfBirth": str(salesPerson[8]),
                "CommissionRate": salesPerson[9],
  
            }
            
            # Return salesPerson data as JSON
            print(salesPerson_dict)
            return jsonify(salesPerson_dict)
        else:
            return jsonify({"error": "salesPerson not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
 #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Route to display success message
@app.route('/success')
def success():
    return 'Car booked successfully!'

if __name__ == '__main__':
    app.run(debug=True)
