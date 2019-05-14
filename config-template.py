#!/usr/bin/env python

#
# DEBUG - enable/disable debug mode
DEBUG = False

#
# SMTP Settings
SMTP_HOST = '<your_ISP_SNMTP_server>'
SMTP_PORT = 25
SMTP_USER = '<your_user>'
SMTP_PASS = '<your_password>'

#
# SOURCES for the feeds
SOURCES = [
    'http://feeds.arstechnica.com/arstechnica/security/',
    'https://nakedsecurity.sophos.com/feed/',
    'https://www.theregister.co.uk/security/headlines.atom'
]

#
# PERIOD - period of posts to take into consideration
# values: all, today, yesterday
PERIOD = 'yesterday'

#
# FROM - email header used for email
SENDER = '<your_email_address>'
RECIPIENTS = '<your_email_address>'

#
# TITLE - email header used for email
TITLE = '<pretty_nice_title>'