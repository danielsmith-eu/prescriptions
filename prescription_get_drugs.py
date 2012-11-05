months = [u"201109", u"201110", u"201111", u"201112", u"201201", u"201202", u"201203", u"201204", u"201205", u"201206", u"201207"] # to pick out filenames
rowid = 0 # for autoincrementd URIs
collate_seen = {} # dict to store URIs to prevent collated data from duplicating

def safeName(string):
    """ Turn a arbitrary predicate string into one safe for using in N3.

    """
    return string.replace(u" ",u"_")


file_count = 0
lines_count = 0

done = {}

def read_rows(f, header, thetype, handlers):
    global done
    for line in f.readlines():
        line = line.rstrip()
        fields = line.split(u",")
        cleanfields = []
        for field in fields:
            cleanfield = field.lstrip()
            cleanfield = cleanfield.rstrip()
            cleanfields.append(cleanfield)

        if header is None:
            header = cleanfields
        else:
            row = {}
            for i in range(len(cleanfields)):
                key = header[i]
                value = cleanfields[i]
                row[key] = value

            bnfname = row['BNF NAME']
            if bnfname not in done:
                done[bnfname] = True
                print row['BNF NAME']



for month in months:
    # prescription data
    iext = u"T{0}PDP%20IEXT.CSV".format(month)
    # practice data
    rext = u"T{0}ADD%20REXT.CSV".format(month)

    f = open(iext)

    handlers = {
        u"PRACTICE": {u"predicate": u"pres:practice", u"type": u"uri", u"uriprefix": u"practice:"},
        u"ITEMS": {u"predicate": u"pres:items", u"type": u"int"},
        u"NIC": {u"predicate": u"pres:net_item_cost", u"type": u"float"},
        u"ACT COST": {u"predicate": u"pres:act_cost", u"type": u"float"},
        u"BNF CODE": {u"predicate": u"pres:bnf_code", u"type": u"uri", u"uriprefix": u"bnf:"},
        u"PCT": {u"predicate": u"pres:pct", u"type": u"uri", u"uriprefix": u"pct:"},
        u"BNF NAME": {u"type": u"value", u"collate": u"BNF CODE", u"collate_predicate": u"rdfs:label", u"collate_type": u"bnf:formulation", u"collate_nodupe": True},
    }

    header = None
    read_rows(f, header, u":Prescription_Row", handlers)
    f.close()



