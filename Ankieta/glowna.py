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
    i=0
    for klucz in tablica_do_porownania:
        for element in tablica_z_bazy:
            a= element[1].find(klucz)
            if(a!=-1):
                tab.append(element[0])
                i=i+1
        if(i==0):
            tab.append(0)
        i=0
    if( len(tab) == 1 ):
        for el in tablica_do_porownania:
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

    where_social_meetings = db.Column(db.String)
    accounts = db.Column(db.String)
    using_accounts = db.Column(db.String)
    like_doing = db.Column(db.String)
    active_time = db.Column(db.String)
    using_computer = db.Column(db.String)
    how_much_money = db.Column(db.String)
    from_money = db.Column(db.String)
    your_money = db.Column(db.String)
	
    def __init__(self, male, student, FamilyPlace, FreeTimeInWeek , FreeTimeWithoutWeekend,MostOfFreeTimeInDay,Responsibilities, Friends, WithWhoAreYouLiving, WhereSocialMeetings, Acounts,UsingAcounts ,LikeToDo, ActiveTime , UsingComputer ,  HowMuchMoney, FromMoney, YourMoney):

        self.male = male
        self.student = student
        self.familyplace = FamilyPlace
        self.free_time_in_week = FreeTimeInWeek
        self.free_time_without_weekend = FreeTimeWithoutWeekend
        self.most_of_free_time_in_day = MostOfFreeTimeInDay
        self.responsibilities = Responsibilities
        self.friends = Friends
        self.with_who_are_you_living = WithWhoAreYouLiving

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

@app.route("/czastydzien")
def show_czastydzien():

    #dane do wykres ile w tygodniu czasu
    fd_10 = db.session.query(Formdata).filter(Formdata.free_time_in_week == "brak wolnego czasu").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.free_time_in_week == "mniej niż 10h").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.free_time_in_week == "10-20 h").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.free_time_in_week == "20-30 h").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.free_time_in_week == "więcej niz 30h ").count()

    danewykres4 = [['ile czasu', 'ile osob'], ['brak wolnego czasu', fd_10], ['mniej niż 10h', fd_30], ['10-20 h', fd_50],
                   ['20-30 h', fd_100], ['więcej niz 30h ', fd_moremoney]]


    # dane do wykresu ile czasu studenci maja czasu w tygodniu z uwzglednieniem weekendu z podzialem na plec
    tablica_wolny_czas = ['brak wolnego czasu', 'mniej niż 10h', '10-20 h', '20-30 h', 'więcej niz 30h ']
    # kobiety
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.male == "K"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_w_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'Kobiety')

    # mezczyzni
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.male == "M"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_m = preparing_data_for_column_chart(tablica_wolny_czas, query, 'Meżczyźni')


    # I rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.student == "I"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_I_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'I')

    # II rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.student == "II"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_II = preparing_data_for_column_chart(tablica_wolny_czas, query, 'II')

    # III rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.student == "III"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_III_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'III')

    # IV rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.student == "IV"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_IV = preparing_data_for_column_chart(tablica_wolny_czas, query, 'IV')

    #V rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.student == "V"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_V = preparing_data_for_column_chart(tablica_wolny_czas, query, 'V')
    tablica_wolny_czas_rok = ['Rok studiów','brak wolnego czasu', 'mniej niż 10h', '10-20 h', '20-30 h', 'więcej niz 30h ' ]
    tablica_wolny_czas.insert(0, "Plec")
    Czas_wolny_plec = [tablica_wolny_czas, wolny_czas_w_, wolny_czas_m]
    Czas_wolny_rok = [tablica_wolny_czas_rok, wolny_czas_I_, wolny_czas_II, wolny_czas_III_, wolny_czas_IV, wolny_czas_V ]
    print(Czas_wolny_rok)

    return render_template('czastydzien.html', danewykres4=danewykres4, Czas_wolny_plec=Czas_wolny_plec, Czas_wolny_rok=Czas_wolny_rok )

