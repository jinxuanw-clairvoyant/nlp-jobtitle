from pprint import pprint
data1 = [line.strip() for line in open("onNetURL", 'r')]
with open("onNetJobTitles", 'r') as myfile:
    data2 = myfile.read().splitlines()