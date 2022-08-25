from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/") #Tells Flask what to display when we ae looking at the homepage.
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape") # Defines the route that flask will be using
def scrape():
   mars = mongo.db.mars                 #Assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all()    #References the scrape all function
   mars.update_one({}, {"$set":mars_data}, upsert=True)     # Update the database
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()

   