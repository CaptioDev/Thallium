import hashlib
import json
from time import time
from flask import Flask, jsonify, request, render_template
import socket
import random
import string

# Blockchain and Transaction classes
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block (genesis block)
        genesis_block = self.create_block(previous_hash='1')
        self.chain.append(genesis_block)

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'previous_hash': previous_hash,
            'hash': self.hash_block(self.pending_transactions, previous_hash),
        }
        self.pending_transactions = []  # Reset the transaction list
        return block

    def hash_block(self, transactions, previous_hash):
        # Return a hash of a block
        block_string = json.dumps(transactions, sort_keys=True) + str(previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_transaction(self, sender, recipient, amount, transaction_type):
        # Create and add a transaction
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'transaction_type': transaction_type,
        }
        self.pending_transactions.append(transaction)

    def last_block(self):
        return self.chain[-1]

    def mine(self):
        # Create a new block and add it to the chain
        new_block = self.create_block(self.last_block()['hash'])
        self.chain.append(new_block)
        return new_block

    def get_balance(self, address):
        # Calculate balance of an address by checking all transactions
        balance = 0
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['recipient'] == address:
                    balance += transaction['amount']
                if transaction['sender'] == address:
                    balance -= transaction['amount']
        return balance

    def burn(self, amount, sender):
        # Burn a specific amount from the sender's balance
        if self.get_balance(sender) >= amount:
            self.add_transaction(sender, "burn_address", amount, "burn")
            return True
        return False

    def flash_mint(self, amount, recipient):
        # Mint new coins and add to recipient
        self.add_transaction("mint_address", recipient, amount, "mint")

    def generate_wallet_address(self):
        # Generate a random wallet address (simplified)
        private_key = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        address = hashlib.sha256(public_key.encode()).hexdigest()[:42]
        return address

# API and transaction handling
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wallet', methods=['GET'])
def generate_wallet():
    address = blockchain.generate_wallet_address()
    return jsonify({"address": address})

@app.route('/block_info', methods=['GET'])
def block_info():
    latest_block = blockchain.chain[-1]
    uptime = round(time() - blockchain.chain[0]['timestamp'], 2)
    ip = socket.gethostbyname(socket.gethostname())  # Get local IP
    return jsonify({
        "block_index": latest_block["index"],
        "uptime": uptime,
        "ip": ip
    })

@app.route('/mine', methods=['GET'])
def mine():
    new_block = blockchain.mine()
    return jsonify(new_block), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount', 'transaction_type']
    
    if not all(field in values for field in required_fields):
        return 'Missing values', 400

    blockchain.add_transaction(values['sender'], values['recipient'], values['amount'], values['transaction_type'])
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/balance/<address>', methods=['GET'])
def balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance}), 200

@app.route('/burn', methods=['POST'])
def burn():
    values = request.get_json()
    if 'sender' not in values or 'amount' not in values:
        return 'Missing sender or amount', 400
    
    sender = values['sender']
    amount = values['amount']
    
    if blockchain.burn(amount, sender):
        return jsonify({'message': f'{amount} TLMX burned from {sender}'}), 200
    return 'Insufficient balance', 400

@app.route('/mint', methods=['POST'])
def mint():
    values = request.get_json()
    if 'recipient' not in values or 'amount' not in values:
        return 'Missing recipient or amount', 400

    recipient = values['recipient']
    amount = values['amount']
    
    blockchain.flash_mint(amount, recipient)
    return jsonify({'message': f'{amount} TLMX minted for {recipient}'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
