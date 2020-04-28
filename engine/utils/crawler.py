import platform
import utils.elastic as es
import time
import utils.data as data_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cfg.config import config, CHROME_PATH
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from jsondb.db import Database
db = Database("./engine/data/log.json")

wd_options = Options()
wd_options.add_argument("--headless")
wd_options.add_argument('--no-sandbox')
wd_options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Remote(
    CHROME_PATH, DesiredCapabilities.CHROME, options=wd_options
)

# wd = webdriver.Chrome(
#     executable_path='./engine/chromedriver.exe', options=wd_options
# )

# get all new links which are not existing on elastic search
def get_new_links(source="", keyword="", from_page=2, end_page=10, exit_when_url_exist=True):
    page = from_page

    document_exist_in_elastic = False
    post_urls = []
    pagination_url = config[source]["pagination_url"]
    xpath_configuration = config[source]["xpath"]
    es_index = config[source]["elastic_index"]
    link_filter = config[source]["link_filter"]

    while True:
        page_url = pagination_url.format(keyword, page)
        print("GETTING "+page_url)
        wd.get(page_url)

        # print(wd.find_elements_by_xpath(xpath_configuration["post_links"]).get_attribute("href"))

        post_links = wd.find_elements_by_xpath(
            xpath_configuration["post_links"]
        )

        if len(post_links) == 0:
            print("Cannot find new links. Terminating...")
            break

        for link in post_links:
            post_url = link.get_attribute("href")

            if link_filter in post_url:
                continue

            print(post_url)
            post_urls.append(post_url)

        page += 1
        if page > end_page:
            break
    
    print("FOUND "+str(len(post_urls)))
    return post_urls


def get_post_content_from_link(source="", post_link="", keyword=""):
    data = {
        "keyword": keyword,
        "url": "",
        "title": "",
        "content": "",
        "date": "",
        "author": "",
        # "tokenize_content": "",
        "comments": {}
    }
    data["url"] = post_link

    wd.get(post_link)

    try:
        title = wd.find_element_by_xpath(
            config[source]["xpath"]["title"]).get_attribute("innerHTML")
        data["title"] = title
    except Exception as e:
        print("Can't fetch title "+str(e))
        pass

    try:
        content = wd.find_element_by_xpath(
            config[source]["xpath"]["content"]).get_attribute("innerHTML")
        data["content"] = data_handler.prepare_content(content)
    except Exception as e:
        print("Can't fetch content "+str(e))
        pass

    try:
        date = wd.find_element_by_xpath(
            config[source]["xpath"]["date"]).get_attribute("innerHTML")
        data["date"] = date
    except Exception as e:
        print("Can't fetch date "+str(e))
        pass

    try:
        author = wd.find_element_by_xpath(
            config[source]["xpath"]["author"]).get_attribute("innerHTML")
        data["author"] = author
    except Exception as e:
        print("Can't fetch author "+str(e))

    try:
        post_id = post_link.split("-")[-1].replace(".html","")

        comments = requests.get(config[source]["comment_url"].format(post_id)).json()["data"]["items"]

        for comment in comments:
            comment_id = comment["comment_id"]
            comment_replies = requests.get(config[source]["reply_url"].format(comment_id)).json()["data"]["items"]
            comment["replys"]["items"] = comment_replies

        data["comments"] = comments
    except Exception as e:
        print("Can't fetch comment "+str(e))


    # try:
    #     try:
    #         viewmore_element = wd.find_element_by_xpath(config[source]["xpath"]["comment_viewmore"])
    #         wd.execute_script("arguments[0].click();", viewmore_element)
    #     except:
    #         print("Can't find viewmore comment element")

    #     while True:
    #         viewreply_elements = wd.find_elements_by_xpath(
    #             config[source]["xpath"]["comment_viewreply"]
    #         )
    #         for item in viewreply_elements:
    #             wd.execute_script("arguments[0].click();", item)

    #         try:
    #             nextpage_element = wd.find_element_by_xpath(config[source]["xpath"]["comment_nextpage"])
    #             wd.execute_script("arguments[0].click();", nextpage_element)            
    #             print(nextpage_element)
    #         except:
    #             print("END OF COMMENT PAGE")
    #             break

    # except Exception as e:
    #     print("Can't fetch comments "+str(e))
            

    # try:
    #     tokenize_content = data_handler.tokenize_content(data["content"])
    #     data["tokenize_content"] = tokenize_content
    # except Exception as e:
    #     print("Can't tokenize content "+str(e))
    #     pass

    return data


def crawl(source="", keyword="", offset=1, batch_size=1, exit_when_url_exist=True, use_elastic_search=True):
    print("STARTING CRAWLER")
    new_record = 0
    msg = ""
    from_page = offset
    end_page = from_page + batch_size - 1

    if use_elastic_search:
        if es.connection_is_available():
            new_links = get_new_links(
                source, keyword, from_page, end_page, exit_when_url_exist
            )
            print(new_links)
            for link in new_links:
                print("Getting content for "+link)
                post_data = get_post_content_from_link(
                    source=source, post_link=link, keyword=keyword)
                es.add_document(
                    es_index=config[source]["elastic_index"], data=post_data)
                new_record += 1
        else:
            msg = "Cannot connect to elastic search"
    else:
        while True:
            print("GETTING NEW LINKS")
            new_links = get_new_links(
                source, keyword, from_page, end_page, exit_when_url_exist
            )

            for link in new_links:
                print("Getting content for "+link)
                post_data = get_post_content_from_link(
                    source=source, post_link=link, keyword=keyword)
                # print(post_data)
                
                db.data(key=post_data["url"],value=post_data)

                # es.add_document(
                #     es_index=config[source]["elastic_index"], data=post_data)
                new_record += 1
            from_page += batch_size
            end_page += batch_size

    return {
        "new_record": new_record,
        "msg": msg
    }
