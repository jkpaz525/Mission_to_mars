from flask import Flask, jsonify, redirect, render_template
import pymongo
# from pymongo import MongoClient
from scrape_mars import scrape
import scrape_mars

client = pymongo.MongoClient('mongodb://localhost:27017/')

app = Flask(__name__)
db = client.mars_data_DB
mars_collection = db.mars_collection

@app.route("/")
def render_index():
    # Error handler for missing collection
    try:
        mars_find =  mars_collection.find_one()

        # Distributes data from collection
        news_title = mars_find['news_data']['news_title']
        news_p = mars_find['news_data']['paragraph']
        featured_image_url = mars_find['featured_image_url']
        tweet_weather = mars_find['tweet_weather']
        mars_table = mars_find['mars_table']
        hemisphere_title_1= mars_find['mars_img'][0]['title']
        hemisphere_img_1 = mars_find['mars_img'][0]['img_url']
        hemisphere_title_2 = mars_find['mars_img'][1]['title']
        hemisphere_img_2 = mars_find['mars_img'][1]['img_url']
        hemisphere_title_3 = mars_find['mars_img'][2]['title']
        hemisphere_img_3 = mars_find['mars_img'][2]['img_url']
        hemisphere_title_4 = mars_find['mars_img'][3]['title']
        hemisphere_img_4 = mars_find['mars_img'][3]['img_url']
    except (IndexError, TypeError) as error_handler:
        # Missing collection; clears fields
        news_title = ""
        news_p =""
        featured_image_url = ""
        tweet_weather = ""
        mars_table = ""
        hemisphere_title_1 = ""
        hemisphere_img_1 = ""
        hemisphere_title_2 = ""
        hemisphere_img_2 = ""
        hemisphere_title_3 = ""
        hemisphere_img_3 = ""
        hemisphere_title_4 = ""
        hemisphere_img_4 = ""

    return render_template("index.html", news_title=news_title,\
                                         news_p=news_p,\
                                         featured_image_url=featured_image_url,\
                                         tweet_weather=tweet_weather,\
                                         mars_table=mars_table,\
                                         hemisphere_title_1=hemisphere_title_1,\
                                         hemisphere_img_1=hemisphere_img_1,\
                                         hemisphere_title_2=hemisphere_title_2,\
                                         hemisphere_img_2=hemisphere_img_2,\
                                         hemisphere_title_3=hemisphere_title_3,\
                                         hemisphere_img_3=hemisphere_img_3,\
                                         hemisphere_title_4=hemisphere_title_4,\
                                         hemisphere_img_4=hemisphere_img_4)

    @app.route('/scrape')
    def scrape_mars_data():
        scrape_results = scrape_mars.scrape()
        mars_collection.replace_one({}, scrape_results, upsert=True)
        return redirect('http://localhost:5000/', code=302)

if __name__ == '__main__':
    app.run()