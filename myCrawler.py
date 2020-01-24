import sys
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    numOfParameters = len(sys.argv)
    if(numOfParameters<3):
        print("Parameters Error")
        sys.exit()

    parametersList=[]
    for i in range (1, numOfParameters):
        parametersList.append(sys.argv[i])

    startingPage = requests.get(parametersList[0])
    pagesToCrawl = int(parametersList[1])
    if(len(parametersList)>2):
        numOfThreads = parametersList[2]

    soup = BeautifulSoup(startingPage.content, 'html.parser')
    print(soup.prettify())
    # a = int(sys.argv[1])
    # b = int(sys.argv[2])
    # print(a)
    # print(b)