import csv
import boto3
import time
import datetime
from datetime import date

def calculate_age(born):
  today = datetime.datetime(2018, 11, 8)
  return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def write_to_db(file, organizer, db):
  items = []
  with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if not organizer:
          dt = row['When is your birthday?'].split('/')
          if(len(dt)==3):
            dt = datetime.datetime(int(dt[2]), int(dt[0]), int(dt[1]))
            age = calculate_age(dt)
          else:
            age = 0
          db.put_item(Item= 
          {'email': row['What is your email?'],
            'checked_in': False,
            'first_name': row['First Name'],
            'last_name': row['Last Name'],
            'shirt_size': row['What is your t-shirt size?'],
            'dietary_restrictions': row['If you have any food restrictions, please select them here.'].split(','),
            'minor_status': age < 18,
            'phone': row['What is your phone number?'],
            'organizer': organizer}
            )
        else:
          names = row['Name'].split(' ')
          db.put_item(Item= 
          {'email': row['Email'],
            'checked_in': False,
            'first_name': names[0],
            'last_name': names[1],
            'phone': row['Phone'],
            'organizer': organizer}
            )
          
          

def lambda_handler(items, context):
  organizer = True
  dynamodb = boto3.resource('dynamodb')
  db = dynamodb.Table('Technica-Data')
  write_to_db('./roster.csv', organizer, db)
             
