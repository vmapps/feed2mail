#!/usr/bin/env python

#
# imports required modules
import argparse
import datetime
import json
import os
import pprint
import sys
import utils

#
# set command-line arguments and parsing options
parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', help='force debug mode (not used yet)', default=False, action='store_true')
parser.add_argument('-c', help='config file name', metavar='<filename>', action='store')
parser.add_argument('-o', help='output file name', metavar='<filename>', action='store')
args = parser.parse_args()

#
# checks arguments and options
if args.debug:
  config['debug'] = True

if args.c:
  file_config = args.c
else:
  file_config = os.path.dirname(__file__) + '/config.json'

if args.o:
  file_output = args.o
else:
  file_output = None

#
# open configuration file
with open( file_config,'r') as fh:
  config = json.load(fh)
fh.close()

#
# walk through each feed sources
if config.get('feeds.sources'):

  # set a feed object and its header
  feed = utils.feed()
  feed.header()

  # for each feed
  for idx,url in enumerate( config['feeds.sources'] ):
    sys.stderr.write( '[%0d/%0d]\tRetrieving %s ...\n' %(idx+1,len(config['feeds.sources']),url) )

    # get feed content from URL and parse according to period
    feed.get(url)
    feed.parse( config['feeds.period'] )

  # set footer content
  feed.footer( config['feeds.sources'] )

#
# exit if no feed sources
else:
  sys.stderr.write( '[ERROR] no feed sources' )
  sys.exit(0)

#
# if output option set then write HTML content to file
if file_output is not None:
  with open( file_output,'w') as fh:
    fh.write( feed.html.encode('utf8') )
  fh.close()

#
# if email recipient set then prepare to send email
if config.get('email.recipient'):
  dt = datetime.datetime.today()

  # set email object and its header
  e = utils.email( config['smtp.host'], config['smtp.port'], config['smtp.ssl'], config['smtp.user'], config['smtp.pass'] )
  e.header( config['email.sender'], config['email.recipient'], '%s %s' % (config['email.title'],dt.strftime('%d/%m/%Y')) )

  # fit with HTML in body and attachment
  e.body( feed.html.encode('utf8') )
  e.attachment( feed.html.encode('utf8'), 'newsletter-%s.html' % dt.strftime('%Y%m%d') )

  # finally send email
  e.send()

#
# end