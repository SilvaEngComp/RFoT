"""
    This is a Smart contract wich gets a block from in Data Blockchain
"""
from blockchain import Blockchain
from block import Block
import random
from cipher import Cipher
import json
class SC3:
    @staticmethod
    def getNotAssinedBlock(node)->Block:
        b1 = Blockchain(node);
        b2 = Blockchain(node);
        chain = b1.solveBizzantineProblem()
        try:
            if(len(chain)>0):
                lastPosition = len(chain)-1
                block = Block.fromJson(chain[random.randint(0,lastPosition)]);
                SC3.registerEncripted(node, block)
                return block
            return None
        except:
            return None
    
    @staticmethod
    def registerEncripted(node,block, prefix="../data_collector/"):
        fileName = str("lastBlockReaded_"+str(node)+'.json')
        cipher = Cipher()
        try:
            dataBytes = json.dumps(block.toJson()).encode("utf-8")
            encrypted = cipher.encrypt(dataBytes)
            try:
                with open(fileName,'wb') as f:       
                    f.write(encrypted)
                print('registring lastBlock to {} with index {} '.format(node,block['index']))
            except:
                print("Erro ao criptografar lastBlock: ", block)
        except:
            print("Erro ao converter lastBlock para bytes ", fileName)