@app.route("/czastydzienpracujacy")
def show_czastydzienpracujacy():
    # dane do wykres ile w tygodniu czasu
    fd_10 = db.session.query(Formdata).filter(Formdata.free_time_without_weekend == "brak wolnego czasu").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.free_time_without_weekend == "ok. 1h").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.free_time_without_weekend == "ok. 3-5h").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.free_time_without_weekend == "20-30 h").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.free_time_without_weekend == "więcej niz 5h ").count()

    danewykres4 = [['ile czasu', 'ile osob'], ['brak wolnego czasu', fd_10], ['ok. 1h', fd_30],
                   ['10-20 h', fd_50],
                   ['20-30 h', fd_100], ['więcej niz 30h ', fd_moremoney]]

    # dane do wykresu ile czasu studenci maja czasu w tygodniu z uwzglednieniem weekendu z podzialem na plec
    tablica_wolny_czas = ['brak wolnego czasu', 'ok. 1h', 'ok 2h', 'ok. 3-5h', 'więcej niz 5h ']
    # kobiety
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.male == "K"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_w_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'Kobiety')

    # mezczyzni
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.male == "M"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_m = preparing_data_for_column_chart(tablica_wolny_czas, query, 'Meżczyźni')

    # I rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.student == "I"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_I_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'I')

    # II rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.student == "II"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_II = preparing_data_for_column_chart(tablica_wolny_czas, query, 'II')

    # III rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.student == "III"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_III_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'III')

    # IV rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.student == "IV"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_IV = preparing_data_for_column_chart(tablica_wolny_czas, query, 'IV')

    # V rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_without_weekend).filter(
        Formdata.student == "V"). \
        group_by(Formdata.free_time_without_weekend).order_by(Formdata.free_time_without_weekend)
    wolny_czas_V = preparing_data_for_column_chart(tablica_wolny_czas, query, 'V')
    tablica_wolny_czas_rok = ['Rok studiów', 'brak wolnego czasu', 'ok. 1h', 'ok 2h', 'ok. 3-5h',
                              'więcej niz 5h ']
    tablica_wolny_czas.insert(0, "Plec")
    Czas_wolny_plec = [tablica_wolny_czas, wolny_czas_w_, wolny_czas_m]
    Czas_wolny_rok = [tablica_wolny_czas_rok, wolny_czas_I_, wolny_czas_II, wolny_czas_III_, wolny_czas_IV,
                      wolny_czas_V]

    return render_template('czastydzienpracujacy.html', danewykres4=danewykres4, Czas_wolny_rok= Czas_wolny_rok, Czas_wolny_plec=Czas_wolny_plec )


@app.route("/gdzie")
def show_gdzie():
    # gdzie studenci  spedzaja wolny czas - piechart
    query = db.session.query(Formdata.where_social_meetings, func.count(Formdata.created_at).label("ile")).\
        group_by(Formdata.where_social_meetings)
    Where = preparing(query)

    #gdzie mezczyzni spedzaja wolny czas - piechart
    query = db.session.query(Formdata.where_social_meetings, func.count(Formdata.created_at).label("ile")).filter(
        Formdata.male == "M"). \
        group_by(Formdata.where_social_meetings)
    Where_m = preparing(query)
    #gdzie kobiety spedzaja wolny czas - piechart

    query = db.session.query(Formdata.where_social_meetings, func.count(Formdata.created_at).label("ile")).filter(
        Formdata.male == "K"). \
        group_by(Formdata.where_social_meetings)
    Where_W = preparing(query)

    # z iloma osobami studenci  spedzaja wolny czas - piechart
    query = db.session.query(Formdata.friends, func.count(Formdata.created_at).label("ile")). \
        group_by(Formdata.where_social_meetings)
    withwho = preparing(query)

    # z iloma osobami mezczyzni spedzaja wolny czas - piechart
    query = db.session.query(Formdata.friends, func.count(Formdata.created_at).label("ile")).filter(
        Formdata.male == "M"). \
        group_by(Formdata.where_social_meetings)
    withwho_m = preparing(query)

    # z iloma osobami kobiety spedzaja wolny czas - piechart
    query = db.session.query(Formdata.friends, func.count(Formdata.created_at).label("ile")).filter(
        Formdata.male == "K"). \
        group_by(Formdata.where_social_meetings)
    withwho_w = preparing(query)



    return render_template('gdzie.html',Where_m = Where_m, Where_w= Where_W, Where=Where, withwho=withwho,withwho_m=withwho_m, withwho_w=withwho_w)

