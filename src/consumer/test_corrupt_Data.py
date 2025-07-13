
from src.proposed_model.smart_contract_3 import SC3

blockchain = SC3.getBCD("h1")
print(blockchain.chain[0])
print("# There are ",str(len(blockchain.chain))+" blocks")