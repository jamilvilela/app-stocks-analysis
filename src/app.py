from flask import Flask, render_template, request, redirect
from datetime import datetime
from dataclasses import dataclass, asdict
from models.AppModel import AppModel


app = Flask(__name__) #, static_folder="static")

@dataclass
class Stocks:
    ticker: str
    inserted_date: datetime

appModel = AppModel()

wallet_struct = {'_id':'', 'user_email':'', 'inserted_date':'', 'updated_date':'', 'stocks':[]}
wallet = wallet_struct.copy()

        
@app.route('/', methods=['GET', 'POST'])
def login():

    global wallet
    
    if request.method == 'POST':
        wallet['user_email'] = request.form.get('user_email')
        
        return redirect('/list?user_email=' + wallet['user_email'])
    return render_template('login.html')


@app.route('/list')
def stocks_list():
    
    global wallet, wallet_struct
    
    if not wallet['stocks']:
        print('wallet stocks is empty')
        
    wallet_db = appModel.get_wallet(wallet['user_email']) if not wallet['stocks'] else {}
    wallet_db = wallet_struct.copy() if not wallet_db else wallet_db 
    wallet = wallet if (not wallet_db['stocks'] or wallet['stocks']) else wallet_db
   
    return render_template('list.html', wallet_list=wallet)


@app.route('/stock_insert', methods=['POST'])
def stock_insert():
    
    global wallet
    
    if request.method == 'POST':
        selected_ticker = request.form.get('stock_ticker')
        
        if selected_ticker and (not wallet['stocks'] or 
                               (not any(item['ticker'] == selected_ticker 
                                        for item in wallet['stocks']))):
            stock = asdict(Stocks(ticker = selected_ticker, inserted_date = datetime.utcnow()))
            wallet['stocks'].append(stock)
   
    return redirect('/list?user_email=' + wallet['user_email'])


@app.route('/delete/<string:ticker>', methods=['POST'])
def stock_delete(ticker):
    
    global wallet
    
    wallet['stocks'] = [stock for stock in wallet['stocks'] if stock['ticker'] != ticker]
   
    return redirect('/list?user_email=' + wallet['user_email'])

@app.route('/save', methods=['POST'])
def wallet_save():
    
    global wallet

    if wallet['user_email'].strip():
        appModel.insert_wallet(wallet)
        wallet = wallet_struct.copy()
    return redirect('/')

if __name__ == '__main__':
    app.run()
