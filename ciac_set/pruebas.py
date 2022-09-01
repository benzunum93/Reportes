from datetime import date, datetime, timedelta

date_ini= date(2022, 6,1)
date_final=date(2022,6,10)


start_date=date_ini
end_date=date_final
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


for single_date in daterange(start_date, end_date):
    fecha=single_date.strftime("%Y-%m-%d")
    print(fecha)