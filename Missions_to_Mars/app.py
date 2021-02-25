from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

#Create instance of flask app
app = Flask(__name__)

# Setup mongo connection
conn = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars_data

#Set route
@app.route("/")
def home():
    mars_data = collection.find_one()
    return render_template("index.html", mars_data=mars_data)

#Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    
    mars_data = collection
    mars_scrape = scrape_mars.scrape()
    
    #Return template and update database
    mars_data.update({}, mars_scrape, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    
