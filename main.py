import os
import sys
import requests
import datetime
import fbchat
from fbchat import Client
from fbchat.models import *


client = Client('<fb user email>', '<fb user password>')
thread_id = "<messenger group or user chat id>"
thread_type = ThreadType.GROUP #Or ThreadType.USER for user chat 
announcements_url = "https://apps.it.teithe.gr/api/announcements/public"
response = requests.get(url=announcements_url)
announcements_data = response.json()
count_ann_file =  open('count_ann','r')
ann_count_last = int(count_ann_file.read())
ann_count_now = len(announcements_data)
print("Last Count: "+ str(ann_count_last))
print("Recently Count: "+ str(ann_count_now))

if ann_count_now > ann_count_last:
    print("We have new announcements, lets take a look")
    count_ann_file = open('count_ann', 'w')
    count_ann_file.write(str(ann_count_now))
    recent_ann = announcements_data[0] #0 is the latest post
    ann_id = recent_ann['_id']
    ann_type = recent_ann['_about']['name']
    ann_title = recent_ann['title']
    ann_desc = recent_ann['text']
    ann_date = recent_ann['date'] #API Format: 2019-09-27T16:26:44.325Z
    ann_author = recent_ann['publisher']['name']
    split_datetime_data = ann_date.split('T')
    split_date = split_datetime_data[0].replace('-', '/').split('/')
    dt_stamp = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    date = dt_stamp.strftime('%d/%m/%Y')

    time = split_datetime_data[1][:8]

    print('--- NEW announcement ('+ str(ann_id) +') ['+ str(ann_type) +'] --- \n')
    print("Uploaded at "+ str(date)+ " "+ str(time) + " by "+ ann_author + " \n")
    print("Title: <<"+ ann_title +">> \n")
    print(ann_desc + " \n")
    attachments_array = recent_ann['attachments']
    if len(attachments_array) > 0 :
        count_attachments = len(attachments_array)
        print("We have " + str(count_attachments) + " attachments \n")
        for x in attachments_array:
            print("Name: "+ x['name'] + " URL: https://apps.it.teithe.gr/api/announcements/"+ str(ann_id) +"/download/"+ str(x['_id'])+ " \n")
    else:
        print("No attachments")

    if ann_type == "Νέα Τμήματος" or ann_type == "Ανακοινώσεις Γραμματείας" or ann_type == "Τεχνικά Θέματα": #You can choose when to send message or not, in which post_type
        print("Send announcement to the group")
        if len(attachments_array) > 0:
            message = '*Νέα Ανακοίνωση [' + str(ann_type) + ']*\n Δημιουργήθηκε *' + str(date) + ' ' + str(time) + '* από *' + str(ann_author) + '*\n Τίτλος: *<<' + str(ann_title) + '>>*\n\n' + str(ann_desc) + '\n\n*Βρέθηκε '+str(len(attachments_array))+' συνημμένο/α:* \n'
            for x in attachments_array:
                #print("Name: " + x['name'] + " URL: https://apps.it.teithe.gr/api/announcements/" + str(ann_id) + "/download/" + str(x['_id']) + " \n")
                message += '\n* *['+ x['name'] +'] => (https://apps.it.teithe.gr/api/announcements/' + str(ann_id) +'/download/'+ str(x['_id'])+')*\n'
            message += '\n Σύνδεσμος Ανακοίνωσης: https://apps.it.teithe.gr/api/announcements/' + str(ann_id) + ' \n'
        else:
            message = '*Νέα Ανακοίνωση [' + str(ann_type) + ']*\n Δημιουργήθηκε *' + str(date) + ' ' + str(time) + '* από *' + str(ann_author) + '*\n Τίτλος: *<<' + str(ann_title) + '>>*\n\n' + str(ann_desc) + '\n\n*Κανένα συνημμένο/α* \n\nΣύνδεσμος Ανακοίνωσης: https://apps.it.teithe.gr/api/announcements/' + str(ann_id) + ' \n'
        client.send(Message(text=str(message)), thread_id=thread_id, thread_type=thread_type)

else:
    print("Nothing new, all good :)")



