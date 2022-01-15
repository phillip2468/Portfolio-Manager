import json

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify
from money_maker.extensions import cache, db
from money_maker.models.news_stories import NewsStories
from sqlalchemy import insert

on_first_load_bp = Blueprint('on_first_load_bp', __name__)


@on_first_load_bp.route("/news-stories")
@cache.cached(timeout=15 * 60)
def load_stories():
    result = get_html_text()
    soup = BeautifulSoup(result, 'html.parser')
    main_section = (soup.find("main", {"id": "content", "class": "-rwd1"}))
    main_stores_list = main_section.find("div", {"class": "_23cgh"})
    stores = main_stores_list.find_all(("div", {"class": "_2slqK undefined", "data-pb-type": "st"}))

    all_stories = []
    for element in stores:
        if element.find("a", {"class": "_20-Rx"}) is not None:
            title = element.find("a", {"class": "_20-Rx"}).text
            paragraph = element.find("p", {"class": "_48ktx", "data-pb-type": "ab"}).text
            link_to_article = element.find("a", {"class": "_20-Rx"}, href=True)["href"]
            image = element.find("img", {"class": "_1srKI"})["data-src"]
            time_inserted = element.find("time").text
            dictionary = {
                "title": title,
                "short_description": paragraph,
                "url": link_to_article,
                "image_url": image,
                "article_updated": time_inserted,
            }
            all_stories.append(dictionary)

    set_of_stories = {json.dumps(d, sort_keys=True) for d in all_stories}
    unique_stories = [json.loads(t) for t in set_of_stories]

    db.session.query(NewsStories).delete()
    stmt = insert(NewsStories)
    db.session.execute(stmt, unique_stories)
    db.session.commit()
    
    return jsonify(unique_stories)


def get_html_text():
    response = requests.get("https://www.afr.com/markets/currencies").text
    return response
