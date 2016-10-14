

def zliczenie(tablica):
    tab=[]
    a=0
    b=0
    slownik=dict()
    for elementy in tablica:
        while(elementy.find(';',b)!=-1):
            a=elementy.find(';',b)
            napis=elementy[b:a]
            b=a+1
            print(napis)
            if napis in slownik:
                slownik[napis]+=1
            else:
                slownik[napis]=1
        a=0
        b=0
    return slownik

def preparing(tab):
    a=0
    b=1
    tablica=[]
    tablica.append(['Co','Ile'])
    t=[]
    for element in tab:
        element=str(element)
        while(a!=-1):
            a=element.find(',',b)
            napis = element[b:a]
            b=a+1
            #t.append(napis)
            try:
                proba_zaminay_na_int = int(napis)
                t.append(proba_zaminay_na_int)
            except ValueError:
                t.append(napis)
        a=0
        b=1
        tablica.append(t)
        t=[]

    return tablica


sl={'Tak':0,'Nie':0}

y=["('1','Tak')","('2','Nie')"]

nowe=preparing(y)
print(nowe)
def preparing_data_for_column_chart(slownik,tablica):
    for klucz in slownik:
        for element in tablica:
            a= element[0].find(klucz)
            if(a!=-1):
                slownik[klucz]=element[1]
    return slownik
dane=preparing_data_for_column_chart(sl,y)
#print(dane)

a='2'

n=int(2)
print(n)