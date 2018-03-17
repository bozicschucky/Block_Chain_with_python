import hashlib
import json
from time import time
from uuid  import uuid4
from flask import Flask
class Blockchain(object):
    """docstring for Blockchain"""
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #create the genesis block
        self.new_block(previous_hash=1,proof=100)


    

    def new_block(self):
        """
        #creates a new block and adds it to the Chain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
                'index':len(self.chain)+1,
                'timestamp':time(),
                'transactions':self.current_transactions,
                'proof':proof,
                'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }
        #reset the current lines of transaction
        self.current_transactions =[]
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        #Adds a new transaction to the list of transactions
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':recipient
            })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        #hashes the block
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        # we make sure that the dictionary is ordered, or we'll inconsistent hashes 
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha-256(block_string).hexdigest()
    @property
    def last_block(self):
        #returns the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        A simple proof of work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof,proof) is false:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof,proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash=hashlib.sha-256(guess).hexdigest()
        return guess_hash[:4] == "0000"


#creat a flask object
app = Flask(__name__)

#Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

#instantiate the blockChain
blockchain = Blockchain()

@app.route('/mine', methods=["GET"])
def mine():
    return "We'll mine a new block "

@app.route('/chain', methods=["GET"])
def full_chain():
    response = {
            'chain':blockchain.chain,
            'lenght':len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run()