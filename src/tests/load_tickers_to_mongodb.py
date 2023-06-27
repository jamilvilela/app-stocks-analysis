from models.TickersModel import TickersModel


if __name__ == '__main__':
    
    try:

        tickers = TickersModel()
        tickers._openFile('17mty_hAjWwq1P2EVzosR7DtB_ANoPQC0n89Z-dBTbf4')

        tickers._insertCollectionTickers()
        
        print('Finish.')
    except Exception as ex:
        raise Exception(f'Error: {ex.args[0]}')