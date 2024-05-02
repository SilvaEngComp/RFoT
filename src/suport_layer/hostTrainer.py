# from blockchain import Blockchain
class HostTrainer:
    def __init__(self, hostTrainer=None, dataIndex=None, dataHash=None):
        self.hostTrainer=hostTrainer
        self.dataIndex=dataIndex
        self.dataHash=dataHash
    
    def __str__(self):
        return str({
            'hostTrainer': self.hostTrainer,
            'dataIndex': self.dataIndex,
            'dataHash': self.dataHash,
            })
    def __repr__(self):
        return str({
            'hostTrainer': self.hostTrainer,
            'dataIndex': self.dataIndex,
            'dataHash': self.dataHash,
            })
    
    @classmethod
    def fromJson(self, jsonHostTrainer):
        if isinstance(jsonHostTrainer, dict):
            hostTrainer = HostTrainer(jsonHostTrainer['hostTrainer'],jsonHostTrainer['dataIndex'],jsonHostTrainer['dataHash'])
            return hostTrainer
        return jsonHostTrainer
    
    def toJson(self):
        data = {
            'hostTrainer': self.hostTrainer,
            'dataIndex': self.dataIndex,
            'dataHash': self.dataHash,
            }
        
        return data
        
    #circular import with blockchain
    # def isValid(self):
    #     b1 = Blockchain('hostTrainer','b1_')
    #     chain = b1.solveBizzantineProblem()
    #     for block in chain:
    #         if self.dataIndex==block.index:
    #             blockHash = b1.hash(block)
    #             if self.dataHash==blockHash:
    #                 return True
    #     return False