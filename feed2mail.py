#!/usr/bin/env python

#
# imports required modules
import argparse
import datetime
import jinja2
import json
import os
import pprint
import sys
import time
import utils

#
# set command-line arguments and parsing options
parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', help='force debug mode (not used yet)', default=False, action='store_true')
parser.add_argument('-c', help='config file name (defaut: config.json)', metavar='<filename>', action='store')
parser.add_argument('-t', help='template file name (defaut: templates/feed2mail.html)', metavar='<filename>', action='store')
parser.add_argument('-o', help='output file name', metavar='<filename>', action='store')
args = parser.parse_args()

#
# checks arguments and options
file_cfg = args.c if args.c else os.path.dirname(__file__) + '/config.json'
file_out = args.o if args.o else None
file_tpl = args.t if args.t else os.path.dirname(__file__) + '/templates/feed2mail.html'

#
# open configuration file
try:
  with open( file_cfg,'r') as fh:
    config = json.load(fh)
  fh.close()
except Exception as e:
  sys.stderr.write( '[ERROR] reading configuration file %s\n' % file_cfg )
  sys.stderr.write( '[ERROR] %s\n' % str(e) )
  sys.exit(1)

#
# overwrite debug config
if args.debug:
 config['debug'] = True

#
# open template file
try:
  with open(file_tpl,'r') as fh:
    tpl = jinja2.Template(fh.read())
  fh.close()
except Exception as e:
  sys.stderr.write( '[ERROR] reading template file %s\n' % file_tpl )
  sys.stderr.write( '[ERROR] %s\n' % str(e) )
  sys.exit(1)

#
# walk through each feed sources
if config.get('feeds.sources'):

  start = time.time()
  data = []

  # for each feed
  for idx,url in enumerate( config['feeds.sources'] ):
    sys.stderr.write( '[%0d/%0d]\tRetrieving %s ...\n' %(idx+1,len(config['feeds.sources']),url) )

    # set a feed object
    f = utils.feed()
    # get feed content from URL and parse according to period
    f.get(url)
    f.parse( config['feeds.period'] )

    if len(f.posts):
      data.append( {'title':f.feed.title, 'posts':f.posts} )

  # render template with data
  html = tpl.render(
    data = data,
    time = '%.2f' % (time.time()-start),
    sources = config['feeds.sources']
    )

#
# exit if no feed sources
else:
  sys.stderr.write( '[ERROR] no feed sources' )
  sys.exit(0)

#
# if output option set then write HTML content to file
if file_out is not None:
  try:
    with open( file_out,'w') as fh:
      fh.write( html.encode('utf8') )
    fh.close()
  except Exception as e:
    sys.stderr.write( '[ERROR] opening output file %s\n' % file_out )
    sys.stderr.write( '[ERROR] %s\n' % str(e) )
    sys.exit(1)

#
# if email recipient set then prepare to send email
if config.get('email.recipient'):
  dt = datetime.datetime.today()

  # set email object and its header
  e = utils.email( config['smtp.host'], config['smtp.port'], config['smtp.ssl'], config['smtp.user'], config['smtp.pass'] )
  e.header( config['email.sender'], config['email.recipient'], '%s %s' % (config['email.title'],dt.strftime('%d/%m/%Y')) )

  # fit with HTML in body and attachment
  e.body( html.encode('utf8') )
  e.attachment( html.encode('utf8'), 'newsletter-%s.html' % dt.strftime('%Y%m%d') )

  # finally send email
  e.send()

#
# end