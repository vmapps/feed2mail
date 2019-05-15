# feed2mail
News feeds sent to your mailbox

## Purpose 
Purpose of this very simple tool is to :
- help retrieving news from diffrent ffeds (RSS, ATOM, XML, ...)
- compile one of those that match a pediod (e.g. 'yesterday')
- send articles as HTML document to some email recipients

## Requirements
Following python modules are required :
- [email](https://docs.python.org/3/library/email.html)
- [feedparser](https://pythonhosted.org/feedparser/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)

Modules could be installed using following commands:
```
$ pip install -r requirements.txt
```
## Configuration
Settings have to be changed using file **config-template.py** :
```
# enable/disable debug mode
DEBUG = False

# SMTP settings
SMTP_HOST = '<your_ISP_SNMTP_server>'
SMTP_PORT = 25
SMTP_SSL  = False
SMTP_USER = '<your_user>'
SMTP_PASS = '<your_password>'

# feeds URL as sources
SOURCES = [
    'http://feeds.arstechnica.com/arstechnica/security/',
    'https://nakedsecurity.sophos.com/feed/',
    'https://www.theregister.co.uk/security/headlines.atom'
]

# period of posts to take into consideration
# values: all, today, yesterday
PERIOD = 'yesterday'

#
# email sender and recipients to be used
SENDER = '<sender_email_address>'
RECIPIENTS = '<recipients_email_address>'

#
# email title to be used
TITLE = '<pretty_nice_title>'
```
Then rename template file as config.py
```
mv config-template.py config.py
```
## Outputs
```
$ newsletter.py
```
Once executed, the program will generate :
- HTML code in email body
- HTML file attached to the email
- HTML code to stderr if DEBUG node is enable
