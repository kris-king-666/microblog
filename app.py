import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

connection_string = os.environ.get('MONGO_URI')
def create_app():
    app = Flask(__name__)
    client = MongoClient(connection_string)
    app.db = client.microblog


    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.utcnow().strftime('%d-%b-%Y')
            app.db.entries.insert_one({'content': entry_content, 'date': formatted_date})
        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.strptime(entry['date'], '%d-%b-%Y').strftime('%d-%b-%Y')
            )
            for entry in app.db.entries.find()
        ]
        return render_template('home.html', entries=entries_with_date)
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
