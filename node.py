import os
import json

class Node:
    
    @classmethod
    def fileNameDefine(self, prefix=''):
        return str(prefix+'nodes.json')
        
    @classmethod
    def get(self, prefix=''):
        fileName = Node.fileNameDefine(prefix)
        nodes = set()
        try:
            with open(fileName) as nodeFile:
                data = json.load(nodeFile)
                
                for node in data['nodes']:
                    """blockchainFileName = str(prefix+'blockchain_'+node+'.json')
                    if os.path.exists(blockchainFileName) is False:
                        pass
                    else:
                        nodes.add(node)"""
                    nodes.add(node)
                if len(nodes) != data['nodes']:
                    Node.register(nodes, prefix)
                return nodes
        except:
            print('except read nodes.json')
            Node.register(nodes, prefix)
            return nodes
            
    @classmethod
    def register(self, nodes, prefix=''):
        fileName = Node.fileNameDefine(prefix)
        with open(fileName,'w') as nodeFile:
            nodes = {"nodes": list(nodes)}
            json.dump(nodes, nodeFile)
            
    @classmethod
    def add(self, node, prefix=''):
        nodes = Node.get()
        fileName = Node.fileNameDefine(prefix)
        with open(fileName,'w') as nodeFile:
            nodes.add(node)
            nodes = {"nodes": list(nodes)}
            json.dump(nodes, nodeFile)
            