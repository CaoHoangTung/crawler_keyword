from utils.crawler import *
import requests
from jsondb.db import Database
db = Database("./engine/data/log.json")

post_data = get_post_content_from_link(
                source="https://vnexpress.net", post_link="https://vnexpress.net/ho-tru-nuoc-ngot-lon-nhat-mien-tay-can-kho-4091186.html")

# print(post_data)
db.data(dictionary=post_data)
