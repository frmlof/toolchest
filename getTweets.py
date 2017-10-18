#!/env python

import sys
import boto3
import tweepy

# SET CREDENTIALS HERE
# VVV VVV VVV

ACCESS_KEY =
ACCESS_SECRET =
CONSUMER_KEY =
CONSUMER_SECRET =


def listTweets(screenName):
    # Start with authentication with service.
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    tapi = tweepy.API(auth)

    # Initialize placeholder
    tweets = []

    # Get 200 (maximum allowed) tweets from user timeline
    ntweets = tapi.user_timeline(screen_name = screenName, count = 200)

    # Save tweets
    tweets.extend(ntweets)

    oldest = tweets[-1].id - 1

    while len(ntweets) > 0:
        ntweets = tapi.user_timeline(screen_name = screenName; count = 200, max_id = oldest)
        tweets.extend(ntweets)
        oldest = tweets[-1] - 1

    tdata = [[tweet.id_str, tweet.lang, tweet.hashtag] for tweet in tweets]

    with open("%s_tweets.csv" % screenName, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'hashtag'])
        writer.writerow(tdata)


# execution starts here
if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Execute application here
    else:
        sys.exit('Usage: python getTweets.py <tweeter screen name> <AWS Kinesis Firehose name>')
