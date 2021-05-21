#!/usr/bin/env python3
import cgi
import cx_Oracle


def main():
    form = cgi.FieldStorage()
    file_name = form.getfirst("file_name", "")
    # print(file_name)
    contents = processInput(file_name)
    print(contents)


def processInput(thefile):
    con = cx_Oracle.connect('i73190', 'abc*2020', '172.31.0.11/STYLEDB')
    cur = con.cursor()
    cur.execute('drop table beegenes')
    cur.execute('''create table beegenes(
                gi number,
                sequence clob,
                freq_A number,
                freq_C number,
                freq_G number,
                freq_T number,
                freq_GC number
                )''')
    cur.bindarraysize = 50
    
    # # read raw data from a file
    # infile = open(thefile, "r")
    # mystr = ""
    # finalstr = ''
    # # form a string with the raw data
    # for aline in infile:
    #     mystr = mystr+aline

    # # form a continuous string
    # strL = mystr.replace('\n', '')
    # # change the string into a list, one protein per list item
    # aList = strL.split('>')
    # # keep the list items that contian the substring,[Apis mellifera]

    # for anItem in aList:
    #     if 'Apis mellifera' in anItem:
    #         s = anItem.find('mRNA')+4
    #         findstr = anItem[:s]+"_**gene_seq_starts_here**_"+anItem[s:]
    #         finalstr = finalstr+findstr
    # end = 0
    # totalLength = len(finalstr)
    # repitions = finalstr.count('Apis mellifera')

    # # extract the target substrings, the gi number and the protein sequence
    # for i in range(repitions):
    #     start = finalstr.find('gi|', end)+3
    #     end = finalstr.find('|', start)
    #     gi = finalstr[start: end]
    #     start = finalstr.find('mellifera', end)+10
    #     end = finalstr.find('gi|', start)
    #     if end == -1:
    #         end = totalLength
    #     seq = finalstr[start:end]
    #     seqLength = len(seq)
    #     freq_A = seq.count('A')/float(seqLength)
    #     freq_C = seq.count('C')/float(seqLength)
    #     freq_G = seq.count('G')/float(seqLength)
    #     freq_T = seq.count('T')/float(seqLength)
    #     freq_GC = (seq.count('G')+seq.count("C"))/float(seqLength)
    contents = ""
    with open("honeybee_gene_sequences.txt") as f:
        contents = f.read()
        contents = contents.split(">")[1:]        
    seq_size = findMax(contents)
    cur.setinputsizes(50, seq_size, float, float, float, float, float) 
    for c in contents:
        single_gene = c.split("\n")
        gi = single_gene[0].split("|")[1]
        seq = ''.join(single_gene[1:])
        total_count = len(seq)
        freq_A = (seq.count('A')/total_count)
        freq_C = (seq.count('C')/total_count)
        freq_G = (seq.count('G')/total_count)
        freq_T = (seq.count('T')/total_count)
        freq_GC = (freq_G + freq_C)
        cur.execute('''insert into beegenes (gi,sequence,freq_A,freq_C,freq_G,freq_T,freq_GC) values(:v1,:v2,:v3,:v4,:v5,:v6,:v7)''',
                    (gi, seq, freq_A, freq_C, freq_G, freq_T, freq_GC))
    con.commit()
    cur.close()
    con.close()

    return makePage('upload_done_template.html', ("Thank you for uploading"))


def fileToStr(fileName):
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents


def makePage(template, subst):
    pageTemplate = fileToStr(template)
    return pageTemplate % subst


def findMax(contents):
    n_list = []
    for c in contents:
        c = ''.join(c.split("\n")[1:])
        n_list.append(c)
    return len(max(n_list, key=len))


if __name__ == "__main__":
    try:
        print("Content-type: text/html\n\n")
        main()
    except:
        cgi.print_exception()
