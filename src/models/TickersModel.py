from mongodb.MongoDB import MongoDB
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

HEADER_STOCKS = ['Ticker','Name','Exchange','Category_Name','Country']
HEADER_ETF = ['Ticker','Name','Exchange']
HEADER_INDEX = ['Ticker','Name','Exchange']
HEADER_CURRENCY = ['Ticker','Name','Exchange']
DB_TABLE_NAME_TICKERS = 'tickers'
TICKER_TYPE_STOCK = 'Stock'
TICKER_TYPE_ETF = 'ETF'
TICKER_TYPE_INDEX = 'Index'
TICKER_TYPE_CURRENCY = 'Currency'

class TickersModel:
    
    def __init__(self) -> None:
        # Define the scope and credentials
        self.scope       = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets.readonly']
        self.credentials = {}
        self.client = None
        self.YahooTickersFile = None
        self.documents = []
        self._authorize()

    def _authorize(self):
        # Authorize the client
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('src/config/credentials.json', self.scope)
        self.client = gspread.authorize(self.credentials)

    def _openFile(self, fileID):
        # Open the Google Sheet by its URL's Id
        self.YahooTickersFile = self.client.open_by_key(fileID)

    def _getTickers(self, workSheet: str):
        # Read all the values from the sheet
        
        if workSheet == TICKER_TYPE_STOCK:
            header = HEADER_STOCKS
        elif workSheet == TICKER_TYPE_ETF:
            header = HEADER_ETF
        elif workSheet == TICKER_TYPE_INDEX:
            header = HEADER_INDEX
        elif workSheet == TICKER_TYPE_CURRENCY:
            header = HEADER_CURRENCY
            
        sheet = self.YahooTickersFile.worksheet(workSheet)
        documents = sheet.get_all_records(head=4, expected_headers=header)
        
        df = pd.DataFrame(documents)
        df.insert(0, column='Type', value=workSheet)
        
        return list(df.to_dict('records'))

    def _insertCollectionTickers(self):
        #insert into mongo      
        _db = MongoDB()
        
        #read tickers from worksheets
        self.documents = self._getTickers(TICKER_TYPE_STOCK)
        _db.mongo_delete_items(Filter={'Type': TICKER_TYPE_STOCK}, Collection=DB_TABLE_NAME_TICKERS)
        _db.mongo_insert_items(self.documents, DB_TABLE_NAME_TICKERS)
        
        self.documents = self._getTickers(TICKER_TYPE_ETF)
        _db.mongo_delete_items(Filter={'Type': TICKER_TYPE_ETF}, Collection=DB_TABLE_NAME_TICKERS)
        _db.mongo_insert_items(self.documents, DB_TABLE_NAME_TICKERS)

        self.documents = self._getTickers(TICKER_TYPE_INDEX)
        _db.mongo_delete_items(Filter={'Type': TICKER_TYPE_INDEX}, Collection=DB_TABLE_NAME_TICKERS)
        _db.mongo_insert_items(self.documents, DB_TABLE_NAME_TICKERS)

        self.documents = self._getTickers(TICKER_TYPE_CURRENCY)
        _db.mongo_delete_items(Filter={'Type': TICKER_TYPE_CURRENCY}, Collection=DB_TABLE_NAME_TICKERS)
        _db.mongo_insert_items(self.documents, DB_TABLE_NAME_TICKERS)
        

        
        
    

    
