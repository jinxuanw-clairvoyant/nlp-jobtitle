import requests
from pprint import pprint
from bs4 import BeautifulSoup, Tag


def getURL(code):
    if (len(code) == 7):
        code = code + ".00"
    elif(len(code) == 10):
        code
    else:
        print code
        raise ValueError('A very specific bad thing happened')
    onNetURLPart = "http://www.onetonline.org/link/result/"
    onNetURLQueryPartType1 = "?c=tk&n_tk=0&e_tk=1&c_tk=50&s_tk=IM&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_cx=10&c_cx=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go"
    onNetURLQueryPartType2 = "?c=ta&n_ta=0&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_wc=10&c_wc=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go"
    #Type 1
    url = onNetURLPart + code + onNetURLQueryPartType1
    webPage = requests.get(url).content
    divList = BeautifulSoup(webPage, 'html.parser').findAll("div", class_="moreinfo")
    if(len(divList) != 0):
        return [(1, url)]
    #Type 2
    url = onNetURLPart + code + onNetURLQueryPartType2
    webPage = requests.get(url).content
    ulList = BeautifulSoup(webPage, 'html.parser').findAll("ul", class_="moreinfo")
    if(len(ulList) != 0):
        return [(2, url)]
    #Type 3, should return a list of url
    url = []
    optionDiv = BeautifulSoup(webPage, 'html.parser').findAll("div", class_="exclist")
    if(len(optionDiv) > 0):
        for execitem in optionDiv[0].contents:
            if isinstance(execitem, Tag):
                code = execitem.find(string= True)
                if code == ".":
                    continue
                else:
                     #remove utf-8 space, http://stackoverflow.com/questions/10993612/python-removing-xa0-from-string
                    url.append(getURL(code.replace(u'\xa0', u'').strip())[0])
    else:
        raise ValueError('The code %s is unable to be processed', code)
        return (-1, "")
    return url
