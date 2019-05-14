#!/usr/bin/env python

import config
import datetime
import sys
import utils

if config.SOURCES:
  feed = utils.feed()
  feed.header()

  for idx,url in enumerate(config.SOURCES):
    sys.stderr.write( '[%0d/%0d]\tRetrieving %s ...\n' %(idx+1,len(config.SOURCES),url) )

    feed.get(url)
    feed.parse( config.PERIOD )

  feed.footer( config.SOURCES )

  if config.DEBUG:
    print feed.html.encode('utf8')
    # exit()
else:
  sys.stderr.write( '[ERROR] no feed sources' )
  sys.exit(0)

sys.exit(0)

if config.RECIPIENTS:
  dt1 = datetime.datetime.today().strftime('%d/%m/%Y')
  dt2 = datetime.datetime.today().strftime('%Y%m%d')

  e = utils.email( config.SMTP_HOST, config.SMTP_PORT, config.SMTP_USER, config.SMTP_PASS )
  e.header( config.SENDER, config.RECIPIENTS, '%s %s' % (config.TITLE.dt1) )
  e.body( feed.html.encode('utf8') )
  e.attachment( feed.html.encode('utf8'), 'newsletter-%s.html' % dt2 )
  e.send()
