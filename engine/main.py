import utils.crawler_v2 as crawler
import time

begin = time.time()

print(crawler.crawl(source="https://ndh.vn",from_page=500,keyword="cổ phiếu",exit_when_url_exist=False))

end = time.time()

print("Done. Time taken: "+str(end-begin))