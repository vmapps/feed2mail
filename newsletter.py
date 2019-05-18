#!/usr/bin/env python

import datetime
import json
import os
import sys
import utils

with open( os.path.dirname(__file__)+'/config.json','r') as fh:
  cfg = json.load(fh)
fh.close()

if cfg.get('feeds.sources'):
  feed = utils.feed()
  feed.header()

  for idx,url in enumerate( cfg['feeds.sources'] ):
    sys.stderr.write( '[%0d/%0d]\tRetrieving %s ...\n' %(idx+1,len(cfg['feeds.sources']),url) )

    feed.get(url)
    feed.parse( cfg['feeds.period'] )

  feed.footer( cfg['feeds.sources'] )

  if cfg.get('debug'):
    print feed.html.encode('utf8')
    # exit()
else:
  sys.stderr.write( '[ERROR] no feed sources' )
  sys.exit(0)

if cfg.get('email.recipients'):
  dt1 = datetime.datetime.today().strftime('%d/%m/%Y')
  dt2 = datetime.datetime.today().strftime('%Y%m%d')

  e = utils.email( cfg['smtp.host'], cfg['smtp.port'], cfg['smtp.ssl'], cfg['smtp.user'], cfg['smtp.pass'] )
  e.header( cfg['email.sender'], cfg['email.recipient'], '%s %s' % (cfg['email.title'],dt1) )
  e.body( feed.html.encode('utf8') )
  e.attachment( feed.html.encode('utf8'), 'newsletter-%s.html' % dt2 )
  e.send()
