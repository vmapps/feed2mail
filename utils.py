#!/usr/bin/env python

# --------------------------------------------------
# Import required packages
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

# --------------------------------------------------
# Class email
# --------------------------------------------------
class email:

    def __init__(self,host,port,ssl,user,password):
        # Private members
        self.__host = host
        self.__port = port
        self.__ssl  = ssl
        self.__user = user
        self.__pass = password
        self.__msg = MIMEMultipart('alternative')

    def header(self,sender,recipient,subject):
        # Create message object instance
        # Declare message elements
        self.__msg['From']    = sender
        self.__msg['To']      = recipient
        self.__msg['Subject'] = subject

    def body(self,body):
        # According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
        #msg.attach( MIMEText(text,'plain') )
        self.__msg.attach( MIMEText(body,'html') )

    def attachment(self,content,filename):
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(content)
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', 'attachment; filename= "%s"' % filename) 
        # attach the instance 'p' to instance 'msg' 
        self.__msg.attach(p)

    def send(self):
        # Create the server connection
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

        try:
            if self.__user and self.__pass: 
               server.login(self.__user, self.__pass)
            server.sendmail(self.__msg['From'], self.__msg['To'], self.__msg.as_string())
            server.quit()
        except:
            sys.stderr.write( '[ERROR] unable to send email from %s\n' % self.__msg['From'] )
            sys.exit(1)

        sys.stderr.write( '[INFO] message successfully sent to %s\n' % self.__msg['To'] )

# --------------------------------------------------
# Class feed
# --------------------------------------------------
class feed:

    def __init__(self):
        self.html = ''
        self.time = time.time()

    def get(self,url):
        self.url = url
        self.data = feedparser.parse(self.url)
        # Data Feed and Data Entries
        self.feed = self.data.feed
        self.entries = self.data.entries
        #print self.data.data

    def header(self):
        self.html = self.html + '''
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html charset=UTF-8" />
                <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed" rel="stylesheet" />
            </head>
            <body style="margin:0; padding:0;">
        '''

    def footer(self,sources):
        self.time = time.time() - self.time

        self.html = self.html + '''   
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="650" style="color:#c0c3c6; border-collapse:collapse;">
                <tr>
                    <td colspan=2 bgcolor="#ffffff" style="padding:0; word-break:break-all;">
                    <hr style="border:dotted 1px #999999; border-width:3px 0 0 0;" />
                    <span style="font-family:Roboto Condensed; font-size:1.1em; text-transform:uppercase; color=#c0c3c6;">Sources checked (in %.2f secs)</span>
                    </td>
                </tr>
        ''' % (self.time)

        buffer = ''
        for s in sources:
            buffer = buffer + s + '<br/>\n'

        self.html = self.html + '''   
                <tr>
                    <td bgcolor="#ffffff" width=50>
                    </td>
                    <td bgcolor="#ffffff" style="padding:0; word-break:break-all;"></p>
                        <p style="font-family:Roboto Condensed; font-size:0.9em;">%s</p>
                    </td>
                </tr>
                </table>
        ''' % (buffer)

        self.html = self.html + '''   
            </body>
            </html>
        '''

    def parse(self,period=''):
        # Feed Updated Parsed Time and Date
        # fupt = self.feed.updated_parsed
        # fupd = '%04d-%02d-%02d' % (fupt.tm_year, fupt.tm_mon, fupt.tm_mday)
        # Current Date and Previous Day
        # curd = datetime.datetime.today().strftime('%Y-%m-%d')
        # pred = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        _html = ''

        # with open("feed.png", "rb") as fh:
        #     onerror='this.onerror=null;this.src=\'data:image/png;base64,%s\';' % base64.b64encode(fh.read())

        if self.feed.get('image'):
            self.feed.icon = '<img src="%s" width=48 title="%s"/>' % (self.feed.image.href, self.feed.title)
        else:
            # self.feed.icon = 'https://upload.wikimedia.org/wikipedia/commons/e/e8/Generic_Feed-icon.png'    
            onerror='this.onerror=null;this.src=\'https://upload.wikimedia.org/wikipedia/commons/e/e8/Generic_Feed-icon.png\';'
            self.feed.icon = '<img src="%s" width=48 title="%s" onerror="%s" />' % (urlparse.urljoin(self.url,'/')+'favicon.ico', self.feed.title, onerror)

        if period=='today':         check = datetime.datetime.today().strftime('%Y-%m-%d')
        elif period=='yesterday':   check = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:                       check = True

        found = False

        _html = _html + '''
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="650" style="border-collapse:collapse;">
        <tr>
            <td colspan=2 bgcolor="#ffffff" style="padding:0; word-break:break-all;">
                <!-- <hr style="height:10px; border:0; box-shadow:0 10px 10px -10px #8c8b8b inset;" /> -->
                <hr style="border:dotted 1px #999999; border-width:3px 0 0 0;"/>
                <span style="font-family:Roboto Condensed; font-size:1.1em; text-transform:uppercase;">%s</span>
            </td>
        </tr>
        ''' % (self.feed.title)

        for post in self.entries:
            # Entry Updated Parsed Time and Date
            eupt = post.updated_parsed
            eupd = '%04d-%02d-%02d' % (eupt.tm_year, eupt.tm_mon, eupt.tm_mday)

            if check==True or eupd==check:
                _html = _html + self.format(post)
                found = True

        if not found:
            _html = '' 
        else:
            _html = _html + '\n</table>\n'

        self.html = self.html + _html

    def format(self,post):
        TAG_RE = re.compile(r'<[^>]+>')

        return '''
        <tr>
            <td bgcolor="#ffffff" width=50>
            </td>
            <td bgcolor="#ffffff" style="padding:0; word-break:break-all;">
                <p style="font-family:Roboto Condensed; text-align:justify;">
                <span style="font-size:1.0em; text-transform:uppercase;"><a href="%s" style="color:#000000; text-decoration:none;"><b>%s</b></a></span><br/>
                <span style="font-size:0.8em;"><i>%s</i></span><br/>
                <span style="font-size:0.9em;">%s</span>
                </p>
            </td>
        </tr>
        ''' % (post.link, post.title, post.updated, TAG_RE.sub('',post.summary) )






# --------------------------------------------------
