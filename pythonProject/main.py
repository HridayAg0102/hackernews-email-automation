import requests  # http requests
from bs4 import BeautifulSoup  # webscraping
# send the mail
import smtplib
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system data and time manipulation
import datetime


# email content placeholder
content = ''


def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ""  # will be used to assign value to the global content variable.
    cnt += ("<b>HN Top Stories:</b>\n" + "<br>" + "-" * 50 + "<br>")
    # this part just gives more readability and base for email text.
    response = requests.get(url)
    content = response.content
    # get the content of the webpage
    # {this content is a local variable
    # don't confuse it with global content variable}
    soup = BeautifulSoup(content, "html.parser")

    for i, tag in enumerate(soup.find_all("td", attrs={"class": "title", "valign": ""})):
        # 1. td is a tag in html dor table data, used hear to find elements with this tag
        # 2. attrs -- attributes of the HTML tag
        # 3. we want class = title but don't want a td with valign attribute, so left it blank

        cnt += ((str(i + 1) + ' :: ' + tag.text + "\n" + '<br>') if tag.text != 'More' else '')
        # i is used for row number, so, to make it 1 indexed, we do i+1
        # .text after tag is used to retrieve only the content within the tags.
        # there is a content called 'More' at the end of the page, which must be ignored in our program (see md file)
    return (cnt)


cnt = extract_news('https://news.ycombinator.com/')  # url of hackernews
content += cnt
content += ('<br>--------<br>')
content += ('<br><br> END OF MESSAGE')


# ===================#
# LET'S SEND EMAIL :)

print("Composing Email ...")

# update your email details
#==============================================
SERVER = "smtp.gmail.com" # "Our smtp server"
PORT = 587 # port number
FROM = 'sendermail@gmail.com' # email sent from this
TO = ["email1@gmail.com","email2@gmail.com"]
PASS = "<your password here>" # email password
#==============================================

# structureing different parts of Email
msg = MIMEMultipart()
now = datetime.datetime.now()

msg["Subject"] = "Top stories from Hackernews [Automated Email]" +' ' + str(
    now.day) + '-' + str(now.month) + '-'+ str(now.year)

msg.attach(MIMEText(content,'html'))
# this creates the content of the Email in HTML format


# AUTHENTICATION SECTION #
print("Initialising Server...\n")

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
# this gives all the errors during our execution
# set it to 0 if you don't need errors to display

server.ehlo() #initialising the server
server.starttls() #starting a secure connection called tls
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('\n Email Sent ...')

server.quit()
