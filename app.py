from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from nameify import Nameify
import re

# configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.secret_key='rocks_ffxiv'
db = SQLAlchemy(app)
namer = Nameify()

#db models
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(2044), nullable=False)
    short = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'My url is {self.long}'

# routes
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url_long = request.form['content']

        if len(url_long) > 2044:
            flash('Too long of a url!')
            return redirect('/')

        found_url = Url.query.filter_by(long= url_long).first()
        url = re.sub("https?://", "", request.url_root)

        if found_url:
            flash(f'Your url is: {url}{found_url.short}')

        else:
            url_short = namer.generate_url()
            tries = 0

            while Url.query.filter_by(short = url_short).first() and tries < 100:
                url_short = namer.generate_url()
                tries+=1

            new_url = Url(long = url_long, short = url_short)
            
            try:
                db.session.add(new_url)
                db.session.commit()
                flash(f'Your url is: {url}{url_short}')

            except:
                return "Error adding url"
            
        return redirect('/')
    else:
        return render_template('index.html')

@app.route('/<path:path>')
def redirect_to_path(path):
    # print(path)
    found_url = Url.query.filter_by(short= path).first()
    if found_url:
        url = re.sub("https?://", "", found_url.long)
        return redirect(f'http://{url}')
    else:
        flash(f'Url not found')
        return redirect('/')

# enable debug
if __name__ == "__main__":
    app.run(debug=True)