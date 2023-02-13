import smtplib
from email.mime.text import MIMEText
from email.header import Header
def mail(usr:str,psw:str,to:str,text:str,subject:str):
    mail = smtplib.SMTP_SSL('smtp.exmail.qq.com')
    mail.connect('smtp.exmail.qq.com',465)
    mail.login(usr,psw)
    msg = MIMEText(text,'plain','utf-8')
    msg['From'] = Header(usr)
    msg['To'] = Header(to)
    msg['Subject'] = Header(subject,'utf-8')
    mail.sendmail(usr,to,msg.as_string())
    mail.quit()