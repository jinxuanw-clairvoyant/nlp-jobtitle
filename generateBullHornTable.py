#This file is used to generate the table
# -*- coding: UTF-8 -*-

import MySQLdb

# mySQLUrl = "unnatis-macbook-pro.local"#"localhost"
# userName = "jinxuan"#"root"
# passwd = "jinxuan"#"8269202"
# DBName = "bullhorn"#"job_title"

mySQLUrl = "localhost"
userName = "root"
passwd = "8269202"
DBName = "bullhorn"

db = MySQLdb.connect(mySQLUrl, userName, passwd, DBName, charset='utf8', use_unicode=True)
cursor = db.cursor()

filePrefix = "jOutput"

for i in range(0,6):
    filename = filePrefix + str(i)

    file = open("./data/" + filename + '.txt', 'r')
    fileContent = file.read()
    content_index = fileContent.index('\n')
    bullHornjobTitle = fileContent[0:content_index]
    bullhornDescription = fileContent[content_index:].replace('\'', '')
    sql = """
        INSERT INTO bullhorn (bullhorn_job_title, bullhorn_job_desc)
        VALUES (%s, %s)
        """
    print sql
    cursor.execute(sql, (bullHornjobTitle, bullhornDescription))
    db.commit()


cursor.close()
db.close()

