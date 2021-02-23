from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

#Create instance of flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/")

@app.route("/")
def home():
    
    #Find one record of data from the mongo database
    data = mongo.db.data.find_one()
    
    #Return template and data
    return render_template("index.html", data=data)

#Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    data = mongo.db.data
    
    #Run the scrape function
    mars_= scrape_mars.scrape()
    
    #Update the Mongo database using update and upsert=True
    data.update({}, data, upsert=True)
    
    #Redirect back to the home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
    
