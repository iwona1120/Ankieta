from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
def zliczenie(tablica):
    tab=[]
    a=0
    b=2
    slownik=dict()
    for elementy in tablica:
        elementy=str(elementy)
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
        b=2
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

def preparing_data_for_column_chart(tablica_do_porownania,tablica_z_bazy,kogo_dotyczy):
    tab=[]
    tab.append(kogo_dotyczy)
    for klucz in tablica_do_porownania:
        for element in tablica_z_bazy:
            a= element[1].find(klucz)
            if(a!=-1):
                tab.append(element[0])
            else:
                tab.append(0)
    return tab

#import statistics
import urllib
from sqlalchemy import func
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daneform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'daneform'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    male = db.Column(db.String)
    student = db.Column(db.String)
    familyplace = db.Column(db.String)
    free_time_in_week = db.Column(db.String)
    free_time_without_weekend = db.Column(db.String)
    most_of_free_time_in_day = db.Column(db.String)
    responsibilities = db.Column(db.String)
    friends = db.Column(db.String)
    with_who_are_you_living = db.Column(db.String)
    single_room = db.Column(db.String)
    where_social_meetings = db.Column(db.String)
    accounts = db.Column(db.String)
    using_accounts = db.Column(db.String)
    like_doing = db.Column(db.String)
    active_time = db.Column(db.String)
    using_computer = db.Column(db.String)
    how_much_money = db.Column(db.String)
    from_money = db.Column(db.String)
    your_money = db.Column(db.String)
	
    def __init__(self, male, student, FamilyPlace, FreeTimeInWeek , FreeTimeWithoutWeekend,MostOfFreeTimeInDay,Responsibilities, Friends, WithWhoAreYouLiving, SingleRoom, WhereSocialMeetings, Acounts,UsingAcounts ,LikeToDo, ActiveTime , UsingComputer ,  HowMuchMoney, FromMoney, YourMoney):

        self.male = male
        self.student = student
        self.familyplace = FamilyPlace
        self.free_time_in_week = FreeTimeInWeek
        self.free_time_without_weekend = FreeTimeWithoutWeekend
        self.most_of_free_time_in_day = MostOfFreeTimeInDay
        self.responsibilities = Responsibilities
        self.friends = Friends
        self.with_who_are_you_living = WithWhoAreYouLiving
        self.single_room  = SingleRoom
        self.where_social_meetings = WhereSocialMeetings
        self.accounts = Acounts
        self.using_accounts = UsingAcounts
        self.like_doing= LikeToDo
        self.active_time =  ActiveTime
        self.using_computer = UsingComputer
        self.how_much_money = HowMuchMoney
        self.from_money  = FromMoney
        self.your_money  = YourMoney

db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/moje")
def show_moje():
    fd_k = db.session.query(Formdata).filter(Formdata.male == "K").count()
    fd_m = db.session.query(Formdata).filter(Formdata.male == "M").count()

    daneplec = [['Płeć', 'Ilość'], [' Kobiety', fd_k], ['Mezczyzni', fd_m]]

    fd_stu1 = db.session.query(Formdata).filter(Formdata.student == "I").count()
    fd_stu2 = db.session.query(Formdata).filter(Formdata.student == "II").count()
    fd_stu3 = db.session.query(Formdata).filter(Formdata.student == "III").count()
    fd_stu4 = db.session.query(Formdata).filter(Formdata.student == "IV").count()
    fd_stu5 = db.session.query(Formdata).filter(Formdata.student == "V").count()

    danerok = [['Który rok','Ilość'],['Student I roku', fd_stu1], ['Student II roku', fd_stu2], ['Student III roku', fd_stu3],
                   ['Student IV roku', fd_stu4], ['Student V roku', fd_stu5]]

    return render_template('moje.html',daneplec=daneplec, danerok=danerok)

@app.route("/jak")
def show_jak():
    # wykres zainteresowania dla wszystkich
    zainteresowania = db.session.query(Formdata.like_doing)
    n = zliczenie(zainteresowania)
    Like = []
    Like.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Like.append([el, n[el]])

    # wykres aktywny czas dla wszytkich
    kontaportale = db.session.query(Formdata.active_time)
    n = zliczenie(kontaportale)
    Active = []
    Active.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Active.append([el, n[el]])

    # wykres aktywny czas dla wszytkich
    co_komputer = db.session.query(Formdata.using_computer)
    n = zliczenie(co_komputer)
    Computer = []
    Computer.append(['Używanie komputera', 'Ile osob'])
    for el in n:
        Computer.append([el, n[el]])

    return render_template('jak.html',Like=Like, Active = Active, Computer=Computer)

