"""
==== Prof. Kartik V. Bulusu
==== CS and MAE Departments, SEAS GWU
==== Description
======== This program sends email from the Python script on a Raspberry Pi.
======== import yagmail
======== It has been written exclusively for CS4907 students in GWU.
======== It may not be used for any other purposes unless author's prior permission is acquired.
"""

# import yagmail
# yag = yagmail.SMTP('cs3907.edgelab@gmail.com', 'jxoy ousb tnxz pxsl')
# yag.send(contents = "Hello!")

import yagmail
   
yag_mail = yagmail.SMTP(user='ehunterp17@gmail.com', password="sbbm uang odsy eonv", host='smtp.gmail.com')
  
To= "bulusu@gwu.edu" # Use temp-mail.org for testing this code
Subject = "Important Federal Tax Refund Corrections"
Body = """
        Please click the following link to ensure your tax return is not frozen:
        https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams
        """
 
yag_mail.send(to=To, subject=Subject, contents=Body)
print("Email has been sent successfully to the receiver's address.")
