import utils.crawler as crawler
import time

begin = time.time()

print("STARTING")

crawler.crawl(source="https://vnexpress.net",keyword="", offset=1, batch_size=5,exit_when_url_exist=False, use_elastic_search=False)

end = time.time()

print("Done. Time taken: "+str(end-begin))