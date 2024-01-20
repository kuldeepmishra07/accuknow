# accuknox
Social_media_project

# Django Rest Framework User Authentication and Friendship API

This Django project provides a RESTful API for user authentication and managing friendships.

### Prerequisites

- Python 3.x
- Docker (optional, for containerization)

### Installing Dependencies

Install the required Python packages using pip:

pip install -r requirements.txt

To test the functionalities using cURL, you can use the following commands. 
Make sure your Django development server is running **python manage.py runserver**


### OR to setup project using dockerfile 


# mydrfproject Docker Setup

This guide explains how to set up and run the Django project `mydrfproject` using Docker.

## Prerequisites

- Docker installed on your machine.

## Build Docker Image

Navigate to the project directory containing the Dockerfile and execute the following command to build the Docker image:

```bash
docker build -t mydrfproject .



### Curl to Test Functionalities

**Register a new user:**

curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword", "email": "test@example.com"}' http://localhost:8000/api/register/

**Login and get the authentication token:**

curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:8000/api/login/

**Search users:**

curl -X GET -H "Authorization: Token YOUR_AUTH_TOKEN" "http://localhost:8000/api/search/?keyword=am&page=1"


**Send friend request:**

curl -X POST -H "Authorization: Token YOUR_AUTH_TOKEN" "http://localhost:8000/api/friend-request/send/2/"


**Accept friend request:**

curl -X POST -H "Authorization: Token YOUR_AUTH_TOKEN" "http://localhost:8000/api/friend-request/accept/1/"


**Reject friend request:**

curl -X POST -H "Authorization: Token YOUR_AUTH_TOKEN" "http://localhost:8000/api/friend-request/reject/1/"


**List friends:**

curl -X GET -H "Authorization: Token YOUR_AUTH_TOKEN" "http://localhost:8000/api/friends/"


**List pending friend requests:**

curl -X GET -H "Authorization: Token YOUR_AUTH_TOKEN" "http://localhost:8000/api/friend-requests/pending/"