@app.route("/ilenasocial")
def show_ilenasocial():

    #dane do wykresu ile czasu studenci poswiecaja na social media z podzialem na plec
    tablica_using_accouts = ['do godziny', '1-3 godziny', '4-5 godzin', 'wiecej niż 5 godzin']
    # kobiety
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.male == "K"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    using_accounts_w_ = preparing_data_for_column_chart(tablica_using_accouts, query, 'Kobiety')

    # mezczyzni
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.male == "M"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    using_accounts_m = preparing_data_for_column_chart(tablica_using_accouts, query, 'Meżczyźni')

    tablica_using_accouts.insert(0, "Plec")
    Using_Accounts_gender = [tablica_using_accouts, using_accounts_w_, using_accounts_m]

    return render_template('ilenasocial.html',Using_Accounts_gender=Using_Accounts_gender)

@app.route("/utrzymanie")
def show_utrzymanie():
    fd_10 = db.session.query(Formdata).filter(Formdata.how_much_money == "mniej niż 10 zł").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.how_much_money == "10-30 zł").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.how_much_money == "30-50 zł").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.how_much_money == "50-100 zł").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.how_much_money == "więcej niż 100 zł").count()

    danewykres4 = [['jaka kwota', 'ile osob'], ['mniej niż 10 zł', fd_10], ['10-30 zł', fd_30], ['30-50 zł', fd_50],
                   ['50-100 zł', fd_100], ['więcej niż 100 zł', fd_moremoney]]


    return render_template('utrzymanie.html',danewykres4=danewykres4)

