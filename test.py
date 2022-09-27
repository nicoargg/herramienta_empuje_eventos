from datetime import datetime
import csv


t_date = datetime.today()
t_date = t_date.strftime('%d-%m-%Y %H-%M-%S')
with open(f"{t_date}.csv", "a+") as f:
    write = csv.writer(f)
    write.writerow(['date','nashei','uwu'])