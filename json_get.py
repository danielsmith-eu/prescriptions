import urllib

url_template = "http://www.openbnf.org/api/?drug={0}"

counter = 0
f = open("distinct_drugs.txt", "r")
for line in f.readlines(): 
    line = line.rstrip()
    if '(' in line:
        line = line[:line.find('(')]
        line = line.rstrip()
    url = url_template.format(urllib.quote(line))
    counter += 1
    print 'wget -O drugs/{0}.json \'{1}\''.format(counter,url)
