from flask import Flask, render_template, request, redirect
from models.WalletModel import WalletModel


app = Flask(__name__)
walletObj = WalletModel()

@app.route('/', methods=['GET', 'POST'])
def login():
    global walletObj
    
    if request.method == 'POST':
        user_email = request.form.get('user_email')
        user_pass = request.form.get('user_password')
        walletObj.setEmail(user_email)
        
        if walletObj.checkLogin(user_email, user_pass):        
            return redirect('/list?user_email=' + user_email)

    return render_template('login.html')


@app.route('/list')
def stocks_list():    
    global walletObj
    
    wallet = walletObj.getStocksWallet()
    ticker_types = walletObj.ticker_type_list if walletObj.ticker_type_list \
                                              else walletObj.get_tickerType()
    ticker_list = walletObj.tickers   
    return render_template('list.html', wallet=wallet, ticker_types=ticker_types, tickers_list=ticker_list)


@app.route('/stock_insert', methods=['POST'])
def stock_insert():    
    global walletObj
    
    if request.method == 'POST':
        ticker_type=request.form.get('ticker_type')
        stock_ticker=request.form.get('stock_ticker')
        walletObj.insert(ticker_type,stock_ticker)        
   
    return redirect('/list?user_email=' + walletObj.getEmail())


@app.route('/delete/<string:ticker>', methods=['POST'])
def stock_delete(ticker):    
    global walletObj
    walletObj.delete(ticker)
    return redirect('/list?user_email=' + walletObj.getEmail())

@app.route('/get_tickers', methods=['GET'])
def get_tickers():    
    global walletObj
    ticker_type_selected = request.args.get('dropdown-item')
    
    ticker_types = walletObj.ticker_type_list if walletObj.ticker_type_list \
                                              else walletObj.get_tickerType()
    
    if not walletObj.tickers or ticker_type_selected != walletObj.ticker_type_current:
        ticker_list = walletObj.get_tickers(ticker_type_selected)
    else:
        ticker_list = walletObj.tickers

    walletObj.ticker_type_current = ticker_type_selected
    walletObj.tickers = ticker_list
    wallet = walletObj.getStocksWallet()   
    return render_template('list.html', wallet=wallet, ticker_types=ticker_types, tickers_list=ticker_list, ticker_type=ticker_type_selected)

@app.route('/save', methods=['POST'])
def wallet_save():    
    global walletObj
    walletObj.save()
    return redirect('/list?user_email=' + walletObj.getEmail())

@app.route('/close_modal', methods=['POST'])
def close_modal():    
    global walletObj
    return redirect('/list?user_email=' + walletObj.getEmail())

@app.route('/logout')
def logout():
    global walletObj
    walletObj = WalletModel()    
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
