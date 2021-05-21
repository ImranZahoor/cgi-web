import cx_Oracle
con = cx_Oracle.connect('i73190', 'abc*2020', '172.31.0.11/STYLEDB')
cur = con.cursor()
cur.execute("Select  a.gi, a.freq_a, a.freq_c, a.freq_g, a.freq_t, a.freq_gc From beegenes a Where a.gi = 147907436")
row = cur.fetchone()
print(row)
cur.close()
con.close()