@app.route("/pora")
def show_pora():

    fd_kobiety = db.session.query(Formdata).filter(Formdata.male == "K")
    fd_mezczyzni = db.session.query(Formdata).filter(Formdata.male == "M")

    #pora dnia podział na płeć
    fd_k_kiedy_czas_rano = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_k_kiedy_czas_przed = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_k_kiedy_czas_po = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_k_kiedy_czas_wieczor = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_k_kiedy_czas_noc = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_m_kiedy_czas_rano = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_m_kiedy_czas_przed = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_m_kiedy_czas_po = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_m_kiedy_czas_wieczor = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_m_kiedy_czas_noc = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    danewykres1 = [['Płeć', 'rano (przed 8)', 'przed południem (8-12)', 'po południu (12-17)', 'wieczorem (17- 22)',
                    'w nocy (po 22) '],
                   ['Kobiety', fd_k_kiedy_czas_rano, fd_k_kiedy_czas_przed, fd_k_kiedy_czas_po, fd_k_kiedy_czas_wieczor,
                    fd_k_kiedy_czas_noc],
                   ['Mężczyzni', fd_m_kiedy_czas_rano, fd_m_kiedy_czas_przed, fd_m_kiedy_czas_po,
                    fd_m_kiedy_czas_wieczor, fd_m_kiedy_czas_noc]]

    # wykres kiedy wolny czas z podzielem na studentow

    fd_student1 = db.session.query(Formdata).filter(Formdata.student == "I")
    fd_student2 = db.session.query(Formdata).filter(Formdata.student == "II")
    fd_student3 = db.session.query(Formdata).filter(Formdata.student == "III")
    fd_student4 = db.session.query(Formdata).filter(Formdata.student == "IV")
    fd_student5 = db.session.query(Formdata).filter(Formdata.student == "V")

    fd_stu1 = db.session.query(Formdata).filter(Formdata.student == "I").count()
    fd_stu2 = db.session.query(Formdata).filter(Formdata.student == "II").count()
    fd_stu3 = db.session.query(Formdata).filter(Formdata.student == "III").count()
    fd_stu4 = db.session.query(Formdata).filter(Formdata.student == "IV").count()
    fd_stu5 = db.session.query(Formdata).filter(Formdata.student == "V").count()

    danestudent = [['Student I roku', fd_stu1], ['Student II roku', fd_stu2], ['Student III roku', fd_stu3],
                   ['Student IV roku', fd_stu4], ['Student V roku', fd_stu5]]

    fd_student1_kiedy_czas_rano = fd_student1.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student1_kiedy_czas_przed = fd_student1.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student1_kiedy_czas_po = fd_student1.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student1_kiedy_czas_wieczor = fd_student1.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student1_kiedy_czas_noc = fd_student1.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student2_kiedy_czas_rano = fd_student2.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student2_kiedy_czas_przed = fd_student2.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student2_kiedy_czas_po = fd_student2.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student2_kiedy_czas_wieczor = fd_student2.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student2_kiedy_czas_noc = fd_student2.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student3_kiedy_czas_rano = fd_student3.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student3_kiedy_czas_przed = fd_student3.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student3_kiedy_czas_po = fd_student3.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student3_kiedy_czas_wieczor = fd_student3.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student3_kiedy_czas_noc = fd_student3.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student4_kiedy_czas_rano = fd_student4.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student4_kiedy_czas_przed = fd_student4.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student4_kiedy_czas_po = fd_student4.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student4_kiedy_czas_wieczor = fd_student4.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student4_kiedy_czas_noc = fd_student4.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student5_kiedy_czas_rano = fd_student5.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student5_kiedy_czas_przed = fd_student5.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student5_kiedy_czas_po = fd_student5.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student5_kiedy_czas_wieczor = fd_student5.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student5_kiedy_czas_noc = fd_student5.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    danewykres2 = [
        ['rok_studiow', 'rano (przed 8)', 'przed południem (8-12)', 'po południu (12-17)', 'wieczorem (17- 22)',
         'w nocy (po 22) '],
        ['Student I roku', fd_student1_kiedy_czas_rano, fd_student1_kiedy_czas_przed, fd_student1_kiedy_czas_po,
         fd_student1_kiedy_czas_wieczor, fd_student1_kiedy_czas_noc],
        ['Student II roku', fd_student2_kiedy_czas_rano, fd_student2_kiedy_czas_przed, fd_student2_kiedy_czas_po,
         fd_student2_kiedy_czas_wieczor, fd_student2_kiedy_czas_noc],
        ['Student III roku', fd_student3_kiedy_czas_rano, fd_student3_kiedy_czas_przed, fd_student3_kiedy_czas_po,
         fd_student3_kiedy_czas_wieczor, fd_student3_kiedy_czas_noc],
        ['Student IV roku', fd_student4_kiedy_czas_rano, fd_student4_kiedy_czas_przed, fd_student4_kiedy_czas_po,
         fd_student4_kiedy_czas_wieczor, fd_student4_kiedy_czas_noc],
        ['Student V roku', fd_student5_kiedy_czas_rano, fd_student5_kiedy_czas_przed, fd_student5_kiedy_czas_po,
         fd_student5_kiedy_czas_wieczor, fd_student5_kiedy_czas_noc]]

    return render_template('pora.html', danewykres1=danewykres1, danewykres2=danewykres2)

@app.route("/kontakt")
def show_kontakt():
    return render_template('kontakt.html')

@app.route("/info")
def show_info():
    return render_template('info.html')

    nowe = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(Formdata.male=="K").group_by(Formdata.free_time_in_week)

    fd_kobiety = db.session.query(Formdata).filter(Formdata.male == "K")
    fd_kobiety_wies = fd_kobiety.filter(Formdata.friends == "sam/sama").count()

    zainteresowania=db.session.query(Formdata.like_doing)
    n=zliczenie(zainteresowania)
    b=[]
    b[0][0]='Zainteresowanie'
    b[0][1]='Ile osob'
    i=2
    for el in n:
       b [i][0] = el
       b[i][1] = n[el]

    return render_template('proba.html', data=n, ilosc=b[1][0])

@app.route("/result")

