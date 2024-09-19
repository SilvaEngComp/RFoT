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
    selectedPositionsFileName = 'selectedPositions.json'
    
    @staticmethod
    def getNotAssinedBlock(node) -> Block:
        b1 = Blockchain(node)
        chain = b1.solveBizzantineProblem()
        
        try:
            selctedPosition = SC3.getSelectedPositions()
            print(f'selctedPosition = {selctedPosition}')
            transactionsSize = len(chain)-1
            if transactionsSize > 0 and len(selctedPosition)<transactionsSize:
                while True:
                    randomPosition = random.randint(0, transactionsSize)
                    if(randomPosition not in selctedPosition):
                        selctedPosition.append(randomPosition)
                        block = Block.fromJson(chain[randomPosition])
                        SC3.registerSelectedPosition(selctedPosition)
                        return block
            else:
                print(f'Limite de dados atingidos: {transactionsSize} pacotes coletados')
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def getSelectedPositions(prefix='../proposed_model/'):
        
        fileName = str(prefix + SC3.selectedPositionsFileName)
    
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
    def registerSelectedPosition(selectedPosition, prefix='../proposed_model/'):
            fileName = str(prefix + SC3.selectedPositionsFileName)
            with open(fileName, "w") as file:
                try:
                    print('registring new selected position | nº: {} '.format(
                        len(selectedPosition)))
                    json.dump(selectedPosition, file)
                except Exception as e:
                    print(e)
                    print('erro in registration')
    @staticmethod
    def registerEncripted(node, block, prefix="../proposed_model/"):
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
       