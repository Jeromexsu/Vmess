import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
def mail(usr:str, psw:str, to:str, html_text:str, subject:str, attaches:list):
    mail = smtplib.SMTP_SSL('smtp.exmail.qq.com')
    mail.connect('smtp.exmail.qq.com',465)
    mail.login(usr,psw)

    msg = MIMEMultipart()
    msg['From'] = Header(usr)
    msg['To'] = Header(to)
    msg['Subject'] = Header(subject,'utf-8')
    msg.attach(MIMEText(html_text,"html","utf-8"))
    for attach_uri in attaches:
        with open(attach_uri) as file:
            attach = MIMEText(file.read(),"base64","utf-8")
        attach["Content-Type"] = 'application/octet-stream'
        filename = attach_uri[attach_uri.rfind('/')+1:]
        attach["Content-Disposition"] = 'attachment; filename=%s' % filename
        msg.attach(attach)

    mail.sendmail(usr,to,msg.as_string())
    mail.quit()