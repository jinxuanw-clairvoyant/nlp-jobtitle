import string

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import codecs
import time
import google
f = codecs.open('bullhorn.txt', encoding='utf-8', mode='r')

queryList = [line.strip() for line in f if line.strip() != '']

countOfFile = 0
for query in queryList:
    #Change
    query = filter(lambda x: x in string.printable, query)
    googleResultGenerator = google.search('bullhorn ' + query)
    print "current querying bullhorn" + query
    countOfGoogleResultInOnePage = 0
    fileName = "Output" +str(countOfFile) + '.txt'
    resultOfOneQuery = ""
    JobTitle = ""
    for googleResultOfOneQuery in googleResultGenerator:
        print "current result is " + str(countOfGoogleResultInOnePage)
        if countOfGoogleResultInOnePage > 5:
            break
        time.sleep(1)
        if "bullhornreach" not in googleResultOfOneQuery:
            countOfGoogleResultInOnePage+=1
            continue
        else:
            bullHornPage = requests.get(googleResultOfOneQuery).content
            soup = BeautifulSoup(bullHornPage, 'html.parser')
            title = soup.find('h1', class_='jobtitle')
            if(title == None):
                continue
            else:
                JobTitle = title.text
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                visible_text = soup.getText()
                resultOfOneQuery += filter(lambda x: x in string.printable, visible_text)
                break
        countOfGoogleResultInOnePage+=1

    if resultOfOneQuery.strip() != "":
        file = codecs.open('./data/'+fileName, 'w', 'utf-8')
        file.write(JobTitle + '\n')
        file.write(resultOfOneQuery)
        file.close()
        countOfFile+=1
    else:
        print "no match is found"