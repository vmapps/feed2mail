# enable/disable debug mode
DEBUG = False

# SMTP settings
SMTP_HOST = '<your_ISP_SNMTP_server>'
SMTP_PORT = 25
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

# email sender and recipients to be used
SENDER = '<your_email_address>'
RECIPIENTS = '<your_email_address>'

# email title to be used
TITLE = '<pretty_nice_title>'
