"""
    This is a Smart contract wich gets a block from in Data Blockchain
"""
from blockchain import Blockchain

class SC2:
    @staticmethod
    def getBlockchain(node, transactions):
        blockchain = Blockchain(node);
        
    @staticmethod
    def minerNotAssinedTransaction(node, transactions):
        print("getting transactions")
        # transactions = Pool.getNotAssinedTransactions()      
        blockchain = Blockchain(node)
        before = len(blockchain.chain)
        print("size before = ",before)
        blockchain.createBlock(transactions)
        after = len(blockchain.chain)
        print("size after = ",after)
        if(after>before):
            return True
        else:
            return False 