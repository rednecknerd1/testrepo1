from os import read
from pickle import FALSE, TRUE
from pandas.io.parsers.readers import read_csv
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import smtplib
import re
import mailtrap as mt



l = ["Russia", "China", "Chinese", "Iran", "Iranian", "Iranian","Microsoft", "Cisco"]
#https://mailtrap.io/sending/domains/
data1 = ''
def url1():
    global data1
    global l
    url = "https://thehackernews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='story-link')

    for article in articles:
        header = article.find('h2', class_='home-title').get_text(strip=True)
        description = article.find('div', class_='home-desc').get_text(strip=True)
        #print(article['href'])
        response1 = requests.get(article['href'])
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        cves = re.findall(r'CVE-\d{4}-\d{4,}', str(soup1))
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\[\.\]\d{1,3}', str(soup1))

        if any(word in header for word in l) or any(word in description for word in l):
        #if re.search('Russia|Microsoft', header) or re.search('Russia|Microsoft',description):
          #response1 = requests.get(article['href'])
          #soup1 = BeautifulSoup(response.text, 'html.parser')
          #for cve in soup1:
            #cves = re.findall(r'CVE-\d{4}-\d{4,}', str(cve))
            #ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', str(cve))
            #soup2 = str(soup1)
          #print(soup2[:50])
          #cves = re.findall(r'CVE-\d{4}-\d{4,}', soup2)
            #print("---------These are the CVEs----------" + str(cves))
            cves = str(cves)
            cves = cves.replace("[", "")
            cves = cves.replace("]", "")
            #ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', soup2)
            #print("---------These are the IPs---------" + str(ips))
            ips = str(ips)
            ips = ips.replace("[", "")
            ips = ips.replace("]", "")

            data = header+ ":" + "\n\n" + description[0:500]+"..." + "\n\n" + "CVEs \n" + cves + "\n" + "IPs\n" + ips + "\n\n" + article['href'] + "\n\n"
            data = str(data)
        #data = re.sub(r'\s\s', ' ',data)
            data = re.sub(r'\t', '',data)
        #print(data)
            data1 = data1 + "\n\n\n\n" + data




def url2():
  global data1
  global l
  print("-------bleep----")
  url = "https://www.bleepingcomputer.com/"
  response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'})
  print(str(response))
  soup = BeautifulSoup(response.text, 'html.parser')
  articles = soup.find_all('li')


  for article in articles:
    header = article.find('h4')
    description = article.find('p')
    link = article.find('a', href=True)
    #link = str(link['href'])
    #link = re.findall(r'(?:https?|ftp):\/\/[^\s/$.?#].[^\s]+', link)
    

    if header is not None and description is not None:
      header1 = header.text.strip()
      description1 = description.text.strip()[0:500]
      

      if any(word in header1 for word in l) or any(word in description1 for word in l):
        response1 = requests.get(link['href'])
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        cves = re.findall(r'CVE-\d{4}-\d{4,}', str(soup1))
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', str(soup1))
        cves = str(cves)
        ips = str(ips)
        ips = ips.replace("0.0.1.1", "")
        ips = ips.replace("1.1.1.1", "")
        ips = ips.replace("\'", '')
        ips = ips.replace(",", ' ')
        cves = cves.replace("[", "")
        cves = cves.replace("]", "")
        ips = ips.replace("]", "")
        ips = ips.replace("[", "")
        

        data = header1 + ":" + "\n\n" + description1[0:500] + "..." + "\n\n" + "CVEs \n" + cves + "\n" + "IPs\n" + ips + "\n\n" + str(link['href']) + "\n\n"
        data = str(data)
        data1 = data1 + "\n\n\n\n" + data


if __name__ == "__main__":
  url1()
  url2()
  print(data1)




#https://mailtrap.io/blog/python-send-email/#:~:text=Base64%20encoding%3A%20Since%20email%20protocols,is%20used%20for%20this%20purpose.
# create mail object
receivers = ['xxx@gmail.com', 'xxx@gmail.com']

for x in receivers:
  mail = mt.Mail(
    sender=mt.Address(email="mailtrap@xxx.com", name=" News Update"),
    to=[mt.Address(email=x)],
    subject="Cyber Intel Update",
    text= "Current cyber intel news regarding your areas of interest" + "\n" + data1,
)

# create client and send
  client = mt.MailtrapClient(token="<API TOKEN GOES HERE>")
  client.send(mail)


#SMTPLIB option
'''

sender = "Email Testing <mailtrap@xxx.com>"
receiver = "A Test User <xxx@gmail.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}


Cyber Intel News.



"""

with smtplib.SMTP("bulk.smtp.mailtrap.io", 587) as server:
    server.starttls()
    server.login("api", "<API TOKEN GOES HERE>")
    server.sendmail(sender, receiver, message)

'''
