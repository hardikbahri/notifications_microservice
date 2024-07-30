# Notifications Microservice

Welcome to the **Notifications Microservice** repository! This microservice handles notifications for various events and provides an API for clients to interact with.
![image](https://github.com/user-attachments/assets/942dfbb3-fe2f-46ff-9a74-b9116082cbc2)

### EMAIL NOTIFICATIONS
![image](https://github.com/user-attachments/assets/342d4970-7b8f-44b6-94fc-efe2dca7dd27)

Whenever flight status is changed, the code automatically detects the change using kafka, the backend checks the users database and sends email to the users who have booked the same flight on that particular date, Everything is automated

### REAL TIME UPDATES!
![image](https://github.com/user-attachments/assets/b6e43316-bb89-4d84-916e-6bda19e0f4ed)

No need to reload the site, this microservice uses kafka and mongodb replica sets to display real time updates on the website! Whenever the database is changed, the code automatically detects the changes, the frontend uses polling mechanism to fetch the updated changes , everything is automatic!

### Flights collection in mongodb
![image](https://github.com/user-attachments/assets/9fa9e65b-92f5-46fc-a8fb-3d43f62c25ed)
### users database collection in mongodb
![image](https://github.com/user-attachments/assets/d9753cf5-2418-41d9-bb65-e647f0f2f795)

### Architecture Overview

1. **Database Change Detected**: A change in the MongoDB database (e.g., a flight status update) is detected.
2. **Change Received**: The backend service receives the change.
3. **Process Change Stream**: The backend processes the change stream.
4. **Send Message**: The backend sends a message to the Kafka Producer.
5. **Send Topics**: The Kafka Producer sends the message to the appropriate Kafka topic.
6. **Consumer Message**: The Kafka Consumer receives the message from the Kafka topic.
7. **API Call Using Polling Mechanism**: The frontend makes an API call to the backend using a polling mechanism to get updates.
8. **Real-Time Updates, Push Notifications**: The frontend receives real-time updates and push notifications.
9. **Email Sent**: An email is sent as part of the notification process.

### Components

- **MongoDB**: Acts as the database where changes are detected.
- **Backend**: Processes the change stream and sends messages to Kafka.
- **Kafka Producer**: Sends messages to Kafka topics.
- **Kafka Consumer**: Consumes messages from Kafka topics.
- **Frontend**: Uses API polling to fetch updates and displays real-time notifications and flight status updates.
- **Email Service**: Sends email notifications as part of the notification workflow.

### File Structure

- `change_streams.py`: This file contains the Flask application that handles receiving flight updates from the Kafka topic and notifying users via email and SMS.
- `notify_users.py`: This file handles the MongoDB change stream and sends relevant flight updates to a Kafka topic.

### How It Works

#### Backend Service (`change_streams.py`)

1. **Flask Setup**: The Flask app is set up with CORS enabled for the `/update` endpoint.
2. **MongoDB Connection**: Connects to MongoDB to access the flight status and user information.
3. **Email Function**: Defines a function to send email notifications using SMTP.
4. **Notification Function**: Combines email and SMS notifications and sends them to users based on flight updates.
5. **Kafka Consumer**: Listens to the `flight_updates` topic on Kafka and processes messages to notify users.
6. **API Endpoint**: Provides an endpoint to fetch the latest flight update.

#### Kafka Producer (`notify_users.py`)

1. **MongoDB Connection**: Connects to MongoDB to watch for changes in the flights collection.
2. **Kafka Setup**: Configures Kafka producer to send messages to the `flight_updates` topic.
3. **Process Change Function**: Processes the change stream from MongoDB and sends relevant updates to Kafka.
4. **Change Stream Listener**: Listens to changes in the flights collection and processes them.

### Running the Application

1. **Start MongoDB**: Ensure MongoDB is running locally.
2. **Start Kafka**: Ensure Kafka is running locally.
3. **Run Kafka Producer**: 
   ```sh
   python producer.py
   ```
4. **Run Flask App**:
   ```sh
   python app.py
   ```
5. **Frontend**: Make API calls to the `/update` endpoint to fetch the latest flight updates.

### Conclusion

This notification microservice efficiently processes flight status updates and notifies users in real-time via email and SMS. The combination of MongoDB, Kafka, and Flask provides a robust and scalable solution for real-time notifications.

---

This README provides a clear overview of the architecture and the workflow, with references to the relevant files without including the entire code.
## Features

- Real-time notification delivery
- Integration with Kafka for event streaming
- MongoDB replica set for database high availability

## Installation

To get started with the Notifications Microservice, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/hardikbahri/notifications_microservice.git
   cd notifications_microservice
   ```

2. **Install Dependencies**

   Ensure you have Python installed. Then, install the necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory and set up the necessary environment variables. Example:

   ```
   DATABASE_URL=your_database_url
   KAFKA_BROKER_URL=your_kafka_broker_url
   ```

## Usage

1. **Start Kafka**

   To start Kafka, you need to run Zookeeper and Kafka servers:

   ```bash
   # Start Zookeeper
   bin/zookeeper-server-start.sh config/zookeeper.properties

   # Start Kafka server
   bin/kafka-server-start.sh config/server.properties
   ```

2. **Set Up MongoDB Replica Set**

   Run the following commands to set up a MongoDB replica set. This should be done only once:

   ```bash
   # Start MongoDB instances
   mongod --dbpath "C:\Program Files\MongoDB\Server\6.0\data" --port 27017 --bind_ip 127.0.0.1
   taskkill /F /IM mongod.exe     # Terminate if it creates errors
   mongod --dbpath "C:\Program Files\MongoDB\Server\6.0\data" --port 27018 --bind_ip 127.0.0.1
   mongod --dbpath "C:\Program Files\MongoDB\Server\6.0\data" --port 27019 --bind_ip 127.0.0.1

   # Initialize MongoDB replica set
   mongod --dbpath "C:\Program Files\MongoDB\Server\6.0\data" --port 27017 --replSet "rs0" --bind_ip 127.0.0.1
   mongod --dbpath "C:\Program Files\MongoDB\Server\6.0\data2" --port 27018 --replSet "rs0" --bind_ip 127.0.0.1
   mongod --dbpath "C:\Program Files\MongoDB\Server\6.0\data3" --port 27019 --replSet "rs0" --bind_ip 127.0.0.1

   # Connect to MongoDB and initialize replica set
   mongosh --port 27017
   ```

   Inside the `mongosh` shell, run:

   ```javascript
   rs.initiate({
     _id: "rs0",
     members: [
       { _id: 0, host: "127.0.0.1:27017" },
       { _id: 1, host: "127.0.0.1:27018" },
       { _id: 2, host: "127.0.0.1:27019" }
     ]
   })
   ```

3. **Run the Microservice**

   Start the microservice using:

   ```bash
   python app.py
   ```

   or, if you use a specific entry point:

   ```bash
   flask run
   ```

4. **Access the API**

   The microservice will be accessible at `http://localhost:5002` by default.

## API Endpoints

Here are some example API endpoints:

- **Send Notification**

  ```http
  POST /update
  ```

  **Request Body**:

  ```json
  {
    "type": "email",
    "message": "Your account has been updated."
  }
  ```

  **Response**:

  ```json
  {
    "status": "success",
    "message": "Notification sent successfully."
  }
  ```

- **Get Notifications**

  ```http
  GET /update
  ```

  **Response**:

  ```json
  [
    {
      "id": 1,
      "type": "email",
      "message": "Your account has been updated."
    }
  ]
  ```

## Configuration

- **Environment Variables**: Ensure you have configured environment variables as specified in the `.env` file.
- **Database Configuration**: Set up your database connection in the configuration file.

## Testing

To run tests for the microservice, use:

```bash
pytest
```

Ensure you have `pytest` installed:

```bash
pip install pytest
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them.
4. Submit a pull request with a description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to further customize the README based on your specific needs and details. Let me know if you need any additional information or help!
