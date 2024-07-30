from flask import Flask, request, Response
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime, timezone
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from bson import json_util

import json
import threading

app = Flask(__name__)
CORS(app, resources={r"/update": {"origins": "http://localhost:3000"}})

latest_flight_update = None

# MongoDB setup
client = MongoClient('mongodb://localhost:27017')
db = client['flight_status_db']
users_collection = db['Users']
flights_collection = db['Flights']

# Twilio setup
twilio_sid = 'your_twilio_sid'
twilio_auth_token = 'your_twilio_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
twilio_client = Client(twilio_sid, twilio_auth_token)


# Function to send email notifications
def send_email(to_email, subject, body):
    from_email = "yg7099104@gmail.com"  # Replace with your email address
    from_password = "uoadsypndvotanfz"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

# Function to send SMS notifications
def send_sms(to_phone_number, message):
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        print(f"SMS sent to {to_phone_number}")
    except Exception as e:
        print(f"Failed to send SMS to {to_phone_number}. Error: {e}")

# Function to send notifications to users
def send_notification(user, flight):
    # Send SMS
    sms_message = f"Flight {flight['flight_number']} update: {flight['status']}. Departure: {flight['departure_date']} {flight['departure_time']}. Arrival: {flight['arrival_date']} {flight['arrival_time']}."
    #send_sms(user['phone'], sms_message)

    # Send email
    subject = f"Flight {flight['flight_number']} Update"
    body = f"Dear {user['name']},\n\nYour flight {flight['flight_number']} has been updated.\nStatus: {flight['status']}\nDeparture: {flight['departure_date']} {flight['departure_time']}\nArrival: {flight['arrival_date']} {flight['arrival_time']}\n\nBest regards,\nFlight Notification Service"
    #send_email(user['email'], subject, body)


def notify_users(flight_update):
    global latest_flight_update
    latest_flight_update = flight_update  # Update the global variable with the latest update

    # Extract details from the flight update
    flight_number = flight_update['flight_number']
    status = flight_update['status']
    departure_date = flight_update['departure_date']
    departure_time = flight_update['departure_time']
    arrival_date = flight_update['arrival_date']
    arrival_time = flight_update['arrival_time']

    # Combine date and time into a single datetime object
    departure_datetime_str = f"{departure_date}T{departure_time}Z"
    departure_datetime = datetime.fromisoformat(departure_datetime_str.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
    
    print(f"Received flight update: Flight Number: {flight_number}, Status: {status}, Departure Time: {departure_datetime}")
    print(f"Type of Kafka departure_datetime: {type(departure_datetime)}, Value: {departure_datetime}")

    # Check if the departure time is in the future
    now = datetime.now(timezone.utc)
    if departure_datetime <= now:
        print("Flight departure time is in the past. No notifications will be sent.")
        return
    
    # Find users who have the same flight number and match the departure date
    user_query = {
        'flight_number': flight_number,
        'departure_date': departure_date,
        'departure_time': departure_time
    }

    users_to_notify = users_collection.find(user_query)

    for user in users_to_notify:
        user_departure_date = user['departure_date']
        user_departure_time = user['departure_time']
        user_departure_datetime_str = f"{user_departure_date}T{user_departure_time}Z"
        user_departure_datetime = datetime.fromisoformat(user_departure_datetime_str.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)

        # Print statements to check values and types
        print(f"User's departure_date: {user_departure_date}")
        print(f"User's departure_time: {user_departure_time}")
        print(f"Type of user's departure_datetime: {type(user_departure_datetime)}")
        print(f"Parsed user's departure_datetime: {user_departure_datetime}")

        # Check if the user's departure time matches and if it hasn't passed
        if user_departure_datetime == departure_datetime:
            print(f"User {user['name']} matches the flight update criteria.")
            send_notification(user, flight_update)
        else:
            print(f"User {user['name']} does not match the criteria.")

# Kafka consumer thread function
def consume_flight_updates():
    consumer = KafkaConsumer(
        'flight_updates',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for message in consumer:
        flight_update = message.value
        print(f"Received message: {flight_update}")
        notify_users(flight_update)

# Start the Kafka consumer in a separate thread
consumer_thread = threading.Thread(target=consume_flight_updates)
consumer_thread.start()

@app.route('/update', methods=['GET'])
def get_update():
    global latest_flight_update
    if latest_flight_update:
        return Response(
            json.dumps(latest_flight_update),
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({"status": "No updates available"}),
            mimetype='application/json'
        )

if __name__ == "__main__":
    app.run(port=5002)
