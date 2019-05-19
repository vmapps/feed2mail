#!/usr/bin/env python

import argparse
import datetime
import json
import os
import pprint
import sys
import utils

with open( os.path.dirname(__file__)+'/config.json','r') as fh:
  config = json.load(fh)
fh.close()

parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', help='force debug mode', default=False, action='store_true')
parser.add_argument('-o', help='output file name', metavar='<filename>', action='store')
args = parser.parse_args()

if args.debug:
  config['debug'] = True
if args.o:
  config['output.file'] = args.o

if config.get('feeds.sources'):
  feed = utils.feed()
  feed.header()

  for idx,url in enumerate( config['feeds.sources'] ):
    sys.stderr.write( '[%0d/%0d]\tRetrieving %s ...\n' %(idx+1,len(config['feeds.sources']),url) )

    feed.get(url)
    feed.parse( config['feeds.period'] )

  feed.footer( config['feeds.sources'] )

  if config.get('output.file'):
    with open( config['output.file'],'w') as fh:
      fh.write( feed.html.encode('utf8') )
    fh.close()

else:
  sys.stderr.write( '[ERROR] no feed sources' )
  sys.exit(0)

if config.get('email.recipient'):
  dt = datetime.datetime.today()

  e = utils.email( config['smtp.host'], config['smtp.port'], config['smtp.ssl'], config['smtp.user'], config['smtp.pass'] )
  e.header( config['email.sender'], config['email.recipient'], '%s %s' % (config['email.title'],dt.strftime('%d/%m/%Y')) )
  e.body( feed.html.encode('utf8') )
  e.attachment( feed.html.encode('utf8'), 'newsletter-%s.html' % dt.strftime('%Y%m%d') )
  e.send()
