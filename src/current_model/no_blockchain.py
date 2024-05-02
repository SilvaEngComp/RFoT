# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""

import sys
# sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/current_model/data_collector')


from .pool import Pool


class NoBlockchain:

    @staticmethod
    def getNotAssinedBlock():

        transactions = Pool.getNotAssinedTransactions()
        return transactions
