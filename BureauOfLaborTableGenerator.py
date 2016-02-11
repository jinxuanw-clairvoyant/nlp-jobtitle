# This file will generate or write to a mySQL table which contains the job id of bureau of labor job titles, job titles
# name and its description from on*Net
import sys
import requests
import logging
from bs4 import BeautifulSoup
from bs4 import Tag
#
#Read in jobid.txt which contains the standard occuption classification as a list, in which each line is a job id.
socCodeList = [line.strip() for line in open("/Users/jinxuanwu/PycharmProjects/virtual_env/jobids.txt" ,"r")]

#The jobTitles in socCodeList don't have dash so we need to add it.
socCodeWithDash = [str(code)[0:2] + "-" + str(code[2:]) for code in socCodeList]

#onNet url
onNetURLPart = "http://www.onetonline.org/link/result/"
onNetURLQueryPartType1 = ".00?c=tk&n_tk=10&e_tk=1&c_tk=50&s_tk=IM&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_cx=10&c_cx=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go"
onNetURLQueryPartType2 = ".00?c=ta&n_ta=0&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_wc=10&c_wc=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go"

#Use request to fetch data
taskList = []
#Open the link of the urlList, use beautifulSoup to get the contents.
count = 0
#This method takes in a url and return

# Method to extract correct url, takes in the soc code and generate a url or a list of url of their corresponding
# location in on*Net
#The only way to check whether the url is correct is use Beautiful Soup to parse the url and find the task tab.





for code in socCodeWithDash:
    webPage = requests.get(onNetURLPart + code + onNetURLQueryPartType1).content
    soup = BeautifulSoup(webPage, "html.parser").findAll("", class_="moreinfo")
    if(soup == []):
        url = onNetURLPart + code + onNetURLQueryPartType2
        webPage = requests.get(url).content
        ulList = BeautifulSoup(webPage, "html.parser").find_all("ul", class_="moreinfo")
        tasks = []
        if(len(ulList) == 0):
            print code
        else:
            for li in ulList[0].contents:
                if(isinstance(li, Tag)):
                    tasks.append(li.find(string = True).strip())
            tasks = ", ".join(tasks)
            taskList.append(tasks)
            print tasks
    else:
        tasksList = map(lambda x:x.contents[0].strip(), soup)
        tasks = " ". join(tasksList)
        taskList.append(tasks)
        print tasks

assert(len(taskList) == 840)