@app.route("/mieszkanie")
def show_mieszkanie():

    #dane do wykres ile w tygodniu czasu
    query = db.session.query(Formdata.friends, func.count(Formdata.created_at).label("ile")). \
        group_by(Formdata.friends)
    withwholiving = preparing(query)


    # dane do wykresu ile czasu studenci maja czasu w tygodniu z uwzglednieniem weekendu z podzialem na plec
    tablica_wolny_czas = ['sam/sama', 'ze znajomymi', 'z partnerką/partnerem', 'z rodzicami', 'z rodzeństwem lub kuzynostwem']
    # kobiety
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.with_who_are_you_living).filter(
        Formdata.male == "K"). \
        group_by(Formdata.with_who_are_you_living).order_by(Formdata.with_who_are_you_living)
    wolny_czas_w_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'Kobiety')

    # mezczyzni
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.with_who_are_you_living).filter(
        Formdata.male == "M"). \
        group_by(Formdata.with_who_are_you_living).order_by(Formdata.with_who_are_you_living)
    wolny_czas_m = preparing_data_for_column_chart(tablica_wolny_czas, query, 'Meżczyźni')


    # I rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.with_who_are_you_living).filter(
        Formdata.student == "I"). \
        group_by(Formdata.with_who_are_you_living).order_by(Formdata.with_who_are_you_living)
    wolny_czas_I_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'I')

    # II rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.with_who_are_you_living).filter(
        Formdata.student == "II"). \
        group_by(Formdata.with_who_are_you_living).order_by(Formdata.with_who_are_you_living)
    wolny_czas_II = preparing_data_for_column_chart(tablica_wolny_czas, query, 'II')

    # III rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.with_who_are_you_living).filter(
        Formdata.student == "III"). \
        group_by(Formdata.with_who_are_you_living).order_by(Formdata.with_who_are_you_living)
    wolny_czas_III_ = preparing_data_for_column_chart(tablica_wolny_czas, query, 'III')

    # IV rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.free_time_in_week).filter(
        Formdata.student == "IV"). \
        group_by(Formdata.free_time_in_week).order_by(Formdata.free_time_in_week)
    wolny_czas_IV = preparing_data_for_column_chart(tablica_wolny_czas, query, 'IV')

    #V rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.with_who_are_you_living).filter(
        Formdata.student == "V"). \
        group_by(Formdata.with_who_are_you_living).order_by(Formdata.with_who_are_you_living)
    wolny_czas_V = preparing_data_for_column_chart(tablica_wolny_czas, query, 'V')

    tablica_wolny_czas_rok = ['sam/sama','ze znajomymi', 'z partnerką/partnerem', 'z rodzicami', '20-30 h', 'z rodzeństwem lub kuzynostwem' ]
    tablica_wolny_czas.insert(0, "Plec")
    Z_kim_mieszka_plec = [tablica_wolny_czas, wolny_czas_w_, wolny_czas_m]
    Z_kim_mieszka_rok = [tablica_wolny_czas_rok, wolny_czas_I_, wolny_czas_II, wolny_czas_III_, wolny_czas_IV, wolny_czas_V ]




    return render_template('mieszkanie.html',danewykres1=withwholiving, danewykres2= Z_kim_mieszka_plec, danewykres4=Z_kim_mieszka_rok)


@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/moje")
def show_moje():

    # gdzie studenci  spedzaja wolny czas - piechart
    query = db.session.query(Formdata.male, func.count(Formdata.created_at).label("ile")). \
        group_by(Formdata.male)
    Gender = preparing(query)

    # gdzie mezczyzni spedzaja wolny czas - piechart
    query = db.session.query(Formdata.familyplace, func.count(Formdata.created_at).label("ile")). \
        group_by(Formdata.familyplace)
    Place = preparing(query)
    # gdzie kobiety spedzaja wolny czas - piechart

    query = db.session.query(Formdata.student, func.count(Formdata.created_at).label("ile")).\
        group_by(Formdata.student)
    Year = preparing(query)

    return render_template('moje.html',danewykres1=Gender, danewykres2=Place, danewykres3 = Year)

