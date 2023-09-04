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
    def getNotAssinedBlock(node):
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
        print("sc3.23 - node:",node)
        print("sc3.24 - block:",block)
        fileName = str("lastBlockReaded_"+str(node)+'.json')
        cipher = Cipher()
        print("sc3.27 - filename",fileName)
        try:
            dataBytes = json.dumps(block.toJson()).encode("utf-8")
            print("sc3.30 - dataBytes",dataBytes)
            encrypted = cipher.encrypt(dataBytes)
            print("sc3.32 - encrypted",encrypted)
            try:
                with open(fileName,'wb') as f:       
                    f.write(encrypted)
                print('registring lastBlock to {} with index {} '.format(node,block['index']))
            except:
                print("Erro ao criptografar lastBlock: ", block)
        except:
            print("Erro ao converter lastBlock para bytes ", fileName)