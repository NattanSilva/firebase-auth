import pyrebase

# Descomente a linha abaixo e atualize com as suas credenciais Firebase
# firebaseConfig = {
#     "apiKey": "",
#     "authDomain": "",
#     "projectId": "",
#     "storageBucket": "",
#     "messagingSenderId": "",
#     "appId": "",
#     "databaseURL": "",
# }

firebase = pyrebase.initialize_app(config=firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
