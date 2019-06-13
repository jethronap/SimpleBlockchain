import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4

from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the first block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        creates a new block and adds it to the chain

        :param proof: <int> the proof given by the Proof of Work Algorithm
        :param previous_hash: (Optional) <str> hash of previous block
        :return: <dict> new Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recepient, amount):
        """
        Creates a new transaction to go into the next mined  Block
        :param sender: <str> Address of the sender
        :param recepient: <str> Address of the recepient
        :param amount: <int> Amount
        :return: <int> the index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recepient': recepient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>

        The dict must be ordered, or else we'll have inconsistent hashes
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Proof of Work Algorithm:
        - Find a number x such that hash(xx') contains 4 leading zeroes, where x is the previous x'
        - x is the previous proof and x' is the new proof

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, else False
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # Instantiate Node
    app = Flask(__name__)

    # Generate a globally unique address for this Node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = Blockchain()

    @app.route('/mine', methods=['GET'])
    def mine():
        return "We'll mine a new block"

    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        return "We'll add a new transaction"

    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
