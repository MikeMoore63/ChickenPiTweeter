#!/usr/bin/env python
import sys,select
import urllib, cStringIO
from StringIO import StringIO
from PIL import Image, ImageFilter
from twython import Twython
#import getch
import sys, tty, termios
import enchant

# Using UK english dictionary
dict = enchant.Dict('en_GB')


CONSUMER_KEY = '******your consumer key******'
CONSUMER_SECRET = '********* your consumer secret ************'
ACCESS_KEY = '***** your access key ********'
ACCESS_SECRET = '*************** your access secret *************'
URL = '************** yor web cam url ***********************'

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

tweetthis = ''
thechar=''
sys.stdout.write( 'Tweet: ')

while True:
       
	# read one character from keyboard
	fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		thechar = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	

	tweetthis=tweetthis + thechar
	sys.stdout.write( thechar)

        # if we have enough text tweet
	if len(tweetthis) >=40:

		sys.stdout.write('\n')

		# get webcam image
		file = cStringIO.StringIO(urllib.urlopen(URL).read())

		# upload image to twitter
		response = api.upload_media(media=file)

		# tweet
		api.update_status( media_ids=[response['media_id']],status=tweetthis+ ' #chickentweet')

		# check for any english words
		words = tweetthis.split()
		for word in words:
			if dict.check(word):
				print "Engish word Bingo:"+word

				# they did it
				if len(word) >= 5:
					api.update_status(status='Chicken first five letter word is:'+word+' well done to the girls')
					exit()
		tweetthis=''
		sys.stdout.write( 'Tweet: ')

