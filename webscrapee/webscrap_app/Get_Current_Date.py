from datetime import datetime
import pytz

def get_current_date():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    utc_now = datetime.now()
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    print(ist_now.strftime("%d-%m-%Y"))
    return ist_now.strftime("%d-%m-%Y")

def calculate_days_difference(date1_str, date2_str):
    date_format = "%d-%m-%Y"
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    difference = abs((date2 - date1).days)
    return difference

