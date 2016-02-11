dict = set(line.strip() for line in open("jobids.txt", 'r'))

with open("DOL.txt", "r") as file:
    lines = file.read().splitlines()
    result = []
    print "Below is the job titles we're not going to process"
    for line in lines:
        if(line.split(",")[0].replace("-", "").strip() in dict):
            result.append(line)
        else:
            print line

file = open("job_id_titles.txt", "w+")

file.writelines(["%s\n" % line for line in result])

file.close()