def show_result():
    # przgotowanie danych do wykresu z podziałem na kobiety i mężczyzn  ile czasu na social media

    tablica_using_accouts = ['do godziny', '1-3 godziny', '4-5 godzin', 'wiecej niż 5 godzin']
    # kobiety
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.male == "K"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    using_accounts_w_ = preparing_data_for_column_chart(tablica_using_accouts, query, 'kobiety')

    # mezczyzni
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.male == "M"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    using_accounts_m = preparing_data_for_column_chart(tablica_using_accouts, query, 'Meżczyźni')

    tablica_using_accouts.insert(0, "Plec")
    I = [tablica_using_accouts, using_accounts_w_, using_accounts_m]




    fd_student=db.session.query(Formdata).filter(Formdata.student=="I").count()
    fd_niestudent=db.session.query(Formdata).filter(Formdata.student=="II").count()

    #przgotowanie danych do wykresu wolny czas w tygodniu z weekendem podzial kobiet mezczyzni
    fd_kobiety = db.session.query(Formdata).filter(Formdata.male == "K")
    fd_mezczyzni = db.session.query(Formdata).filter(Formdata.male == "M")

    fd_k=db.session.query(Formdata).filter(Formdata.male == "K").count()
    fd_m=db.session.query(Formdata).filter(Formdata.male == "M").count()

    #wykres pierwszy
    fd_kobiety_wolny_czas_brak = fd_kobiety.filter(Formdata.free_time_in_week == "brak wolnego czasu").count()
    fd_kobiety_wolny_czas_mniej = fd_kobiety.filter(Formdata.free_time_in_week == "mniej niż 10h").count()
    fd_kobiety_wolny_czas_10h = fd_kobiety.filter(Formdata.free_time_in_week == "10-20 h").count()
    fd_kobiety_wolny_czas_20h = fd_kobiety.filter(Formdata.free_time_in_week == "20-30 h").count()
    fd_kobiety_wolny_czas_30h = fd_kobiety.filter(Formdata.free_time_in_week == "wiecej niż 30h").count()
    fd_m_wolny_czas_brak = fd_mezczyzni.filter(Formdata.free_time_in_week == "brak wolnego czasu").count()
    fd_m_wolny_czas_mniej = fd_mezczyzni.filter(Formdata.free_time_in_week == "mniej niż 10h").count()
    fd_m_wolny_czas_10h = fd_mezczyzni.filter(Formdata.free_time_in_week == "10-20 h").count()
    fd_m_wolny_czas_20h = fd_mezczyzni.filter(Formdata.free_time_in_week == "20-30 h").count()
    fd_m_wolny_czas_30h = fd_mezczyzni.filter(Formdata.free_time_in_week == "wiecej niż 30h").count()
    dane1=[['Plec','brak wolnego czasu','mniej niż 10h','10-20 h','20-30 h','wiecej niż 30h'],
           ['Kobiety', fd_kobiety_wolny_czas_brak, fd_kobiety_wolny_czas_mniej, fd_kobiety_wolny_czas_10h, fd_kobiety_wolny_czas_20h, fd_kobiety_wolny_czas_30h],
           ['Mezczyzni',fd_m_wolny_czas_brak,fd_m_wolny_czas_mniej,fd_m_wolny_czas_10h,fd_m_wolny_czas_20h,fd_m_wolny_czas_30h]]

    #wykres 2 o jakiej poprze najwiecej czasu z podzialem kiedy podziałem na plec

    fd_k_kiedy_czas_rano = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_k_kiedy_czas_przed = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_k_kiedy_czas_po = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_k_kiedy_czas_wieczor = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_k_kiedy_czas_noc = fd_kobiety.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_m_kiedy_czas_rano = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_m_kiedy_czas_przed = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_m_kiedy_czas_po = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_m_kiedy_czas_wieczor = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_m_kiedy_czas_noc = fd_mezczyzni.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    danewykres1 = [['Płeć', 'rano (przed 8)', 'przed południem (8-12)', 'po południu (12-17)', 'wieczorem (17- 22)',
                    'w nocy (po 22) '],
                   ['Kobiety', fd_k_kiedy_czas_rano, fd_k_kiedy_czas_przed, fd_k_kiedy_czas_po, fd_k_kiedy_czas_wieczor,
                    fd_k_kiedy_czas_noc],
                   ['Mężczyzni', fd_m_kiedy_czas_rano, fd_m_kiedy_czas_przed, fd_m_kiedy_czas_po,
                    fd_m_kiedy_czas_wieczor, fd_m_kiedy_czas_noc]]

    #wykres kiedy wolny czas z podzielem na studentow

    fd_student1 = db.session.query(Formdata).filter(Formdata.student == "I")
    fd_student2 = db.session.query(Formdata).filter(Formdata.student == "II")
    fd_student3 = db.session.query(Formdata).filter(Formdata.student == "III")
    fd_student4 = db.session.query(Formdata).filter(Formdata.student == "IV")
    fd_student5 = db.session.query(Formdata).filter(Formdata.student == "V")

    fd_stu1 = db.session.query(Formdata).filter(Formdata.student == "I").count()
    fd_stu2 = db.session.query(Formdata).filter(Formdata.student == "II").count()
    fd_stu3 = db.session.query(Formdata).filter(Formdata.student == "III").count()
    fd_stu4 = db.session.query(Formdata).filter(Formdata.student == "IV").count()
    fd_stu5 = db.session.query(Formdata).filter(Formdata.student == "V").count()

    danestudent = [['Student I roku', fd_stu1], ['Student II roku', fd_stu2], ['Student III roku', fd_stu3],
                   ['Student IV roku', fd_stu4], ['Student V roku', fd_stu5]]

    fd_student1_kiedy_czas_rano = fd_student1.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student1_kiedy_czas_przed = fd_student1.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student1_kiedy_czas_po = fd_student1.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student1_kiedy_czas_wieczor = fd_student1.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student1_kiedy_czas_noc = fd_student1.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student2_kiedy_czas_rano = fd_student2.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student2_kiedy_czas_przed = fd_student2.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student2_kiedy_czas_po = fd_student2.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student2_kiedy_czas_wieczor = fd_student2.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student2_kiedy_czas_noc = fd_student2.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student3_kiedy_czas_rano = fd_student3.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student3_kiedy_czas_przed = fd_student3.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student3_kiedy_czas_po = fd_student3.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student3_kiedy_czas_wieczor = fd_student3.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student3_kiedy_czas_noc = fd_student3.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student4_kiedy_czas_rano = fd_student4.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student4_kiedy_czas_przed = fd_student4.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student4_kiedy_czas_po = fd_student4.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student4_kiedy_czas_wieczor = fd_student4.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student4_kiedy_czas_noc = fd_student4.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    fd_student5_kiedy_czas_rano = fd_student5.filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_student5_kiedy_czas_przed = fd_student5.filter(
        Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_student5_kiedy_czas_po = fd_student5.filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_student5_kiedy_czas_wieczor = fd_student5.filter(
        Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_student5_kiedy_czas_noc = fd_student5.filter(Formdata.most_of_free_time_in_day == "w nocy (po 22) ").count()

    danewykres2 = [
        ['rok_studiow', 'rano (przed 8)', 'przed południem (8-12)', 'po południu (12-17)', 'wieczorem (17- 22)',
         'w nocy (po 22) '],
        ['Student I roku', fd_student1_kiedy_czas_rano, fd_student1_kiedy_czas_przed, fd_student1_kiedy_czas_po,
         fd_student1_kiedy_czas_wieczor, fd_student1_kiedy_czas_noc],
        ['Student II roku', fd_student2_kiedy_czas_rano, fd_student2_kiedy_czas_przed, fd_student2_kiedy_czas_po,
         fd_student2_kiedy_czas_wieczor, fd_student2_kiedy_czas_noc],
        ['Student III roku', fd_student3_kiedy_czas_rano, fd_student3_kiedy_czas_przed, fd_student3_kiedy_czas_po,
         fd_student3_kiedy_czas_wieczor, fd_student3_kiedy_czas_noc],
        ['Student IV roku', fd_student4_kiedy_czas_rano, fd_student4_kiedy_czas_przed, fd_student4_kiedy_czas_po,
         fd_student4_kiedy_czas_wieczor, fd_student4_kiedy_czas_noc],
        ['Student V roku', fd_student5_kiedy_czas_rano, fd_student5_kiedy_czas_przed, fd_student5_kiedy_czas_po,
         fd_student5_kiedy_czas_wieczor, fd_student5_kiedy_czas_noc]]

    daneplec = [['Płeć','Ilość'],[' Kobiety', fd_k],['Mezczyzni', fd_m]]

    #dane wykres z kim wolny czas podzial na kobiety i mezczyzn
    fd_k_zkim_sam = fd_kobiety.filter(Formdata.friends == "sam/sama").count()
    fd_k_zkim_jedna = fd_kobiety.filter(Formdata.friends == "z jedną osobą").count()
    fd_k_zkim_dwa = fd_kobiety.filter(Formdata.friends == "z dwoma lub trzema osobami").count()
    fd_k_zkim_wiecej = fd_kobiety.filter(Formdata.friends == "z więcej niż trzema osobami").count()

    fd_m_zkim_sam = fd_mezczyzni.filter(Formdata.friends == "sam/sama)").count()
    fd_m_zkim_jedna = fd_mezczyzni.filter(Formdata.friends == "z jedną osobą").count()
    fd_m_zkim_dwa = fd_mezczyzni.filter(Formdata.friends == "z dwoma lub trzema osobami").count()
    fd_m_zkim_wiecej = fd_mezczyzni.filter(Formdata.friends == "z więcej niż trzema osobami").count()

    dane_k_z_kim=[['Rodzaj','ile'],['sama',fd_k_zkim_sam],['z jedną osobą',fd_k_zkim_jedna], ['z dwoma lub trzema osobami', fd_k_zkim_dwa],
                  ['z więcej niż trzema osobami',fd_k_zkim_wiecej]]

    dane_m_z_kim=[['Rodzaj','ile'],['sam',fd_m_zkim_sam],['z jedną osobą',fd_m_zkim_jedna], ['z dwoma lub trzema osobami',fd_m_zkim_dwa],
                  ['z więcej niż trzema osobami',fd_m_zkim_wiecej]]

    #ile czasu na media spolecznosciowe:

    fd_h = db.session.query(Formdata).filter(Formdata.using_accounts == "do godziny").count()
    fd_3h = db.session.query(Formdata).filter(Formdata.using_accounts == "1-3 godziny").count()
    fd_5h = db.session.query(Formdata).filter(Formdata.using_accounts == "4-5 godzin").count()
    fd_more = db.session.query(Formdata).filter(Formdata.using_accounts == "wiecej niż 5 godzin").count()

    danewykres3 = [['opcje','media_czas'], ['do godziny', fd_h], ['1-3 godziny', fd_3h], ['4-5 godzin', fd_5h],
                   ['wiecej niż 5 godzin', fd_more]]

    fd_10 = db.session.query(Formdata).filter(Formdata.how_much_money == "mniej niż 10 zł").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.how_much_money == "10-30 zł").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.how_much_money == "30-50 zł").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.how_much_money == "50-100 zł").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.how_much_money == "więcej niż 100 zł").count()

    danewykres4 = [['jaka kwota','ile osob'], ['mniej niż 10 zł', fd_10], ['10-30 zł', fd_30], ['30-50 zł', fd_50],
                   ['50-100 zł', fd_100], ['więcej niż 100 zł', fd_moremoney]]



    return render_template('result.html', daneplec=daneplec, dane1=dane1, danewykres1=danewykres1, danewykres2=danewykres2,
                           dane_k_z_kim=dane_k_z_kim,dane_m_z_kim=dane_m_z_kim, danewykres3=danewykres3, danewykres4=danewykres4)


