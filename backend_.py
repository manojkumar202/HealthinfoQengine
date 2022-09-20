from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup 
import Phase_3 as ph

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def home(): 
    
    if request.method == 'POST':
        #print('before')
        query = test.AppRanking(request.form['search'])
        #print('after')
        return render_template("home.html", results = query, query = request.form['search'])
    return render_template("home.html")


#if __name__ == "__main__":
test=ph.QueryRanking()
print('came')
app.run()

