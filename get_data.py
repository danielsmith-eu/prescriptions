import urllib2, re, os, sys, shutil

src = "http://www.ic.nhs.uk/services/transparency/prescribing-by-gp-practice--chemical-level-data"
link_match = r'<a title="datagov.ic.nhs.uk/T.*?\.CSV" href="(http://datagov.ic.nhs.uk/)(T.*?\.CSV)" target="_blank">'

f = urllib2.urlopen(src)
src_page = f.read()

def download_file(url, file_name, f):
    print "Downloading: {0}".format(url)
    u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,


matches = re.findall(link_match, src_page)
for match in matches:
    data_url = "".join(match)
    result_csv = match[1]

    # if the CSV already exists, then don't download this source EXE (ZIP)
    if not os.path.exists(result_csv):
        fout = open(result_csv, "wb")
        download_file(data_url, result_csv, fout)
        fout.close()

