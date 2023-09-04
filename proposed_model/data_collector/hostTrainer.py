# from blockchain import Blockchain
class HostTrainer:
    def __init__(self, hostTrainer=None, block=None):
        self.hostTrainer=hostTrainer
        self.dataIndex=block.index
    
    @classmethod
    def fromJson(self, jsonHostTrainer):
        if isinstance(jsonHostTrainer, dict):
            hostTrainer = HostTrainer(jsonHostTrainer['hostTrainer'],jsonHostTrainer['dataIndex'])
            return hostTrainer
        return jsonHostTrainer
    
    def toJson(self):
        return {
            'hostTrainer': self.hostTrainer,
            'dataIndex': self.dataIndex,
            }
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