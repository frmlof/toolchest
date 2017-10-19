#!env python

# This program is going to collect 200 twitts of a specified user
# and publish it AWS S3 using Kinesis Firehose

import csv
import sys
import boto3
import tweepy

# Define access keys
ACCESS_KEY = ""
ACCESS_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

def access_twitter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    t_api = tweepy.API(auth)
    return t_api

def collect_twitts(screen_name):
    api = access_twitter()
    # make a placeholder, empty list
    alltwitts = []
    # ... and initial request ...
    new_twitts = api.user_timeline(screen_name = screen_name, count = 200)
    # ... and add everything to list
    alltwitts.extend(new_twitts)
    # now save id of oldest twitt
    oldest_twitt = alltwitts[-1].id - 1

    while len(new_twitts) > 0:
        print("getting twitts before %s" % oldest_twitt)
        new_twitts = api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest_twitt)
        alltwitts.extend(new_twitts)
        oldest_twitt = alltwitts[-1].id - 1

    twitts_out = [[twitt.id_str, twitt.created_at, twitt.text.encode("utf-8")] for twitt in alltwitts]

    with open('%s_twitts.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(twitts_out)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Some logic here
        print("Command has parameters")
        collect_twitts(sys.argv[1])
    else:
        sys.exit("No parameters present.\nUsage: getTwitts <screen name>.")
