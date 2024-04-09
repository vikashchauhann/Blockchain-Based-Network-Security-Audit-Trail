import sqlite3
from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from web3 import Web3, HTTPProvider
import json
from werkzeug.security import check_password_hash
from flask import redirect



app = Flask(__name__) 
app.secret_key = b'\x1e\xa1\x9b\xbf\xafU\xad\xff\tZ\xc4\xa9\x9d\x14\xcd\xeb\x03\xa0\xf3\xf8\xb3\x1bH\xd8'
app.static_folder = 'static'
# Connect to Ganache using web3
ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache URL
web3 = Web3(HTTPProvider(ganache_url))

def fetch_all_contract_addresses():
  
    # Get all transactions from ganache and saving the contract addresses
    block_number = web3.eth.block_number
    all_contract_addresses = set()

    for block_num in range(1, block_number + 1):
        block = web3.eth.get_block(block_num)
        for tx_hash in block['transactions']:
            tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
            if tx_receipt and tx_receipt['contractAddress']:
                all_contract_addresses.add(tx_receipt['contractAddress'])

    return list(all_contract_addresses)


def get_transactions(contract_address):

    # Load contract ABI file
    with open('../SmartContracts/SmartContract.abi', 'r') as file:
        abi = json.load(file)

    # Get contract instance
    contract = web3.eth.contract(address=contract_address, abi=abi)

    # Get all events names from the ABI
    event_names = [event['name'] for event in abi if event['type'] == 'event']

    transactions = []

    # Call the getData function to retrieve the data stored in the contract
    data = contract.functions.getData().call()
    transactions.append(data)

    return transactions
    


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Query the database for the provided username using a parameterized query
        #this is done for sql injection prevention
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        # Close the database connection
        conn.close()

        # If user exists and password is correct
        if user and check_password_hash(user[2], password):
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

# Filtered transactions route
@app.route('/', methods=['GET', 'POST'])
def filtered_transactions():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            date_input = request.form['date']
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
        elif 'date' in request.args:
            date_input = request.args['date']
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
        else:
            # Default to today's date if no date is provided
            date = None

        # Get all contract addresses from Ganache
        contract_addresses = fetch_all_contract_addresses()

        # Iterate through each contract address and get transactions
        transactions_data = []
        all_timestamps = set()  # To store all available timestamps
        for contract_address in contract_addresses:
            transactions = get_transactions(contract_address)
            transactions_data.append({"contract_address": contract_address, "transactions": transactions})
            for tx in transactions:
                if isinstance(tx, str):  # Check if tx is a string
                    try:
                        tx_data = json.loads(tx)  # Load the JSON data
                        if "Timestamp" in tx_data:
                            timestamp = datetime.fromisoformat(tx_data["Timestamp"]).date()
                            all_timestamps.add(timestamp)
                    except (ValueError, KeyError):
                        pass  # Ignore transactions with invalid or missing timestamps

        # Convert set of timestamps to sorted list for display
        all_timestamps = sorted(list(all_timestamps))

        # Calculate transactions count for each timestamp
        timestamp_transactions_count = {}
        for timestamp in all_timestamps:
            count = sum(1 for data in transactions_data for tx in data["transactions"] if isinstance(tx, str)
                        for key in json.loads(tx).keys() if key == "Timestamp"
                        and datetime.fromisoformat(json.loads(tx)["Timestamp"]).date() == timestamp)
            timestamp_transactions_count[timestamp] = count

        if date:  # Proceed only if a date is selected
            # Filter transactions based on the provided date
            filtered_transactions_data = []
            for data in transactions_data:
                filtered_transactions = []
                for tx in data["transactions"]:
                    if isinstance(tx, str):  # Check if tx is a string (assuming it's JSON)
                        try:
                            tx_data = json.loads(tx)  # Load the JSON data
                            # Check if the transaction occurred on the provided date
                            if "Timestamp" in tx_data and datetime.fromisoformat(tx_data["Timestamp"]).date() == date:
                                # Add the transaction to filtered_transactions
                                filtered_transactions.append(tx_data)
                        except (ValueError, KeyError):
                            pass  # Ignore transactions with invalid or missing timestamps
                # If there are filtered transactions, add them to filtered_transactions_data
                if filtered_transactions:
                    filtered_transactions_data.append({"contract_address": data["contract_address"], "transactions": filtered_transactions})
            # Render the template with filtered transactions data, all timestamps, and transaction count for each timestamp
            return render_template('index.html', transactions_data=filtered_transactions_data, all_timestamps=all_timestamps, timestamp_transactions_count=timestamp_transactions_count)
        else:
            # Render the template with a message asking the user to select a date
            return render_template('index.html', message='Please select a date.', all_timestamps=all_timestamps, timestamp_transactions_count=timestamp_transactions_count)
    else:
        return redirect('/login')

if __name__ == '__main__':
    # Clear session when the server starts
    @app.before_first_request
    def clear_session():
        session.clear()

    # Function to check if user is logged in before each request
    @app.before_request
    def require_login():
        allowed_routes = ['login']
        if request.endpoint not in allowed_routes and 'logged_in' not in session:
            return redirect('/login')

    app.run(debug=True)
