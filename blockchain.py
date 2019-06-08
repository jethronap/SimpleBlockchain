import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self):
        # creates a new block and adds it to the chain
        pass
    
    def new_transaction(self):
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
        # hashes a block
        pass

    @property
    def last_block(self):
        # returns the last block in the chain
        pass