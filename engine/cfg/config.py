CHROME_PATH = "http://127.0.0.1:4444/wd/hub"

config = {
    "https://ndh.vn": {
        "elastic_index": "posts",
        "pagination_url": "https://ndh.vn/search.html?q={:s}&page={:d}.html",
        "xpath": {
            "post_links": "//div[@class='list-news']//article[@class='item-news']//h3[@class='title-news']//a",
            "title": "//h1[@class='title-detail']",
            "content": "//article[@class='fck_detail']",
            "date": "//span[@class='date-post']",
            "author": "",
        }
    },
    "https://vnexpress.net": {
        "elastic_index": "vnexpress",
        "pagination_url": "{:s}https://vnexpress.net/thoi-su-p{:d}",
        "comment_url": "https://usi-saas.vnexpress.net/index/get?offset=0&limit=100&objectid={:s}&siteid=1&objecttype=1",
        "reply_url": "https://usi-saas.vnexpress.net/index/getreplay?siteid=1&objecttype=1&id={:s}&limit=100&offset=0",
        "xpath": {
            "post_links": "//article//*[@class='title-news']//a",
            "title": "//h1[@class='title-detail']",
            "content": "//article[@class='fck_detail']",
            "date": "//span[@class='date']",
            "author": "//p[@class='author_mail']//strong",
            "comment_viewmore": "//div[@class='view_more_coment width_common mb10']//a",
            "comment_viewreply": "//p[@class='count-reply']//a",
            "comment_nextpage": "//a[@class='btn-page next-page ']",
            "comment_item": "//div[contains(@class, 'comment_item')]",
            "comment_item_username": "//div[contains(@class, 'content-comment')]//p[contains(@class, 'full_content')]//span[contains(@class, 'txt-name')]//a//b",
            "comment_item_body": "//div[contains(@class, 'content-comment')]//p[contains(@class, 'full_content')]"
        },
        "link_filter": "c.eclick.vn",
    },
}