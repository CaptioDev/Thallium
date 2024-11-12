from flask import Flask, render_template, jsonify, request
import hashlib
import random
import string
import time
import socket

app = Flask(__name__)

# Initialize blockchain (simplified)
blockchain = [{"index": 1, "timestamp": time.time(), "transactions": [], "previous_hash": "1", "hash": "genesis_block_hash"}]
current_transactions = []
start_time = time.time()

def generate_wallet_address():
    # Generate a random private key (simulated)
    private_key = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    
    # Create the address by hashing the private key
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    
    # Address is the first 42 characters of the hash of the public key
    address = hashlib.sha256(public_key.encode()).hexdigest()[:42]
    
    return address

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wallet', methods=['GET'])
def generate_wallet():
    address = generate_wallet_address()
    return jsonify({"address": address})

@app.route('/block_info', methods=['GET'])
def block_info():
    latest_block = blockchain[-1]
    uptime = round(time.time() - start_time, 2)
    ip = socket.gethostbyname(socket.gethostname())  # Get local IP
    return jsonify({
        "block_index": latest_block["index"],
        "uptime": uptime,
        "ip": ip
    })

if __name__ == '__main__':
    app.run(debug=True)