@app.route("/jak")
def show_jak():
    # wykres zainteresowania dla wszystkich
    zainteresowania = db.session.query(Formdata.like_doing)
    n = zliczenie(zainteresowania)
    Like = []
    Like.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Like.append([el, n[el]])


    #dla kobiet

    zainteresowania_k = db.session.query(Formdata.like_doing).filter(Formdata.male =="K")
    n = zliczenie(zainteresowania_k)
    Like_k = []
    Like_k.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Like_k.append([el, n[el]])

    #dla mezczyzn

    zainteresowania_m = db.session.query(Formdata.like_doing).filter(Formdata.male == "M")
    n = zliczenie(zainteresowania_k)
    Like_m = []
    Like_m.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Like_m.append([el, n[el]])


    # wykres aktywny czas dla wszytkich
    kontaportale = db.session.query(Formdata.active_time)
    n = zliczenie(kontaportale)
    Active = []
    Active.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Active.append([el, n[el]])

     #dla kobiet

    kontaportale_k = db.session.query(Formdata.active_time).filter(Formdata.male == "K")
    n = zliczenie(kontaportale_k)
    Active_k = []
    Active_k.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Active_k.append([el, n[el]])

    # dla mezczyzn

    kontaportale_m = db.session.query(Formdata.active_time).filter(Formdata.male == "M")
    n = zliczenie(kontaportale_m)
    Active_m = []
    Active_m.append(['Zainteresowanie', 'Ile osob'])
    for el in n:
        Active_m.append([el, n[el]])

    # wykres aktywny czas dla wszytkich
    co_komputer = db.session.query(Formdata.using_computer)
    n = zliczenie(co_komputer)
    Computer = []
    Computer.append(['Używanie komputera', 'Ile osob'])
    for el in n:
        Computer.append([el, n[el]])

    co_komputer_k = db.session.query(Formdata.using_computer).filter(Formdata.male == "K")
    n = zliczenie(co_komputer_k)
    Computer_k = []
    Computer_k.append(['Używanie komputera', 'Ile osob'])
    for el in n:
        Computer_k.append([el, n[el]])

    co_komputer_m = db.session.query(Formdata.using_computer).filter(Formdata.male == "M")
    n = zliczenie(co_komputer_m)
    Computer_m = []
    Computer_m.append(['Używanie komputera', 'Ile osob'])
    for el in n:
        Computer_m.append([el, n[el]])

    return render_template('jak.html',Like=Like,Like_k=Like_k,Like_m=Like_m, Active = Active,Active_k=Active_k,
                           Active_m=Active_m, Computer=Computer, Computer_k=Computer_k, Computer_m=Computer_m)

@app.route("/ilenasocial")
def show_ilenasocial():

    # dane do wykres ile w tygodniu czasu
    query = db.session.query(Formdata.using_accounts, func.count(Formdata.created_at).label("ile")). \
        group_by(Formdata.using_accounts)
    using_accounts_all = preparing(query)


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


    # I rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.student == "I"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    wolny_czas_I_ = preparing_data_for_column_chart(tablica_using_accouts, query, 'I')

    # II rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.student == "II"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    wolny_czas_II = preparing_data_for_column_chart(tablica_using_accouts, query, 'II')

    # III rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.student == "III"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    wolny_czas_III_ = preparing_data_for_column_chart(tablica_using_accouts, query, 'III')

    # IV rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.student == "IV"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    wolny_czas_IV = preparing_data_for_column_chart(tablica_using_accouts, query, 'IV')

    # V rok
    query = db.session.query(func.count(Formdata.created_at).label("ile"), Formdata.using_accounts).filter(
        Formdata.student == "V"). \
        group_by(Formdata.using_accounts).order_by(Formdata.using_accounts)
    wolny_czas_V = preparing_data_for_column_chart(tablica_using_accouts, query, 'V')
    tablica_wolny_czas_rok = ['Rok studiów', 'do godziny', '1-3 godziny', '4-5 godzin', 'wiecej niż 5 godzin']


    tablica_using_accouts.insert(0, "Plec")

    Using_Accounts_gender = [tablica_using_accouts, using_accounts_w_, using_accounts_m]

    Using_Accounts_year = [tablica_wolny_czas_rok, wolny_czas_I_, wolny_czas_II, wolny_czas_III_, wolny_czas_IV,
                     wolny_czas_V]

    return render_template('ilenasocial.html',Using_Accounts_gender=Using_Accounts_gender, danewykres1=Using_Accounts_year, using_accounts_all=using_accounts_all)

