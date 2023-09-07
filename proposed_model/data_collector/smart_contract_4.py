"""
    This is a Smart contract wich gets a block from in Data Blockchain
"""
from blockchain import Blockchain

class SC4:
    @staticmethod
    def setAssinedBlockModel(node,blockType, transactions):
        blockchain = Blockchain(node)
        before = len(blockchain.chain)
        print("SC4 - size before = ",before)
        blockchain.createBlock(transactions,blockType)
        after = len(blockchain.chain)
        print("SC4 - size after = ",after)
        if(after>before):
            return True
        else:
            return False 