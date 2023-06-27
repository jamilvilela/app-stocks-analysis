from config.Common import Common
from mongodb.MongoDB import MongoDB
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
import bcrypt

@dataclass
class Stocks:
    type: str
    ticker: str
    inserted_date: datetime
            
class WalletModel:
    
    def __init__(self):
        conf = Common()
        self.db_config = conf.get_Database() 
        self.Timezone = conf.get_TimeZone()
        self._db = MongoDB()        
        self.wallet_struct= {}
        self.wallet= {}
        self.ticker_type_current = ''
        self.ticker_type_list= []
        self.tickers= []
        self.setStruct()

    def get_tickerType(self):
        
        collection = self.db_config['DB_TABLE_TICKERS']
        pipeline = [{"$group": {"_id": "$Type", "count": {"$sum": 1}}},
                    {"$sort": {"_id": -1}}
                    ]        
        self.ticker_type_list = self._db.mongo_aggregate(pipeline, collection)
        return self.ticker_type_list

    def checkLogin(self, email, password) -> bool:
        wlt = self.get_wallet(email)

        if wlt:
            pwd = bytes(password, 'utf-8')
            hsh_pwd = wlt['user_password']
            return bcrypt.checkpw(pwd, hsh_pwd)            
        else:
            self.setPassword(password)
            return True    

    def get_wallet(self, user_email) -> dict:        
        result = self._db.mongo_find(Filter={'user_email': user_email}, 
                                     Collection=self.db_config['DB_TABLE_WALLET'], 
                                     Limit=1
                                     )
        return result
            
    def get_tickers(self, tickerType=None):        
        return self._db.mongo_find(Filter={'Type': tickerType}, 
                                     Collection=self.db_config['DB_TABLE_TICKERS'],
                                     Limit=0,
                                     Sort=[('Ticker', 1)]
                                     )
    
    def setStruct(self):
        self.wallet_struct = {'_id':'', 
                              'user_email':'', 
                              'user_password':'', 
                              'inserted_date':'', 
                              'updated_date':'', 
                              'stocks':[]
                              }
        self.wallet = self.wallet_struct.copy()
        return
        
    def setEmail(self, email: str):
        if email:
            self.wallet['user_email'] = email
        return
    
    def setPassword(self, pwd: str):
        if pwd:
            pwd = bytes(pwd, 'utf-8')
            salt = bcrypt.gensalt(rounds=10)
            hsh_pwd = bcrypt.hashpw(pwd, salt)
            self.wallet['user_password'] = hsh_pwd
        return
    
    def getEmail(self) -> str:
        return self.wallet['user_email']

    def getStocks(self) -> list:
        return self.wallet['stocks']

    def getStocksWallet(self) -> dict:
        wallet_db = self.get_wallet(self.getEmail()) if not self.getStocks() else {}
        wallet_db = self.wallet_struct.copy() if not wallet_db else wallet_db 
        self.wallet = self.wallet if (not wallet_db['stocks'] or self.getStocks()) else wallet_db
        self.wallet['stocks'] = sorted(self.wallet['stocks'], key=lambda x: (x['type'], x['ticker'])) 
        return self.wallet
    
    def getWallet(self) -> dict:
        return self.wallet
    
    def insert(self, ticker_type, ticker):
        ticker = ticker.split(' :: ')[0]
        if ticker and (not self.getStocks() or (not any(item['ticker'] == ticker for item in self.getStocks()))):
            stock = asdict(Stocks(type = ticker_type, ticker = ticker, inserted_date = datetime.utcnow()))
            self.wallet['stocks'].append(stock)

        return
    
    def delete(self, ticker):
        self.wallet['stocks'] = [stock for stock in self.wallet['stocks'] if stock['ticker'] != ticker]
        return

    def insert_wallet(self, wallet: dict):
        collection = self.db_config['DB_TABLE_WALLET']            
        filter = {'user_email': wallet['user_email']}
        data = self._db.mongo_find(filter, collection, Limit=1)
        
        if not data:
            wallet['_id'] = str(uuid.uuid4())
            wallet['inserted_date'] = datetime.utcnow()
            wallet['updated_date'] = datetime.utcnow()
            result = self._db.mongo_insert_items(wallet, collection)
        else:
            if data != wallet:
               wallet['updated_date'] = datetime.utcnow()
               result = self._db.mongo_update_items(Filter={'_id': wallet['_id']},
                                                    Update={'$set': wallet},
                                                    Collection=collection,
                                                    Upsert=True
                                                    )
               return result
               
    def save(self):
        if self.getEmail():
            self.insert_wallet(self.getWallet())
        return
