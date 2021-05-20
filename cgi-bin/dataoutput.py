# -*- coding: utf-8 -*-
"""
Created on Sun May 16 23:50:24 2021

@author: wzq
"""

import scipy as sp
import cgi
import cx_Oracle

def main():
    contents = processInput()
    print(contents)
    
def processInput():
    con = cx_Oracle.connect('SYSTEM/0601')
    cur = con.cursor()
    aaList = ['A','C','G','T']
    fList = [() for t in range(4)]
    for i in range(4):
        myDict = {'aa':aaList[i]}
        obj=cur.execute('''select gi, freq_%(aa)s from beegenes,(select max(freq_%(aa)s)
                        as max%(aa)s from beegenes) where freq_%(aa)s=max%(aa)s''' % myDict)
        for x in obj:
            fList[i]=x
            
    myTuple = ()
    for t in range(4):
        myTuple = myTuple + fList[t]
    cur.close()
    con.close()
    
    return makePage('see_result_template.html',myTuple)

def fileToStr(fileName):
    fin = open(fileName);
    contents = fin.read();
    fin.close()
    return contents

def makePage(templateFileName,substitutions):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitutions

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()