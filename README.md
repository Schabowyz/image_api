# Image api


## Description

API for uploading and sharing images with specific abilities based on user's tiers. Created in order to learn DRF and as a recruitment task.


## Usage

### Startup
1. Clone the repository or download it to your hard drive.
2. Open projects directory and run command "docker compose up --build"
3. Once the app is running you can use any software to communicate with it. Personally I'm using Postman which I find very convinient. App should be running on http://127.0.0.1:8000

### Functions
1. Registration - you have to use admin panel in django to create new users. Credentials are login: admin, pw: admin. You can use any password when creating a user due to disabled validators.
2. Log in:\
http://127.0.0.1:8000/login \
METHOD: POST\
{"username": "YOURUSERNAME", "password": "YOURPASSWORD"}\
Returns auth token
4. Images listning:\
http://127.0.0.1:8000/images \
METHOD: GET\
HEADER: Authorization Token YOURTOKENSTRING\
Returns list of images with links for sharing
6. Image upload:\
http://127.0.0.1:8000/upload \
METHOD: POST\
HEADER: Authorization Token YOURTOKENSTRING\
{"image": YOURIMAGEFILE}\
Returns image links for sharing
8. Generate expiring link:\
http://127.0.0.1:8000/share/<original_link>/<expiration_time_seconds> \
METHOD: POST\
HEADER: Authorization Token YOURTOKENSTRING\
Returns link to image of choice, in size of choice, working for the time of choice. Link will be now visible in images links, untill someone opens it after time expires.
10. CRUD for user tiers and tier's rights in admin panel.

### Built in tiers/users
There are few users and tiers for testing, their credentials are:

username: basic / password: basic / basic tier account:\
    - a link to thmbnail that's 200px in height

username: premium / password: premium / premium tier account:\
    - a link to thmbnail that's 200px in height\
    - a link to thmbnail that's 400px in height\
    - a link originally uploaded image

username: enterprise / password: enterprise / enterprise tier account:\
    - a link to thmbnail that's 200px in height\
    - a link to thmbnail that's 400px in height\
    - a link originally uploaded image\
    - ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))
