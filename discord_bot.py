#!/usr/bin/env python3.7
import os
import sys
import requests
import logging
from datetime import datetime
import time
import discord
import asyncio



now = datetime.now()
currentdatetime_string = now.strftime("%d/%m/%Y %H:%M:%S")
channel_id = "1234567890" #Discord Channel ID
print('WELCOME :)')
print('Running datetime: ', currentdatetime_string)


client = discord.Client()

@client.event
async def on_ready(self):
        print('Logged on as', self.user)

@client.event
async def on_guild_available(message):
    print("Server available, gathering information :)")
    channel_ann = client.get_channel(1234567890) #Discord Announcements Channel ID
    channel_debug = client.get_channel(1234567890) #Discord Debug/Logs Channel ID (Optional)
    try:
        print('Running datetime: ', currentdatetime_string)
        announcements_url = "https://apps.it.teithe.gr/api/announcements/public"
        response = requests.get(url=announcements_url)
        announcements_data = response.json()
        count_ann_file = open('count_ann', 'r')
        ann_count_last = int(count_ann_file.read())
        ann_count_now = len(announcements_data)
        print("Last Count: " + str(ann_count_last))
        await channel_debug.send("Last Count: " + str(ann_count_last))
        print("Recently Count: " + str(ann_count_now))
        await channel_debug.send("Recently Count: " + str(ann_count_now))

        if ann_count_now > ann_count_last:
            print("We have new announcements, lets take a look")
            count_ann_file = open('count_ann', 'w')
            count_ann_file.write(str(ann_count_now))
            count_ann_file.close()
            recent_ann = announcements_data[0]  # 0 is the latest
            ann_id = recent_ann['_id']
            ann_type = recent_ann['_about']['name']
            ann_title = recent_ann['title']
            ann_desc = recent_ann['text']
            ann_date = recent_ann['date']  # 2019-09-27T16:26:44.325Z
            ann_author = recent_ann['publisher']['name']
            split_datetime_data = ann_date.split('T')
            split_date = split_datetime_data[0].replace('-', '/').split('/')
            dt_stamp = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))
            date = dt_stamp.strftime('%d/%m/%Y')

            time = split_datetime_data[1][:8]

            print('--- NEW announcement (' + str(ann_id) + ') [' + str(ann_type) + '] --- \n')
            print("Uploaded at " + str(date) + " " + str(time) + " by " + ann_author + " \n")
            print("Title: <<" + ann_title + ">> \n")
            print(ann_desc + " \n")
            attachments_array = recent_ann['attachments']
            if len(attachments_array) > 0:
                count_attachments = len(attachments_array)
                print("We have " + str(count_attachments) + " attachments \n")
                for x in attachments_array:
                    print("Name: " + x['name'] + " URL: https://apps.it.teithe.gr/api/announcements/" + str(
                        ann_id) + "/download/" + str(x['_id']) + " \n")
            else:
                print("No attachments")

            if ann_type == "Νέα Τμήματος" or ann_type == "Ανακοινώσεις Γραμματείας" or ann_type == "Τεχνικά Θέματα" or ann_type == "Εκδηλώσεις":
                print("Send announcement to the group")

                if len(attachments_array) > 0:
                    message = '@everyone *Νέα Ανακοίνωση [' + str(ann_type) + ']*\n Δημιουργήθηκε *' + str(date) + ' ' + str(
                        time) + '* από *' + str(ann_author) + '*\n Τίτλος: *<<' + str(ann_title) + '>>*\n ```' + str(
                        ann_desc) + '``` \n*Βρέθηκε ' + str(len(attachments_array)) + ' συνημμένο/α:* \n'
                    for x in attachments_array:
                
                        message += '\n`[' + x['name'] + ']` https://apps.it.teithe.gr/api/announcements/' + str(ann_id) + '/download/' + str(x['_id']) + '\n'

                    message += '\n Σύνδεσμος Ανακοίνωσης: https://apps.it.teithe.gr/api/announcements/' + str(
                        ann_id) + ' \n'
                else:
                    message = '@everyone *Νέα Ανακοίνωση [' + str(ann_type) + ']*\n Δημιουργήθηκε *' + str(date) + ' ' + str(
                        time) + '* από *' + str(ann_author) + '*\n Τίτλος: *<<' + str(ann_title) + '>>*\n```' + str(
                        ann_desc) + '```\n*Κανένα συνημμένο/α* \n\nΣύνδεσμος Ανακοίνωσης: https://apps.it.teithe.gr/api/announcements/' + str(
                        ann_id) + ' \n'

                await channel_ann.send(str(message))
                now = datetime.now()
                currentdatetime_string2 = now.strftime("%d/%m/%Y %H:%M:%S")
                await channel_debug.send("Η Ανακοίνωση (" + str(ann_id) + ") [" + str(ann_type) + "] ["+ str(ann_title) + "] στάλθηκε  {"+ str(currentdatetime_string2)+"}") # Discord Debug/Logs Channel Message Notify (Optional)

        else:
            print("Nothing new, all good :)")
            now = datetime.now()
            currentdatetime_string3 = now.strftime("%d/%m/%Y %H:%M:%S")
            await channel_debug.send("Καμία ανακοίνωση {"+ str(currentdatetime_string3) + "") # Discord Debug/Logs Channel Message Notify (Optional)

    except Exception as e:
        print(str(e))
        now = datetime.now()
        currentdatetime_string3 = now.strftime("%d/%m/%Y %H:%M:%S")
        await channel_debug.send("Η Ανακοίνωση (" + str(ann_id) + ") [" + str(ann_type) + "] [" + str(ann_title) + "] ΔΕΝ στάλθηκε  {" + str(currentdatetime_string3) + "} \n\n\n "+(str(e) + "")) # Discord Debug/Logs Channel Message Notify (Optional)
        logging.exception(str(e))
    sys.exit("Done :)")

client.run('<discord bot token here>')







