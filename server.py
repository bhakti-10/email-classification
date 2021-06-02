from imap_tools import MailBox, AND
from pprint import pprint
import yaml, os, time
import firebase_admin
from firebase_admin import credentials, firestore
from stopwords import stopwords

credential = yaml.load(open('credential.yml'),Loader=yaml.FullLoader)

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'Email-Classification-Service': 'projectId',
})
db = firestore.client()

def processCsv(filename):
    f = open(filename, "r")
    l2 = []
    l1 = f.read()
    l1 = l1.split('\n')
    l1 = l1[1::]
    for x in l1:
        x = x.split(',')[0]
        for y in x.split():
            l2.append(y.lower())
    return l2

def removeStopwords(l1):
    final = []
    for x in l1:
        if x not in stopwords:
            final.append(x)
    return final

hr = list(set(processCsv("hr.csv")))
marketing = list(set(processCsv("marketing.csv")))
finance = list(set(processCsv("finance.csv")))
research = list(set(processCsv("research.csv")))
hr = removeStopwords(hr)
marketing = removeStopwords(marketing)
finance = removeStopwords(finance)
research = removeStopwords(research)

def getCategory(hr, marketing, finance, research, userString):
    hu = mk = fn = rs = 0
    for x in userString:
        if x in hr: hu+=1
        if x in marketing: mk+=1
        if x in finance: fn+=1
        if x in research: rs+=1
    if hu==max([hu,mk,fn,rs]): return 'HR'
    if mk==max([hu,mk,fn,rs]): return 'MK'
    if fn==max([hu,mk,fn,rs]): return 'Finance'
    if rs==max([hu,mk,fn,rs]): return 'Research'

# userString = input().
# print(getCategory(hr, marketing, finance, research, userString)) 

while(True):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time,"Checking for emails...")
    mailbox = MailBox('imap.gmail.com')
    mailbox.login(credential['gmail']['email'],credential['gmail']['password'], initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
    mails=mailbox.fetch(AND(seen=False))
    for mail in mails:
        print("New Email received from: ",mail.from_)
        doc_ref = db.collection(u'mails').document()
        doc_ref.set({
            u'to':mail.to,
            u'from':mail.from_,
            u'date':mail.date,
            u'subject':mail.subject,
            u'text':mail.text,
            u'category': getCategory(hr, marketing, finance, research, str(mail.subject).lower().split())
        })
    mailbox.logout()
    




