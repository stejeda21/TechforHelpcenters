# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from models import Refugee
from flask import Flask
import requests

app = Flask(__name__)

API_BASE_URL ='https://api.twilio.com/2010-04-01'
 

"""Loop over help centers that are not at full capacity"""
# helpcenters = ['Refugee.helpcenter']
# for open_helpcenters in helpcenters:
#  if open_helpcenters != '100%':
"""Send a SMS message to multiple receipients"""
#  numbers_to_message = ['Refugee.phonenumber']
# for numbers in numbers_to_message:
#     url = f'{API_BASE_URL}/Accounts/{ACCOUNTSID}/Messages?To={MY_PHONE_NUMBER}&From={TWILIO_PHONE_NUMBER}&Body=Hi {Refugee.firstname}, unfortunately {user.help_center}'s capacity is full. The other help center's that have open occupancy are:
        # {open_helpcenters}
#       '

#     payload=f'To=%2B19083728419&From=%2B19084023124&Body=Hi%20%7B{Refugee.firstname}%7D%2C%20unfortunately%20%7B{user.help_center}%7D\'s%20capacity%20is%20full.%20The%20other%20help%20center\'s%20that%20have%20open%20occupancy%20are%3A%20%7B{o}pen_helpcenters}%7D'
#     headers = {
#     'Authorization': 'Basic QUNkMDFmNmRkYWI2MjRlMDM2N2EzYzZjMGMwMDAzODU3YzozYmIyZmY5MzI4ZThiYWI0N2VmNmI3OGQwZjdjNDAxYg==',
#     'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)