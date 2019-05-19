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
        self.__msg.attach( MIMEText(body,'html') )

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
        #print self.data.data

    # setup HTML content header
    def header(self):
        self.html = self.html + '''
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html charset=UTF-8" />
            </head>
            <body style="margin:0; padding:0;">
        '''

    # setup HTML content footer
    def footer(self,sources):
        # set execution time as current time - start time
        self.time = time.time() - self.time
        # set HTML block
        self.html = self.html + '''   
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="600px" style="color:#c0c3c6; border-collapse:collapse;">
                <tr>
                    <td colspan=2 bgcolor="#ffffff" style="padding:0; word-break:break-all;">
                    <hr style="border:dotted 1px #999999; border-width:3px 0 0 0;" />
                    <span style="font-family:Tahoma, Geneva, sans-serif; font-size:1.1em; text-transform:uppercase; color=#c0c3c6;">Sources checked (in %.2f secs)</span>
                    </td>
                </tr>
        ''' % (self.time)
        # add feed sources as list in HTML block
        buffer = ''
        for s in sources:
            buffer = buffer + s + '<br/>\n'
        # append to HTML block
        self.html = self.html + '''   
                <tr>
                    <td bgcolor="#ffffff" width="50px">
                    </td>
                    <td bgcolor="#ffffff" style="padding:0; word-break:break-all;"></p>
                        <p style="font-family:Tahoma, Geneva, sans-serif; font-size:0.9em;">%s</p>
                    </td>
                </tr>
                </table>
        ''' % (buffer)
        # close HTML content
        self.html = self.html + '''   
            </body>
            </html>
        '''

    # parse feed content according to period asked
    def parse(self,period=''):
        _html = ''
        found = False
        # [NOT USED] if feed contains image
        if self.feed.get('image'):
            self.feed.icon = '<img src="%s" width="48" title="%s"/>' % (self.feed.image.href, self.feed.title)
        else:
            onerror='this.onerror=null;this.src=\'https://upload.wikimedia.org/wikipedia/commons/e/e8/Generic_Feed-icon.png\';'
            self.feed.icon = '<img src="%s" width="48" title="%s" onerror="%s" />' % (urlparse.urljoin(self.url,'/')+'favicon.ico', self.feed.title, onerror)
        # check for period to check and to keep for content
        if period=='today':
            check = datetime.datetime.today().strftime('%Y-%m-%d')
        elif period=='yesterday':
            check = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            check = True
        # setup HTML content with feed title
        _html = _html + '''
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600px" style="border-collapse:collapse;">
        <tr>
            <td colspan=2 bgcolor="#ffffff" style="padding:0; word-break:break-all;">
                <hr style="border:dotted 1px #999999; border-width:3px 0 0 0;"/>
                <span style="font-family:Tahoma, Geneva, sans-serif; font-size:1.1em; text-transform:uppercase;">%s</span>
            </td>
        </tr>
        ''' % (self.feed.title)
        # for each post in feed
        for post in self.entries:
            eupt = post.updated_parsed
            eupd = '%04d-%02d-%02d' % (eupt.tm_year, eupt.tm_mon, eupt.tm_mday)
            # keep content only if it matches petiod
            if check==True or eupd==check:
                _html = _html + self.format(post)
                found = True
        # if nothing found
        if not found:
            _html = '' 
        else:
            _html = _html + '\n</table>\n'
        # append HTML content to object
        self.html = self.html + _html

    # format feed post as HTML
    def format(self,post):
        # regexp to remove HTML tags from feed fields 
        TAG_RE = re.compile(r'<[^>]+>')
        # format HTML content
        return '''
        <tr>
            <td bgcolor="#ffffff" width="50px">
            </td>
            <td bgcolor="#ffffff" style="padding:0; word-break:break-all;">
                <p style="font-family:Tahoma, Geneva, sans-serif; text-align:justify;">
                <span style="font-size:1.0em; text-transform:uppercase;"><a href="%s" style="color:#000000; text-decoration:none;"><b>%s</b></a></span><br/>
                <span style="font-size:0.8em;"><i>%s</i></span><br/>
                <span style="font-size:0.9em;">%s</span>
                </p>
            </td>
        </tr>
        ''' % (post.link, post.title, post.updated, TAG_RE.sub('',post.summary) )

#
# end