import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
RUTARRD = 'RRDs/'
RUTAGRA = 'Graficas/'

mailsender = "khort93@gmail.com"
mailreceip = "khort93@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'Ui72EGsPpxJM7LH'

def send_alert_attached(subject: str, imagen:str):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    m = 'Estimado usuario, su computadora se está quemando.\nLe recomendamos usar el extintor mas cercano y correr por su vida.'
    msg.attach(MIMEText(m, _charset='utf-8'))
    fp = open(RUTAGRA+imagen, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()
