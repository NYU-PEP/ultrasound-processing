#!/usr/bin/python
# Concatenates .con files from EdgeTrak to a csv or tsv format that
# is the input of the SSANOVA script used at NYU.
# Daniel Szeredi 2014


import argparse
import os
import re
import string

def readCon(filename):
    "Reads in a .con file, returns a list with {x,y} dictionaries"
    F = open(filename,"rt")
    rv = []
    for line in F:
        xy = re.match(r"(\S*)\s*(\S*)",line.strip())
        if not xy:
            print "File read error in %s" % filename
            return []
        rv.append({"x": xy.group(1), "y": xy.group(2)})
    F.close()
    return rv

def parseFileName(filename):
    """Parses the .con filename to a dictionary of the variables coded in that file name
    Uses the SUBJECT_REPETITION_WORD_FRAME format, where WORD may contain extra underscores."""

    m = re.match(r"(.+)\_(\d+)\_(.+)\_(\d+)\.con",f)
    if not m:
        print "File name parse error: %s" % filename
        return False
    return [
        m.group(1), #subject
        m.group(3), #word
        int(m.group(4)), #time.frame
        int(m.group(2)), #repetition
    ]

def parseFileNameAllUnderscores(filename):
    filename = filename[:-4] # chop off .con
    return filename.split("_")


#parse args
parser = argparse.ArgumentParser(prog="python conconcatenate.py", description="Concatenate .con files from EdgeTrak to a table format readable by th e SSANOVA script in the NYU PEP lab.")
parser.add_argument("directory", default=".", nargs="?", help="The directory where the .con files are found. Defaults to the current directory")
#parser.add_argument("-s", "--stimuli", nargs="?", help="An optional file containing the stimuli list as a CSV. If used, words in the first column on the stimuli file will be replaced with what is found in the second column.")
parser.add_argument("-f", "--format", choices=["tsv","csv"], help="The output format: tab separated (default) or comma separated.", default="tsv")
parser.add_argument("-a", "--all-underscores", help="Separate filenames using all underscores and store each field in a separate column. Without this flag, the program"
                    " expects a SUBJECT_REPETITION_WORD_FRAME format, where WORD may contain extra underscores.", action="store_true")
parser.add_argument("--suffix", help="The suffix on the results file name which looks like SUBJECT_SUFFIX.{csv,txt}. Defaults to \"results\".", default="results")
args = vars(parser.parse_args())

files = [n for n in os.listdir(args["directory"]) if re.search(r"\.con$",n)] # ls *.con
outfiles = {} # files dictionary, keys = subject names, values = file objects
sepchar = "\t"
for f in files:
    if args["all_underscores"]:
        fnattr = parseFileNameAllUnderscores(f)
    else:
        fnattr = parseFileName(f)
    if not fnattr:
        continue
    xy = readCon(f)
    if fnattr[0] not in outfiles.keys(): # create the new subject file, fnattr[0] is the key (subject name)
        fn = fnattr[0] + "_" + args["suffix"]
        if args["format"] == "csv":
            fn = fn + ".csv"
            sepchar = ","
        else:
            fn = fn + ".txt"
        outfiles[fnattr[0]] = open(fn, "wt")

    for i in range(len(xy)): # print out all the xy's to the subject's results file
        info = [xy[i]["x"], xy[i]["y"]]
        info += [str(x) for x in fnattr[1:]] # merge the xy info with the file info
        s = sepchar.join(info) + "\n" # create tab/comma separated string
        outfiles[fnattr[0]].write(s)

for f in outfiles:
    outfiles[f].close()


