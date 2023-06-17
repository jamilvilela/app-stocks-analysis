from flask import Flask, render_template, request, redirect
from datetime import datetime
from dataclasses import dataclass, field
from config.Common import Common
from models.AppModel import AppModel


app = Flask(__name__) #, static_folder="static")

@dataclass
class Item:
    ticker: str
    insert_date: datetime

@dataclass
class Wallet:
    user_email: str
    stocks: Item = field(default_factory=list)
         
appModel = AppModel()
wallet = Wallet(user_email='', stocks=[])
        
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        wallet.user_email = request.form.get('user_email')
        
        return redirect('/list?user_email=' + wallet.user_email)
    return render_template('login.html')

@app.route('/list')
def stocks_list():
    
    global wallet
    
    if len(wallet.stocks) == 0:
        
        wlt = appModel.get_wallet(wallet.user_email)
        if len(wlt):
            wlt_new = Wallet(user_email=wlt['user_email'], stocks=list(wlt['stocks']))
            if wlt['_id']:
                wallet = wlt_new
    
    return render_template('list.html', wallet_list=wallet)

@app.route('/stock_insert/<string:ticker>', methods=['POST'])
def stock_insert(ticker):
    
    list(wallet.stocks).append({"ticker": ticker, "insert_date": datetime.utcnow()})
    
    return redirect('/list?user_email=' + wallet.user_email)

@app.route('/delete/<string:ticker>', methods=['POST'])
def stock_delete(ticker):
    
    index = next((index for index, stock in enumerate(wallet.stocks) if stock['ticker'] == ticker), None)
   
    if index is not None:
        del wallet.stocks[index]
    return redirect('/list?user_email=' + wallet.user_email)

@app.route('/save', methods=['POST'])
def wallet_save():
    if wallet:
        appModel.insert_wallet(wallet)
        
    return redirect('/')

if __name__ == '__main__':
    app.run()
