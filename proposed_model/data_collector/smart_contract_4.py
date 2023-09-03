"""
    This is a Smart contract wich miner a block in Consumer Blockchain
"""
from blockchain import Blockchain

class SC4:
    @staticmethod
    def setAssinedBlockModel(node, typeBlock, model):   
        transactions = [Transaction(node, node, node, model)]      
        blockchain = Blockchain(node, 'B3_')
        try:
            blockchain.createBlock(transactions, typeBlock)
            return True
        except:
            print("Sorry! the model could not be saved in the blockchain")
            return False