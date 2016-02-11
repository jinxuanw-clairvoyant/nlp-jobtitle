from unittest import TestCase

from getURL import getURL


class TestGetURL(TestCase):
    # def test_getURLType3(self):
    #     codeList = ["11-3031", "11-3071", "11-9013", "13-1031", "13-1041", "13-2011", "13-2021", "17-2111", "17-2121", "17-3011", "17-3012", "17-3019", "17-3023", "17-3029", "17-3031", "19-1029", "19-1031", "19-3031", "19-3039", "19-3091", "19-4011", "19-4041", "19-4051", "21-1019", "21-1029", "25-1069", "25-2059", "27-1019", "27-1029", "27-2012", "27-2041", "27-2042", "27-3043", "29-1029", "29-1069", "29-1129", "33-1021", "33-2011", "33-2021", "33-3021", "33-3051", "35-2019", "37-2019", "37-3019", "39-3019", "41-3031", "43-3021", "43-4031", "43-4041", "43-5081", "43-9041", "45-1011", "45-2092", "45-4029", "47-2031", "47-2152", "47-3019", "47-5049", "49-3023", "49-9021", "49-9069", "51-4121", "51-9071", "51-9195", "53-5021", "53-6051"]
    #     for code in codeList:
    #         try:
    #             print getURL(code)
    #         except ValueError:
    #             print code

    def test_getURLWhole(self):
        codeList = [line.strip() for line in open("/Users/jinxuanwu/PycharmProjects/virtual_env/jobids.txt", "r")]
        for code in codeList:
            try:
                print getURL(str(code)[0:2] + "-" + str(code[2:]))
                print "--------------------"
            except ValueError:
                print code