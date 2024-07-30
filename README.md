Here's an updated GitHub README with details on how to set up and run the Kafka and MongoDB components for your notifications microservice:

---

# Notifications Microservice

Welcome to the **Notifications Microservice** repository! This microservice handles notifications for various events and provides an API for clients to interact with.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

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

   The microservice will be accessible at `http://localhost:5000` by default.

## API Endpoints

Here are some example API endpoints:

- **Send Notification**

  ```http
  POST /notifications
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
  GET /notifications
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
