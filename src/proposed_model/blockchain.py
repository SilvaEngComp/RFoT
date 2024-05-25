# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
from src.suport_layer.hostTrainer import HostTrainer
from src.suport_layer.cipher import Cipher
from src.proposed_model.pool import Pool
import re
from src.suport_layer.node import Node
from src.suport_layer.transaction import Transaction
from src.suport_layer.block import Block
import ast
import os
import json
import hashlib
import datetime
import time
# import sys
# sys.path.insert(
#     0, '/home/mininet/mininet_blockchain_ml/proposed_model/proposed_model')


class Blockchain:
    def __init__(self, node=None):
        self.node = node
        self.blockchainType = "data_blockchain"
        self.chain = []
        self.nodes = set()
        self.cipher = Cipher()
    
    
    @property
    def fileName():
        return str(self.blockchainType+str(self.node)+'.json')
    
    @property
    def fileNameNotCript():
       return str(
            'blockchain_notCript_'+str(self.node)+'.json')

    def __str__(self):

        return str({
            "chain": self.chain,
        })

    def __repr__(self):
        return str({
            "chain": self.chain,
        })

    def toJson(self):
        chain = []
        for block in self.chain:
            chain.append(Block.toJson(block))

        return {
            "chain": chain,
        }

    def toJsonDecrypted(self) -> dict():
        chain = []
        if self.chain is not None:
            for block in self.chain:
                chain.append(Block.fromJsonDecrypt(Block.toJson(block)).toJson())


        return {
            "chain": chain,
        }

    @classmethod
    def fromJson(self, data):
        try:
            if isinstance(data, list):
                chain = []
                for jsonBlock in data:
                    chain.append(Block.fromJson(jsonBlock))
                return chain
        except:
            if isinstance(data, Blockchain(node)):
                return data
            print('That is not a dict object. Try it again!')

    def registerEncripted(self, prefix="../proposed_model/"):
        self.fileName = str(self.blockchainType +
                            str(self.node)+'.json')
        # fileNameNotCript = str(prefix + self.fileNameNotCript)
        fileNameNotCript =  self.fileNameNotCript
        try:
            dataBytes = json.dumps(self.toJson()).encode("utf-8")
            encrypted = self.cipher.encrypt(dataBytes)
            try:
                with open(self.fileName, 'wb') as f:
                    f.write(encrypted)
                print('registring new chain in {} with {} blocks '.format(
                    self.fileName, len(self.chain)))
            except:
                print("Erro ao criptografar blockchain: ", self.chain)
        except:
            print("Erro ao converter chain para bytes ", self.fileName)

    def register(self, prefix="../proposed_model/"):
        # fileNameNotCript = str(prefix + self.fileNameNotCript)
        fileNameNotCript = self.fileNameNotCript
        with open(fileNameNotCript, 'w') as blockchainFile:
            jsonData = self.toJson()
            print('registring new chain in {} with {} blocks '.format(
                self.fileName, len(self.chain)))
            if jsonData is not None:
                json.dump(self.toJson(), blockchainFile)

    def createBlock(self, data, typeBlock="data", dataBlock=None):

        if typeBlock == "data":
            self.blockchainType = "data_blockchain"
            return self.createDataBlock(data)
        else:
            self.blockchainType = "consumer_blockchain"
            return self.createConsumerBlock(data, dataBlock)

    def createDataBlock(self, pool):
        previousBlock = self.getPreviousBlock()
        if previousBlock is None:
            block = Block(pool, self.blockchainType)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(pool, self.blockchainType,
                          (previousBlock.index+1), proof, previousHash)

        self.chain.append(block)
        if (self.isChainValid(self.chain)):
            # self.register()
            self.registerEncripted()
        else:
            self.chain = []

        return block

    def createConsumerBlock(self, pool, dataBlock):
        if dataBlock is None:
            print('Some bad happens...data block is None')
            return None
        previousBlock = self.getPreviousBlock()
        index = dataBlock.index
        dataHash = self.hash(dataBlock)
        hostTrainer = HostTrainer(self.node, index, dataHash)
        if previousBlock is None:
            block = Block(pool, self.blockchainType, None,
                          None, None, None, hostTrainer)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(pool, self.blockchainType, (previousBlock.index+1),
                          proof, previousHash, None, hostTrainer)
        print('135 - transactions: ', block.transactions)
        self.chain.append(block)
        if (self.isChainValid(self.chain)):
            self.register()
            self.registerEncripted()
        else:
            self.chain = []

        return block

    def getPreviousBlock(self):
        chain = self.solveBizzantineProblem()
        if chain is None:
            return None
        elif len(chain) > 0:
            self.chain = chain
            return self.chain[-1]
        return None

    def proofOfWork(self, previous_proof, new_proof=1):
        if isinstance(previous_proof, str):
            previous_proof = int(previous_proof)
        if isinstance(new_proof, str):
            new_proof = int(new_proof)

        while True:
            hashOperation = self.getHashOperation(previous_proof, new_proof)
            if self.checkPuzzle(hashOperation) is True:
                break
            else:
                new_proof += 1
        return new_proof

    def checkPuzzle(self, hash_test):
        if hash_test[0:7] == '0000000':
            return True
        return False

    def getHashOperation(self, previous_proof, new_proof):
        return hashlib.sha256(str(new_proof**2-previous_proof**2).encode("utf-8")).hexdigest()

    def hash(self, value):
        try:
            if isinstance(value, Block):
                value = str(value)
                encoded = json.dumps(value).encode("utf-8")
                return hashlib.sha256(encoded).hexdigest()
        except:
            print('It can not get the hash of not Block: ', type(value))
            return None

    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            previousBlockHash = self.hash(previousBlock)
            if block.previousHash != previousBlockHash:
                print('hashs diferents')
                return False
            previousProof = previousBlock.proof
            proof = block.proof
            hashOperation = self.getHashOperation(previousProof, proof)
            if self.checkPuzzle(hashOperation) is False:
                return False
            previousBlock = block
            blockIndex += 1
        return True

    def getLocalBLockchainFile(self, node=None, prefix='../proposed_model/'):
        if node is not None:
            x = re.search("^"+self.blockchainType+".*json$", node)
            if (x is False):
                fileName = str(prefix + self.blockchainType+node+'.json')
            else:
                fileName = str(prefix + node)
            
            if os.path.exists(fileName) is False:
                return []

            try:
                with open(fileName, 'rb') as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        cipher = Cipher()
                        data = blockchainFile.read()
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        dataJson = Blockchain.fromJson(dataJson['chain'])
                        return dataJson
            except:
                print('not found local blockchain file: ', fileName)
                return []

    def getBlockchainFileNames(self, prefix='../proposed_model'):
        fileNames = []
        for file in os.listdir(prefix):
            if file.endswith(".json"):
                x = re.search("^"+self.blockchainType+".*json$", file)
                if (x):
                    fileNames.append(file)
        return fileNames

    def solveBizzantineProblem(self):
        try:
            nodes = self.getBlockchainFileNames()
            longest_chain = None
            max_length = 0
            nameNode = None
            if (nodes):
                for node in nodes:
                    chain = self.getLocalBLockchainFile(node)
                    length = len(chain)
                    isValide = self.isChainValid(chain)
                    if length > max_length and isValide:
                        max_length = length
                        longest_chain = chain
                        nameNode = node
            else:
                longest_chain = []
            print('The current biggest chain is {} with {} blocks'.format(
                nameNode, len(longest_chain)))
            return longest_chain

        except:
            print('Something wrong happen in replaceChain...')
            return None
