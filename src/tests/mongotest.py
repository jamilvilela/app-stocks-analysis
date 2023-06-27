from pymongo import MongoClient
from mongodb.MongoDB import MongoDB
import urllib.parse as parse

class test:
    def __init__(self) -> None:
        self.tickers = []
        
    def mongo_client(self):
        senha = parse.quote_plus('dE@012022')

        stringConn = (f'mongodb+srv://jamilvilela:{senha}@Cluster0.n3igf.mongodb.net/stocks_analysis') 
        cluster  = MongoClient(stringConn)

        db = cluster['stocks_analysis']
        coll = db['tickers']
        result = coll.aggregate(pipeline=[{"$group": {"_id": "$Type", "count": {"$sum": 1}}}])

        print(list(result))
        for doc in result:
            print(doc)

        tickerType = 'Currency'
        listFound = coll.find(filter={'Type': tickerType}, limit=10)


        print(list(listFound))
        for item in listFound:
            print(item)

    def mongo_class(self):
        db = MongoDB()
        result = db.mongo_find(Filter={'Type': 'Stock'}, 
                                     Collection='tickers',
                                     Limit=10, Sort=[('Name', 1)])
        
        print(result[0])
        self.tickers = result
        return result

if __name__ == '__main__':
    tst = test()
    tickers = tst.mongo_class()
    if tst.tickers and tst.tickers[0]['Type'] == 'Stock':
        for tck in tickers:
            if tst.tickers and tck['Type'] == 'Stock':
                print(tck['Type'], tck['Name'])