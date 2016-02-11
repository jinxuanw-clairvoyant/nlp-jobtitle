from bs4 import BeautifulSoup, Tag
import requests


def getContent(urlList):
    content = ""
    for url in urlList:
        soup = BeautifulSoup(requests.get(url[1]).content, "html.parser")
        if(url[0] == 1):
            divList = soup.findAll("", class_="moreinfo")
            tasksList = map(lambda x:x.contents[0].strip(), divList)
            taskStr = " ". join(tasksList)
            content += taskStr
        elif(url[0] == 2):
            ulList = soup.findAll("ul", class_="moreinfo")
            tasks = []
            for li in ulList[0].contents:
                if(isinstance(li, Tag)):
                    tasks.append(li.find(string = True).strip())
            taskStr = " ".join(tasks)
            content += taskStr
        else:
            raise ValueError("url type unknown")
    return content

