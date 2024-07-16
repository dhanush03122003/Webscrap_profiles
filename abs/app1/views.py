from django.shortcuts import render
from app1.models import Send_remainder
from datetime import datetime,timedelta
from django.core.mail import *
from abs import settings

# Create your views here.
def send_rem(user = 10):
    # l_time = Send_remainder.objects.get(user_name = user).time
    # l_date = Send_remainder.objects.get(user_name = user).date
    # m_sent = Send_remainder.objects.get(user_name = user).mail_sent_time
    date_str = "2024-02-15"
    time_str = "12:50:14"

    date_format = "%Y-%m-%d"
    time_format = "%H:%M:%S"

    # Convert strings to datetime objects
    given_datetime = datetime.strptime(f"{date_str} {time_str}", f"{date_format} {time_format}")

    # Current date and time
    current_time = datetime.now()

    # Calculate the time difference
    time_difference = current_time - given_datetime

    # Check if the difference is greater than 24 hours
    if time_difference > timedelta(hours=24):
        given_time = datetime.strptime(m_sent, time_format)
        if datetime.now() - given_time > timedelta(hours=6):
            txt_all = ["Hey! Your student application is waiting for you. Take a break and catch up on your studies. 📖✨"
,"Hello! Your education journey is important. Log in to your student app and continue making progress. You've got this! 💪🎓"
,"Hi there! It's been a while since you visited your student app. Your courses miss you! Log in and explore the latest content. 🚀"
,"Greetings! Your student app is like a treasure trove of knowledge. Dive back in and let the learning adventure continue! 🌟📚"
]
            msg = txt_all[0]
            g = Send_remainder.objects.get(user_name = user)
            t=settings.EMAIL_HOST_USER
            sndr = True#
            sbj = True#
            send_mail(sbj,msg,t,[sndr])
            your_datetime_object = datetime.now()
            g.mail_sent_time = your_datetime_object.strftime("%H:%M:%S")
            g.save()

    


def create_time_stamp(user):
    g = Send_remainder.objects.get(user_name = user)
    your_datetime_object = datetime.now()
    g.date = your_datetime_object.strftime("%Y-%m-%d")
    g.time = your_datetime_object.strftime("%H:%M:%S")
    g.mail_sent_time = your_datetime_object.strftime("%H:%M:%S")
    g.save()


