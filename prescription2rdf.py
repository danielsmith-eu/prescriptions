months = [u"201110", u"201111", u"201112", u"201201", u"201202", u"201203", u"201204", u"201205"] # to pick out filenames
rowid = 0 # for autoincrementd URIs
collate_seen = {} # dict to store URIs to prevent collated data from duplicating

def safeName(string):
    """ Turn a arbitrary predicate string into one safe for using in N3.

    """
    return string.replace(u" ",u"_")

def row2n3(row, thetype, handlers):
    """ Turn a row (a dict) into an N3 blob, and return the blob.

        thetype is the complete string of the type, so should be N3-safe.

        handlers is a dict of how to handle the data, see example.
        
    """
    global rowid
    rowid+=1
    uri = u":row{0}".format(rowid)
    out = u"{0} a {1} ;\n".format(uri, thetype)
    out2 = u""
    for key in row:

        if key in handlers:
            value = row[key]

            if len(value) == 0:
                continue

            if handlers[key]['type'] == u"uri":
                handled_value = u"{0}{1}".format(handlers[key]['uriprefix'], value)
            elif handlers[key]['type'] == u"int":
                handled_value = int(value)
            elif handlers[key]['type'] == u"float":
                handled_value = float(value)
            else:
                handled_value = u"\"\"\"{0}\"\"\"".format(value)

            if u"collate" in handlers[key]:
                collate_key = handlers[key]["collate"]
                collate_uri = u"{0}{1}".format(handlers[collate_key]["uriprefix"],row[collate_key])
                collate_predicate = handlers[key]["collate_predicate"]
                collate_type = handlers[key]["collate_type"]

                skip = False
                if u"collate_nodupe" in handlers[key]:
                    if collate_uri in collate_seen:
                        skip = True
                    collate_seen[collate_uri] = True

                if not skip:
                    out2 += u"{0} a {1} ;\n".format(collate_uri, collate_type)
                    out2 += u"  {0} {1} .\n".format(collate_predicate, handled_value)
            else:
                if u"predicate" in handlers[key]:
                    out += u"  {0} {1} ;\n".format(handlers[key]['predicate'],handled_value) 
        else:
            safekey = safeName(key)
            value = row[key]
            out += u"  pres:{0} \"\"\"{1}\"\"\" ;\n".format(safekey, value)

    out += u"  rdfs:label \"\"\"Prescription Data Row {0}\"\"\" .\n".format(rowid)
    return u"{0}\n{1}\n".format(out, out2)

""" Start writing the output with the prefixes.

"""
outf = open("prescription_data_all.n3", "w")
outf.write(u"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
outf.write(u"@prefix pres: <http://webbox.ecs.soton.ac.uk/ontology/prescriptions#> .\n")
outf.write(u"@prefix practice: <http://webbox.ecs.soton.ac.uk/ontology/prescription_practice#> .\n")
outf.write(u"@prefix pct: <http://webbox.ecs.soton.ac.uk/ontology/prescription_primary_care_trust#> .\n")
outf.write(u"@prefix bnf: <http://webbox.ecs.soton.ac.uk/ontology/prescription_bnf#> .\n")
outf.write(u"@prefix : <http://webbox.ecs.soton.ac.uk/ontology/prescription_data#> .\n\n")

def read_rows(f, header, thetype, handlers):
    global outf
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
            outf.write(row2n3(row, thetype, handlers).encode("utf-8"))
            outf.flush()

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

    f = open(rext)

    handlers = {
        u"NAME": {u"type": u"value", u"collate": u"PRACTICE", u"collate_predicate": u"practice:name", u"collate_type": u"practice:Practice"},
        u"ADDRESS": {u"type": u"value", u"collate": u"PRACTICE", u"collate_predicate": u"practice:address", u"collate_type": u"practice:Practice"},
        u"ADDRESS2": {u"type": u"value", u"collate": u"PRACTICE", u"collate_predicate": u"practice:address2", u"collate_type": u"practice:Practice"},
        u"CITY": {u"type": u"value", u"collate": u"PRACTICE", u"collate_predicate": u"practice:city", u"collate_type": u"practice:Practice"},
        u"COUNTY": {u"type": u"value", u"collate": u"PRACTICE", u"collate_predicate": u"practice:county", u"collate_type": u"practice:Practice"},
        u"POSTCODE": {u"type": u"value", u"collate": u"PRACTICE", u"collate_predicate": u"practice:postcode", u"collate_type": u"practice:Practice"},

        u"PERIOD": {u"type": u"value"}, # no predicate mean ignore
        u"PRACTICE": {u"type": u"uri", u"uriprefix": "practice:"},
        
    }

    header = [u"PERIOD",u"PRACTICE",u"NAME",u"ADDRESS",u"ADDRESS2",u"CITY",u"COUNTY",u"POSTCODE"]
    read_rows(f, header, u"practice:Practice", handlers)
    f.close()

outf.close()

