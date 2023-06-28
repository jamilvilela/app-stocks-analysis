import urllib.parse as parse
from config.Common import Common
from pymongo import MongoClient

class MongoDB:
    """
    This class gives a connection to the MongoDB database 
    and executes basic operations (Insert, Insert many, Update)
    """    

    def __init__(self):
        config = Common()
        self.db_config = config.get_Database() 
        
        self.cluster  = self.db_config['DB_CLUSTER_NAME']
        self.port     = self.db_config['DB_PORT_NUMBER']        
        self.database = self.db_config['DB_DATABASE_NAME']    
        self.user     = self.db_config['DB_USER_NAME']
        self.password = parse.quote_plus( self.db_config['DB_PASSWORD'] )

        self._stringConn = (f'mongodb+srv://{self.user}:{self.password}@{self.cluster}.n3igf.mongodb.net/{self.database}') #?retryWrites=true&w=majority
        #self._stringConn = (f'mongodb://{self.user}:{self.password}@{self.cluster}:{self.port}/')

        try:
            cluster  = MongoClient(self._stringConn)
            self._db = cluster[self.database]
            
        except Exception as ex:
            raise Exception(f'Database connection error: {ex}')
    
    def mongo_aggregate(self, Pipeline, Collection) -> list:
        
        try:            
            coll = self._db[Collection]
            cursor = coll.aggregate(pipeline=Pipeline)
            result = [doc for doc in cursor if doc]
            return result 
        
        except Exception as ex:
            raise Exception(f'Aggregate MongoDB Error: {Collection}')
    
    def mongo_find(self, Filter, Collection, Limit=0, Sort=None):
        try:
            coll = self._db[Collection]
            
            if Filter == None and (Limit == 0 or Limit == None):
                Limit = 1000
            
            if Limit == 1:
                cursor = coll.find_one(Filter)
                result = cursor
            else:
                cursor = coll.find(filter=Filter, limit=Limit).sort(Sort)
                result = [doc for doc in cursor if doc]
            return result
        
        except Exception as ex:
            raise Exception(f'Database connection error: {ex}')

    def mongo_insert_items(self, Items, Collection):
        """ Insert a set of documents"""
        try:
            coll = self._db[Collection]      
            if type(Items) is dict:   
                insList = coll.insert_one(Items)
            else:
                insList = coll.insert_many(Items)
                
            return insList 
        
        except Exception as ex:
            raise Exception(f'Error inserting into MongoDB: {ex.args[0]}')
    
    def mongo_update_items(self, Filter, Update, Collection, Upsert):
        """ Update a set of documents"""
        try:
            coll    = self._db[Collection]
        
            if Filter == None:
                raise 'There is no filter for update command.'
        
            upd_rslt = coll.update_many(Filter, Update, upsert=Upsert)
            return upd_rslt
        
        except Exception as ex:
            raise Exception(f'Error updating into MongoDB: {ex.args[0]}')

    def mongo_delete_items(self, Filter, Collection):
        ''' 
            delete the documents regarding the Filter parameter
        '''
        try:            
            coll = self._db[Collection]
            coll.delete_many(filter=Filter)
            
        except Exception as ex:
            raise Exception(f'Error deleting MongoDB collection: {Collection} when {Filter}. \n{ex.args[0]}')
        
        

   