import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAHUP96N1jxm7MfAhrqK3ExxAVS6lqAlYA",
    "authDomain": "pyrebase-auth.firebaseapp.com",
    "projectId": "pyrebase-auth",
    "storageBucket": "pyrebase-auth.appspot.com",
    "messagingSenderId": "278748329803",
    "appId": "1:278748329803:web:65aa8082b970ba2f2e5ace",
    "databaseURL": "https://pyrebase-auth-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(config=firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
