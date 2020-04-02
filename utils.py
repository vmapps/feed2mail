#!/usr/bin/env python

# import required packages
# --------------------------------------------------
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pprint import pprint

import base64
import datetime
import feedparser
import os
import re
import smtplib
import sys
import time
import urlparse

# class email
# --------------------------------------------------
class email:

    # initialize class object
    def __init__(self,host,port,ssl,user,password):
        self.__host = host
        self.__port = port
        self.__ssl  = ssl
        self.__user = user
        self.__pass = password
        self.__msg = MIMEMultipart('alternative')

    # setup email header
    def header(self,sender,recipient,subject):
        self.__msg['From']    = sender
        self.__msg['To']      = recipient
        self.__msg['Subject'] = subject

    # setup email body
    def body(self,body):
        #msg.attach( MIMEText(text,'plain') )
        self.__msg.attach( MIMEText(body,'html','utf-8') )

    # setup email attachment 
    def attachment(self,content,filename):
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(content)
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', 'attachment; filename= "%s"' % filename) 
        # attach the instance 'p' to instance 'msg' 
        self.__msg.attach(p)

    # connect to SMTP server and send email
    def send(self):
        # according to SMTP settings use SSL or not to connect
        try:
            if self.__ssl:
                server = smtplib.SMTP_SSL(host=self.__host ,port=self.__port )
            else:
                server = smtplib.SMTP(host=self.__host ,port=self.__port )
        except socket.error as e:
            sys.stderr.write( '[ERROR] when connecting to %s:%d\n' % (self.__host,self.__port) )
            sys.exit(1)
        except:
            sys.stderr.write( '[ERROR] when send email using %s:%d\n' % (self.__host,self.__port) )
        # log into SMTP server, send and quit
        try:
            if self.__user and self.__pass: 
               server.login(self.__user, self.__pass)
            server.sendmail(self.__msg['From'], self.__msg['To'], self.__msg.as_string())
            server.quit()
        except:
            sys.stderr.write( '[ERROR] unable to send email from %s\n' % self.__msg['From'] )
            sys.exit(1)
        # all done
        sys.stderr.write( '[INFO] message successfully sent to %s\n' % self.__msg['To'] )

# class feed
# --------------------------------------------------
class feed:

    # initialize class object
    def __init__(self):
        self.html = ''
        self.time = time.time()

    # download content from URL
    def get(self,url):
        self.url = url
        self.data = feedparser.parse(self.url)
        self.feed = self.data.feed
        self.entries = self.data.entries
        self.posts = []
        # pprint( self.data )

    # parse feed content according to period asked
    def parse(self,period=''):
        # check for period to check and to keep for content
        if period=='today':
            check = datetime.datetime.today().strftime('%Y-%m-%d')
        elif period=='yesterday':
            check = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            check = True
        # for each post in feed
        for (idx,post) in enumerate(self.entries):
            eupt = post.updated_parsed
            eupd = '%04d-%02d-%02d' % (eupt.tm_year, eupt.tm_mon, eupt.tm_mday)
            # keep content only if it matches petiod
            if (check==True or eupd==check):
                self.posts.append(post) 
                sys.stderr.write('\t- %s\n' % (post.title).encode('utf-8') )

#
# end
