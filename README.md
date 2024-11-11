# Thallium Blockchain

Thallium is a lightweight blockchain project designed to provide an easy-to-use framework for creating and managing blockchain transactions, mining new blocks, and handling wallets. This repository contains the codebase for the Thallium Blockchain and its associated front-end GUI interface.

## Features

- **Blockchain Info**: Display current block index, uptime, and server IP.
- **Wallet Generation**: Generate a new wallet address for transactions.
- **Transaction Creation**: Create and manage transactions between addresses.
- **Block Mining**: Mine new blocks and add pending transactions to the blockchain.
- **Transaction Viewing**: View transaction details, including sender, recipient, amount, and more.
- **Mint & Burn Tokens**: Support for minting new tokens and burning existing ones.

## Getting Started

To run this project locally, follow these steps:

### Prerequisites

- Python 3.8+
- Flask
- jQuery
- Git (for version control)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/CaptioDev/Thallium.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Thallium
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv thallium-env
    source thallium-env/bin/activate  # On Windows, use `thallium-env\Scripts\activate`
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the app:

    ```bash
    python app.py
    ```

    This will start a local server at `http://127.0.0.1:5000`.

### Running the Application

- Open your browser and navigate to `http://127.0.0.1:5000`.
- You will see a GUI displaying blockchain info, the wallet generation button, and transaction data.

### API Endpoints

Here are the available API commands:

1. **Mine New Block**:  
    - Endpoint: `/mine`
    - Description: Mines a new block and adds all pending transactions to the blockchain.

2. **Create a New Transaction**:  
    - Endpoint: `/transactions/new`
    - Required JSON:
      ```json
      {
          "sender": "address_from",
          "recipient": "address_to",
          "amount": 100,
          "transaction_type": "transfer"
      }
      ```
    - Description: Creates a new transaction. Specify the sender, recipient, amount, and transaction type (e.g., "transfer").

3. **Check Balance**:  
    - Endpoint: `/balance/<address>`
    - Description: Returns the balance of the specified address.

4. **Burn Tokens**:  
    - Endpoint: `/burn`
    - Required JSON:
      ```json
      {
          "sender": "address_from",
          "amount": 100
      }
      ```
    - Description: Burns a specified amount of tokens from the sender's balance.

5. **Mint New Tokens**:  
    - Endpoint: `/mint`
    - Required JSON:
      ```json
      {
          "recipient": "address_to",
          "amount": 100
      }
      ```
    - Description: Mints new tokens and sends them to the specified recipient.

## Contributing

We welcome contributions to Thallium! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new pull request.

## License

This project is licensed under the GNU General Public License v3.0 License - see the [GNU General Public License v3.0](LICENSE) file for details.

## Acknowledgments

- Flask for creating the web framework.
- jQuery for simplifying front-end interactions.

---

Feel free to reach out with any questions or issues related to the project!
