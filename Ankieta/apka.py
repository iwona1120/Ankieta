import pymysql
import glob,os
conn = pymysql.connect(host='mysql.agh.edu.pl', user='stuglik', passwd='01ce02la', db='stuglik', port=3306)
cur = conn.cursor()



j= 0
Czynnosc = {'bieg': 1,
            'chód': 2,
            'siedzenie': 3,
            'upadek': 4,
            }

path ='C:/Users/Iwona/Desktop/danetelemedycyna'
for filename in os.listdir(path):
  #filename = filename.replace('\\','/')

  f = path +'/'+filename
  #print(f)
  fn = filename.lower()
  id = Czynnosc[fn]
  id = str(id)
  #print(Czynnosc[fn])

  idosoby = 1
  idosoby =str(idosoby)
  for file in glob.glob(os.path.join(f, '*.txt')):
    file = file.replace('\\','/')
    #print(file)
    j = j+1
    plik = open(file)
    Czas = ''
    X = ''
    Y = ''
    Z = ''

    i = 0
    #print(plik)

    for wiersz in plik:
      #print(wiersz)
      if (i >= 2):
          a = wiersz.split('\t')
          #print(a[0])
          Czas = Czas + a[0] + ';'
          X = X + a[1] + ';'
          Y = Y + a[2] + ';'
          Z = Z + a[3] + ';'
      i = i + 1
    #print(X)
    #try:
    sql = "INSERT INTO Sygnaly(idOsoby,IdCzynnosci, Czas, X, Y, Z) VALUES ('" + idosoby + "','"+ id + "' , '" + Czas + "','" + X + "','" + Y + "','" + Z + "');"
    cur.execute(sql)
    #except:
     #   print('Bład połaczenia z bazą')
    #print(sql)
    a = int(idosoby)+1
    idosoby = str(a)

print(j)

cur.close()
conn.close()