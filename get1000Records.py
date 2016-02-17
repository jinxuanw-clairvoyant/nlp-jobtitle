import re
import string

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import codecs
import time
import json

from requests.packages.urllib3.connection import ConnectionError

f = codecs.open('bullhorn.txt', encoding='utf-8', mode='r')

queryList = [line.strip() for line in f if line.strip() != '']
fileName = "Output"
countOfFile = 341
for query in queryList:
    originalQuery = query
    # query = filter(lambda x: x in string.printable, query)
    regex = re.compile('[\W_]+')
    query = regex.sub(' ', query)
    queryUsingPlus = query.strip().replace(' ', '+')
    #Replace it with google custom search API
    #googleResultGenerator = google.search('site:bullhornreach.com ' + query)

    print "current querying bullhorn" + query
    countOfGoogleResultInOnePage = 0
    customGoogleSearchURL="https://www.googleapis.com/customsearch/v1?key=AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU&cx=017136784574439370931:7teyiee9x6k&q="
    res = requests.get(customGoogleSearchURL + queryUsingPlus).content
    jsonRes = json.loads(res)
    fiveJobDescriptionStr = ""
    #for loop in json
    if 'items' not in jsonRes:
        continue
    for urlField in jsonRes["items"]:
        url =  urlField["link"]
        #visit the url, use beautifulSoup to extract the content
        try:
            page = requests.get(url).content
        except ConnectionError:
            pass
        soup = BeautifulSoup(page, "html.parser")
        reportSpamTag = soup.find('span', 'report-spam')
        if reportSpamTag != None:
            jobDescriptionTag = reportSpamTag.previous_sibling.find("div", class_="infrm")
            if jobDescriptionTag != None:
                jobDescription = jobDescriptionTag.findAll(text=True)
                oneJobDescriptionStr = " ".join([line.strip() for line in jobDescription if line.strip() != ""])
                fiveJobDescriptionStr += oneJobDescriptionStr + "\n"
                if oneJobDescriptionStr == "":
                    print "one job description is none"
            else:
                print "description tag not found"
        else:
            print "there is no spam tag"
        countOfGoogleResultInOnePage += 1

        if countOfGoogleResultInOnePage > 5:
            break
    if fiveJobDescriptionStr != "":
        file = codecs.open('./data/'+fileName + str(countOfFile), 'w', 'utf-8')
        file.write(originalQuery + '\n')
        file.write(fiveJobDescriptionStr)
        file.close()
        print "finish output " + str(countOfFile) + "for query " + originalQuery
        countOfFile+=1
    else:
        print "no match is found"

    # fileName = "Output" +str(countOfFile) + '.txt'
    # resultOfOneQuery = ""
    # JobTitle = query
    # for googleResultOfOneQuery in googleResultGenerator:
    #     print "current result is " + str(countOfGoogleResultInOnePage)
    #     if countOfGoogleResultInOnePage > 5:
    #         break
    #     if "bullhornreach" not in googleResultOfOneQuery:
    #         countOfGoogleResultInOnePage+=1
    #         continue
    #     else:
    #         bullHornPage = requests.get(googleResultOfOneQuery).content
    #         soup = BeautifulSoup(bullHornPage, 'html.parser')
    #         title = soup.find('h1', class_='jobtitle')
    #         if(title == None):
    #             continue
    #         else:
    #             [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    #             visible_text = soup.getText()
    #             resultOfOneQuery += filter(lambda x: x in string.printable, visible_text)
    #     countOfGoogleResultInOnePage+=1
    #
