# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:27:45 2021

@author: wzq
"""

import cgi
import cx_Oracle


def main():
    form = cgi.FieldStorage()
    theStr = form.getfirst("theList", "")
    contents = processinput(theStr)
    print(contents)


def processinput(thefile):
    con = cx_Oracle.connect('SYSTEM/0601')
    cur = con.cursor()
    cur.execute('drop table beegenes')
    cur.execute('''create table beegenes(
                gi varchar2(10),
                sequence clob,
                freq_A number,
                freq_C number,
                freq_G number,
                freq_T number,
                freq_GC number
                )''')
    cur.bindarraysize = 50
    cur.setinputsizes(10, 9000, float, float, float, float, float)
    # read raw data from a file
    infile = open(thefile, "r")
    mystr = ""
    finalstr = ''

    # form a string with the raw data
    for aline in infile:
        mystr = mystr+aline

    # form a continuous string
    strL = mystr.replace('\n', '')

    # change the string into a list, one protein per list item
    aList = strL.split('>')

    # keep the list items that contian the substring,[Apis mellifera]

    for anItem in aList:
        if 'Apis mellifera' in anItem:
            s = anItem.find('mRNA')+4
            findstr = anItem[:s]+"_**gene_seq_starts_here**_"+anItem[s:]
            finalstr = finalstr+findstr
    end = 0
    totalLength = len(finalstr)
    repitions = finalstr.count('Apis mellifera')

    # extract the target substrings, the gi number and the protein sequence
    for i in range(repitions):
        start = finalstr.find('gi|', end)+3
        end = finalstr.find('|', start)
        gi = finalstr[start: end]
        start = finalstr.find('mellifera', end)+10
        end = finalstr.find('gi|', start)
        if end == -1:
            end = totalLength
        seq = finalstr[start:end]

        seqLength = len(seq)
        freq_A = seq.count('A')/float(seqLength)
        freq_C = seq.count('C')/float(seqLength)
        freq_G = seq.count('G')/float(seqLength)
        freq_T = seq.count('T')/float(seqLength)
        freq_GC = (seq.count('G')+seq.count("C"))/float(seqLength)

        cur.execute('''insert into beegenes (gi,sequence,freq_A,freq_C,freq_G,freq_T,freq_GC) values(
                    :v1,:v2,:v3,:v4,:v5,:v6,:v7)''', (gi, seq, freq_A, freq_C, freq_G, freq_T, freq_GC))

        con.commit()

        cur.close()
        con.close()

        return makePage('done_submission_template.html', ("Thank you for uploading"))


def filetostr(fileName):
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents


def makePage(templateFileName, substitutions):
    pageTemplate = filetostr(templateFileName)
    return pageTemplate % substitutions


try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()