@app.route("/save", methods=['POST'])
def save():

    # Get data from FORM
    male = request.form['plec']
    student = request.form['rok_studiow']
    family_place = request.form['pochodzenie']
    FreeTimeInWeek = request.form['ilosc_czasu']
    FreeTimeWithoutWeekend= request.form['ilosc_czasu_ty']
    MostOfFreeTimeInDay = request.form['pora_najwiecej_czasu']
    Responsibilities = request.form['obowiazki']
    Friends = request.form['ile_osob']
    WithWhoAreYouLiving= request.form['mieszkanie']
    SingleRoom = request.form['swoj_pokoj']
    WhereSocialMeetings= request.form['spotkania']
    Acounts = request.form.getlist('portal')
    UsingAcounts= request.form['media_czas']
    LikeToDo= request.form.getlist('formy_spedzania_czasu')
    ActiveTime = request.form.getlist('aktywny_czas')
    UsingComputer = request.form.getlist('czas_komp')
    HowMuchMoney= request.form['kwota']
    FromMoney = request.form['srodki']
    YourMoney= request.form['wlasne_zarobki']
    def zamiana(lista):
        do_bazy=""
        for element in lista:
            do_bazy=do_bazy + element+";"
        return do_bazy
    Like = zamiana(LikeToDo)
    Computer=zamiana(UsingComputer)
    Portal=zamiana(Acounts)
    Active=zamiana(ActiveTime)

    # Save the data
    fd = Formdata(male, student, family_place, FreeTimeInWeek , FreeTimeWithoutWeekend, MostOfFreeTimeInDay,Responsibilities, Friends, WithWhoAreYouLiving, SingleRoom, WhereSocialMeetings, Portal,UsingAcounts ,Like, Active , Computer ,  HowMuchMoney, FromMoney,YourMoney)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()