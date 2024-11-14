# SelfActualize - Communications Service

This is a FastAPI app built based on the instructions provided in the take home test.

There are many component:
1. FastAPI app - The core app that contains the logic as well as REST endpoints to accept a users request to send message.
    - `controllers` - Contains the `message_controller` which has endpoints the user can hit.
    - `db` - Contains code related to the PSQL DB and Redis (Used for implementing the Queue as well as Batch-Write to DB)
    - `services` - Contains logic to send message as well as write to DB.

    The `sender` class is the base class and can be inherited to implement different types of senders in future. Currently there are 2 types of senders
    1. SmsSender
    2. EmailSender

2. There is GitHub CI/CD setup to run tests on merge as well as run the containers locally.

3. There is a docker-compose file that contains information about all the services.


The Backend requirements are straight forward and REST endpoints are exposed. 

`POST /api/v1/sendMessage` takes in user payload and sends a message based on message type and logs the transaction to DB.
`POST /api/v2/sendMessage` takes in user payload and pushes the request to a queue (Implemented with Redis/Celery for now but could use SQS in production). This functionality is implemented to write to DB asynchornously.

There is another flag called `USE_LOG_BUFFER` which is set to true in code. When set to true, the log messages to be written to DB are batched in Redis and flushed to the DB every minute. (Can extend this functionality by accepting the CRON). This is being done using Celery and Celery Beat.

There are tests in the test folder which can be run by using the command `pytest tests`

To run the app, you should have docker installed. Just run the following next:
```
docker-compose up --build
```