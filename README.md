# feed2mail
News feeds sent to your mailbox

## Purpose 
Purpose of this very simple tool is to :
- help retrieving news from different feeds (RSS, ATOM, XML, ...)
- compile one of those that match a pediod (e.g. 'yesterday')
- send articles as HTML document to some email recipients

## Requirements
Following python modules are required :
- [email](https://docs.python.org/3/library/email.html)
- [feedparser](https://pythonhosted.org/feedparser/)
- [jinja2](http://jinja.pocoo.org/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)

Modules could be installed using following commands:
```
$ pip install -r requirements.txt
```
## Configuration
Settings have to be defined using JSON config file :
```
# enable/disable debug mode
"debug": [true|false]

# SMTP settings
"smtp.host": "<your_ISP_SNMTP_server>"
"smtp.port": 465
"smtp.ssl": [true|false]
"smtp.user": "<your_user>"
"smtp.pass": "<your_password>"

# feeds sources and period of posts to take into consideration
"feeds.sources": [
    'http://feeds.arstechnica.com/arstechnica/security/',
    'https://nakedsecurity.sophos.com/feed/',
    'https://www.theregister.co.uk/security/headlines.atom'
]
"feeds.period": "[all|yesterday|today]"

# email settings
"email.sender": "<sender_email_address>"
"email.recipient": "<recipient_email_address>"
"email.title": "<pretty_nice_title>"
```
Do not forget to rename template file as `config.json`
```
mv config-template.json config.json
```
## Usage
```
usage: feed2mail.py [-h] [-a] [-d] [-c <filename>] [-o <filename>] [-t <filename>]

optional arguments:
  -h, --help            show this help message and exit
  -a, --attachment      add HTML content as attachment
  -d, --debug           force debug mode (not used yet)
  -c <filename>, --config <filename>
                        config file name (defaut: config.json)
  -t <filename>, --template <filename>
                        template file name (defaut: templates/feed2mail.html)
  -o <filename>, --output <filename>
                        output file name
```
## Outputs
```
$ feed2mail.py
[INFO] message successfully sent to *****@*****.***

$ feed2mail.py -c feed2mail.json -t templates/feed2mail-outlook.html -o /tmp/output.html
[INFO] message successfully sent to *****@*****.***
```
Once executed, the program will generate :
- HTML code in email body
- HTML file attached to the email
- HTML code to <filename> if output option is used
- success/error messages to stderr
    
## Sample
![newsletter](samples/feed2mail.png)

