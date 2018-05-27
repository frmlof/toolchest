#!env python

# This program is going to collect 200 tweets of a specified user
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

def access_tweeter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    t_api = tweepy.API(auth)
    return t_api

def collect_tweets(screen_name):
    api = access_tweeter()
    client = boto3.client('firehose')
    # make a placeholder, empty list
    alltweets = []
    # ... and initial request ...
    new_tweets = api.user_timeline(screen_name = screen_name, count = 200)
    # ... and add everything to list
    alltweets.extend(new_tweets)
    # now save id of oldest tweet
    oldest_tweet = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest_tweet)
        new_tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest_tweet)
        alltweets.extend(new_tweets)
        oldest_tweet = alltweets[-1].id - 1

    for tweet in alltweets:
        tweets_out = [tweed.id_str, tweet.created_at, tweet.text.encode("utf-8")]
        response = client.put_record(
            DeliveryStreamName = firehose,
            Record = {
                'Data': tweets_out
            }
        )

    """
    tweets_out = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet['entries']['hashtags']] for tweet in alltweets]
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(tweets_out)

    client = boto3.client('firehose')
    response = client.put_record(
        DeliveryStreamName = firehose,
        Record = {
            'Data':
        }
    )
    """

def write_to_S3(firehose):
    # Additionally you may specify region if you need to.
    # otherwise program is going to use default region defined
    # in AWS CLI.
    client = boto3.client('firehose')
    response = client.put_record(
        DeliveryStreamName=firehose,
        Record = {
            'Data':
        }
    )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Some logic here
        print("Command has parameters")
        collect_tweets(sys.argv[1])
    else:
        sys.exit("No parameters present.\nUsage: gettweets <screen name>.")
