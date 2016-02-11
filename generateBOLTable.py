from getContent import getContent
from getURL import getURL
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

codeDescriptionList = [line.strip() for line in open("job_id_titles.txt", "r")]
#file = open("job_id_title_description", "w+")
for each_item in codeDescriptionList:
    index = each_item.index(',')
    code = each_item[:index].strip()
    jobtitles = each_item[index+1:]
    try:
        url = getURL(code)
        description = getContent(url)
        integerCode = int(code.replace('-', ''))
        #file.write(each_item + ',' + description + '\n')
        sql = """
            INSERT INTO SOC_JOBTITLE
            VALUES ('%d', '%s', '%s');
        """ % (integerCode, jobtitles.replace('\'', ''), description.replace('\'', ''))
        print sql
        cursor.execute(sql)
        db.commit()
    except ValueError:
        print "value err"

cursor.close()
db.close()
#file.close()