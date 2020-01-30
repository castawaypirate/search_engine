import sys
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count
from collections import deque
import time


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def worker(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    final = u" ".join(t.strip() for t in visible_texts)
    tag = soup.find('title')
    for x in tag:
        title=(str(x))
    l.append(final)

if __name__ == "__main__":
    start_time = time.time()

    numOfParameters = len(sys.argv)
    if(numOfParameters==1):
        startingPage="http://toscrape.com"
        pagesToCrawl=50
        keep=0
        numOfThreads=8
    else:
        parametersList = []
        for i in range(1, numOfParameters):
            parametersList.append(sys.argv[i])

        # starting page
        startingPage = parametersList[0]

        # number of pages to crawl
        pagesToCrawl = int(parametersList[1])

        # 0 doesnt keep data from previous crawl, 1 keeps it
        keep = int(parametersList[2])

        # number of threads
        if (len(parametersList) > 3):
            numOfThreads = int(parametersList[3])
        else:
            numOfThreads=1


    pool = Pool(cpu_count() * numOfThreads)
    visited = set([startingPage])
    dq = deque([[startingPage, "", 0]])
    count=0
    l=[]
    while dq:
        base, path, depth = dq.popleft()
        #                         ^^^^ removing "left" makes this a DFS (stack)
        try:
            soup = BeautifulSoup(requests.get(base + path).text, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href not in visited:
                    if count < pagesToCrawl:
                        visited.add(href)
                        print("  " * depth + f"at depth {depth}: {href}")
                        results = pool.imap(worker,(soup,))
                        if href.startswith("http"):
                            dq.append([href, "", depth + 1])
                        else:
                            dq.append([base, href, depth + 1])
                        count=count+1
                    else:
                        break

        except:
            pass



    time.sleep(2)
    for item in l:
        print(item)
    print("--- %s seconds ---" % (time.time() - start_time))