import yaml
import os
import time
import firebase_admin
from firebase_admin import credentials, firestore
from stopwords import stopwords
from cryptography.fernet import Fernet
from pprint import pprint

credential = yaml.load(open('credential.yml'), Loader=yaml.FullLoader)


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'Email-Classification-Service': 'projectId',
})
db = firestore.client()

docs = db.collection(u'mails').stream()

for doc in docs:
    pprint(f'{doc.id} => {doc.to_dict()}')
