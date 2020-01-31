import sys
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from collections import deque
import time
import Script
import pickle

# finds tags of visible text inside the html
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# filters text from tags and finds title of url
def worker(url):
    workersoup = BeautifulSoup(requests.get(url).text, "html.parser")
    texts = workersoup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    final = u" ".join(t.strip() for t in visible_texts)
    tag = workersoup.find('title')
    for x in tag:
        title=(str(x))
    indexer.update(title, url, final)

# main
if __name__ == "__main__":
    # execution time
    start_time = time.time()
    numOfParameters = len(sys.argv)

    # initialize paramameters
    if(numOfParameters==1):
        startingPage="https://www.insomnia.gr/"
        pagesToCrawl=50
        keep=0
        numOfThreads=8
    else:
        parametersList = []
        # initialize command line parameters
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


    # pool of threads
    pool = Pool(cpu_count() * numOfThreads)

    # set of visited links
    visited = set([startingPage])

    # deque of links
    dq = deque([[startingPage, "", 0]])
    count=0

    if keep == 0:
        indexer = Script.Indexer()
    else:
        with open('indexer.pkl' , 'rb') as input:
            indexer = pickle.load(input)
    while dq:
        base, path, depth = dq.popleft()
        try:
            soup = BeautifulSoup(requests.get(base + path).text, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href not in visited:
                    if count < pagesToCrawl:
                        visited.add(href)
                        # print("  " * depth + f"at depth {depth}: {href}")

                        #assigns worker function to thread
                        results = pool.imap(worker,(href,))
                        if href.startswith("http"):
                            dq.append([href, "", depth + 1])
                        else:
                            dq.append([base, href, depth + 1])
                        count=count+1
                    else:
                        break

        except:
            pass
    with open('indexer.pkl' , 'wb') as output:
        pickle.dump(indexer,output,pickle.HIGHEST_PROTOCOL)


    # prints execution time
    # print("--- %s seconds ---" % (time.time() - start_time))