#using Flask and Mongo to create a web app

#imports 
#use flask to render a template, redirecting to another url, and creating a url
from flask import Flask, render_template, redirect, url_for
#use pymongo to interact with mongo database
from flask_pymongo import PyMongo 
#to use the scraping code, convert from jupyter notebook to python
import scraping 

#set up Flask 
app = Flask(__name__)

#tell python how to connect to mongo using pymongo
#use flask_pymongo to setup mongo connection
#This URI is saying that the app can reach Mongo through our localhost server, 
#using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

#define the route for the html page
@app.route('/') #tells flask what to display on homepage
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route('/scrape')
def scrape():
    #new variable that points to mars database
    mars = mongo.db.mars 
    #variable to hold newly scraped data
    #here it's referencing the scrape_all function in the scraping.py file 
    mars_data = scraping.scrape_all() 
    # {} means we're inserting empty data so we need a new, empty json object
    # upsert = True tells mongo to create a new doc if one doesn't already exist
    mars.update({}, mars_data, upsert = True)
    #will navigate the page back to '/'
    return redirect('/', code = 302)

#tell flask to run 
if __name__ == "__main__":
    app.run()