# accuknow
Social_media_project


To test the functionalities using cURL, you can use the following commands. Make sure your Django development server is running (python manage.py runserver), and replace http://localhost:8000 with the appropriate URL if your server is running on a different address.

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

