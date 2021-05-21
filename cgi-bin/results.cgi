#!/usr/bin/env python3
import scipy as sp
import cgi
import cx_Oracle


def main():
    contents = processInput()
    print(contents)


def processInput():
    con = cx_Oracle.connect('i73190', 'abc*2020', '172.31.0.11/STYLEDB')
    cur = con.cursor()
    aaList = ['A', 'C', 'G', 'T']
    desc = {'A': 'Adenine', 'C': 'Cytosine', 'G': 'Guanine', 'T': 'Thymine'}
    fList = {}
    row = ""
    for i in range(4):
        myDict = {'aa': aaList[i]}
        obj = cur.execute('''select gi, freq_%(aa)s from beegenes,(select max(freq_%(aa)s)
                        as max%(aa)s from beegenes) where freq_%(aa)s=max%(aa)s''' % myDict)
        for x in obj:
            fList[aaList[i]] = x

    for key in fList.keys():
        row += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(desc[key],
                                                                              key, fList[key][0], fList[key][1])
    cur.close()
    con.close()
    return makePage('out_template.html', row)


def fileToStr(fileName):
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents


def makePage(template, sub):
    pageTemplate = fileToStr(template)
    return pageTemplate % sub


try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()
