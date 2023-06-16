import uuid
import pytz
from flask import Flask, render_template, request, redirect
from datetime import datetime
from config.Common import Common
from models.AppModel import AppModel


app = Flask(__name__) #, static_folder="static")

class app():
    '''
    This class allow users register their stocks wallet
    '''
    
    def __init__(self) -> None:
        self.conf = Common()
        self.appModel = AppModel()
        self.timezone = self.conf.get_TimeZone()
        self._db = self.conf.get_Database()


@app.route('/', methods=['GET', 'POST'])
def create_text():
    if request.method == 'POST':
        user_email = request.form['user_email']
        query = request.form['query']
        language = request.form['language']
        created_dt = datetime.now(pytz.timezone(timezone))
          
        search_list.append({'_id': text_id, 
                            'user_email': user_email, 
                            'user_query': query, 
                            'user_language': language, 
                            'created_date': created_dt})
        return redirect('/list?user_email=' + user_email)
    return render_template('create.html')

@app.route('/list')
def search_full_list():
    usrSearchApp = AppSearch()
    user_email = request.args.get('user_email')
    stored_search = []
    stored_search = usrSearchApp.get_user_search_list(user_email)
    filtered_search = search_list.extend(stored_search)
    if user_email:
        filtered_search = [text for text in search_list if text['user_email']==user_email]
        #filtered_search = sorted(filtered_search, key=lambda x: ['user_language'], reverse=True)
    return render_template('list.html', search_list=filtered_search, filter_email=user_email)

@app.route('/delete/<string:text_id>', methods=['POST'])
def delete_text(text_id):
    index = next((index for index, text in enumerate(search_list) if text['_id'] == text_id), None)
    filter_email = search_list[index]['user_email']
    if index is not None:
        del search_list[index]
    return redirect('/list?user_email='+filter_email)

@app.route('/insert-mongodb', methods=['POST'])
def insert_mongodb():
    if search_list:
        usrSearchApp = AppSearch()
        usrSearchApp.insert_app_data(search_list)
        
        log = extract_from_twitter()
        print(log)
        search_list.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run()
