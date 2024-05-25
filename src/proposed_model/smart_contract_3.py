"""
    This is a Smart contract wich gets a block from in Data Blockchain
"""
from src.proposed_model.blockchain import Blockchain
from src.suport_layer.block import Block
import random
from src.suport_layer.cipher import Cipher
import json
import os


class SC3:
    @staticmethod
    def getNotAssinedBlock(node) -> Block:
        b1 = Blockchain(node)
        chain = b1.solveBizzantineProblem()
        try:
            if (len(chain) > 0):
                lastPosition = len(chain)-1
                block = Block.fromJson(chain[random.randint(0, lastPosition)])
                SC3.registerEncripted(node, block)
                return Block.fromJsonDecrypt(block.toJson())
            return None
        except:
            return None

    @staticmethod
    def registerEncripted(node, block, prefix=""):
        fileName = str("lastBlockReaded_"+str(node)+'.json')
        cipher = Cipher()
        try:
            dataBytes = json.dumps(block.toJson()).encode("utf-8")
            encrypted = cipher.encrypt(dataBytes)
            try:
                with open(fileName, 'wb') as f:
                    f.write(encrypted)
                print('registring lastBlock to {} with index {} '.format(
                    node, block.index))
            except:
                print("Erro ao criptografar lastBlock: ", block)
        except:
            print("Erro ao converter lastBlock para bytes ", fileName)

    @staticmethod
    def getBCD(node) -> Blockchain:
        b1 = Blockchain(node)
        b1.chain= b1.solveBizzantineProblem()
        return b1
       