@app.route("/utrzymanie")
def show_utrzymanie():
    fd_10 = db.session.query(Formdata).filter(Formdata.how_much_money == "mniej niż 10 zł").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.how_much_money == "10-30 zł").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.how_much_money == "30-50 zł").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.how_much_money == "50-100 zł").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.how_much_money == "więcej niż 100 zł").count()

    danewykres4 = [['jaka kwota', 'ile osob'], ['mniej niż 10 zł', fd_10], ['10-30 zł', fd_30], ['30-50 zł', fd_50],
                   ['50-100 zł', fd_100], ['więcej niż 100 zł', fd_moremoney]]

    fd_10 = db.session.query(Formdata).filter(Formdata.from_money == "od rodziny").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.from_money == "z oszczędności").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.from_money == "ze stypendium").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.from_money == "50-100 zł").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.from_money == "pracuję").count()

    danewykres1 = [['skąd środki', 'ile osob'], ['od rodziny', fd_10], ['z oszczędności', fd_30], ['ze stypendium', fd_50],
                   ['kredyt studencki', fd_100], ['pracuję', fd_moremoney]]

    fd_10 = db.session.query(Formdata).filter(Formdata.your_money == "całość").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.your_money == "70-90%").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.your_money == "50-70%").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.your_money == "30-50%").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.your_money == "poniżej 30%").count()

    danewykres2 = [['jaka kwota', 'ile osob'], ['całość', fd_10], ['70-90%', fd_30], ['50-70%', fd_50],
                   ['30-50%', fd_100], ['poniżej 30%', fd_moremoney]]

    return render_template('utrzymanie.html',danewykres4=danewykres4, danewykres1=danewykres1, danewykres2=danewykres2)

@app.route("/pora")
def show_pora():

    fd_10 = db.session.query(Formdata).filter(Formdata.most_of_free_time_in_day == "rano (przed 8)").count()
    fd_30 = db.session.query(Formdata).filter(Formdata.most_of_free_time_in_day == "przed południem (8-12)").count()
    fd_50 = db.session.query(Formdata).filter(Formdata.most_of_free_time_in_day == "po południu (12-17)").count()
    fd_100 = db.session.query(Formdata).filter(Formdata.most_of_free_time_in_day == "wieczorem (17- 22)").count()
    fd_moremoney = db.session.query(Formdata).filter(Formdata.most_of_free_time_in_day == "więcej niz 5h ").count()

    danewykres4 = [['pora dnia', 'ile osob'], ['rano (przed 8)', fd_10], ['przed południem (8-12)', fd_30],
                   ['po południu (12-17)', fd_50],
                   ['wieczorem (17- 22)', fd_100], ['w nocy (po 22) ', fd_moremoney]]

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

    return render_template('pora.html', danewykres1=danewykres1, danewykres2=danewykres2, danewykres4=danewykres4)

@app.route("/portale")
def show_portale():

    portale = db.session.query(Formdata.accounts)
    n = zliczenie(portale)
    portal_all = []
    portal_all.append(['Portal', 'Ile osob'])
    for el in n:
        portal_all.append([el, n[el]])

    portale_k = db.session.query(Formdata.accounts).filter(Formdata.male=="K")
    n = zliczenie(portale_k)
    portal_w = []
    portal_w.append(['Portal', 'Ile osob'])
    for el in n:
        portal_w.append([el, n[el]])

    portale_m = db.session.query(Formdata.accounts).filter(Formdata.male == "M")
    n = zliczenie(portale_m)
    portal_m = []
    portal_m.append(['Portal', 'Ile osob'])
    for el in n:
        portal_m.append([el, n[el]])

    return render_template('portale.html', danewykres1= portal_all, danewykres2 = portal_w, danewykres3 = portal_m)

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
    fd = Formdata(male, student, family_place, FreeTimeInWeek , FreeTimeWithoutWeekend, MostOfFreeTimeInDay,Responsibilities, Friends, WithWhoAreYouLiving, WhereSocialMeetings, Portal,UsingAcounts ,Like, Active , Computer ,  HowMuchMoney, FromMoney,YourMoney)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()