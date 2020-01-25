import sys
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


if __name__ == "__main__":
    numOfParameters = len(sys.argv)
    if(numOfParameters<4):
        print("Parameters Error")
        sys.exit()

    parametersList=[]
    for i in range (1, numOfParameters):
        parametersList.append(sys.argv[i])

    # starting page
    startingPage = requests.get(parametersList[0])
    # number of pages to crawl
    pagesToCrawl = int(parametersList[1])
    # 0 doesnt keep data from previous crawl, 1 keeps it
    keep = int(parametersList[2])
    # number of threads
    if(len(parametersList)>3):
        numOfThreads = parametersList[3]

    soup = BeautifulSoup(startingPage.content, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    # for l in links:
    #     print(l)
    final = u" ".join(t.strip() for t in visible_texts)
    print(final)
    print(type(final))
    # a = int(sys.argv[1])
    # b = int(sys.argv[2])
    # print(a)
    # print(b)