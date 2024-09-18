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
            selctedPosition = SC3.getSelectedPositions()
            transactionsSize = len(chain)-1
            if transactionsSize > 0 and len(selctedPosition)<transactionsSize:
                while True:
                    randomProsition = random.randint(0, transactionsSize)
                    if(randomProsition not in selctedPosition):
                        block = Block.fromJson(chain[random.randint(0, lastPosition)])
                        SC3.registerEncripted(node, block)
                        return Block.fromJsonDecrypt(block.toJson())
            else:
                print(f'Limite de dados atingidos: {transactionsSize} pacotes coletados')
        except:
            return None
    
    @staticmethod
    def getSelectedPositions(prefix='../proposed_model/'):
        selectedPositionsFileName = 'selectedPositions.json'
        fileName = str(prefix + selectedPositionsFileName)
    
        try:
            with open(fileName, 'w+') as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    return data
                else:
                    return []
        except Exception as e:
            print(e)
            print(f'not found local pool file: {fileName} ')
            return []

    @staticmethod
    def registerEncripted(node, block, prefix="../data_collector/"):
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
       