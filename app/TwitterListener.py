from tweepy.streaming import StreamListener
import json


class TwitterListener(StreamListener):

    def __init__(self):
        super(TwitterListener, self).__init__()
        self.__max_tweets = 5
        self.__tweets_collected = 0
        self.__all_collected_tweets_json = {}

    # def get_max_tweets(self):
    #     return self.__max_tweets

    # Set the maximum number of tweets to be collected from Twitter
    def set_max_tweets(self, maximum):
        self.__max_tweets = int(maximum)

    # When a tweet comes along the Twitter stream that matches our search criteria, grab it, print it to the user,
    # and store it for future reference, in case the user wants to view the tweet on the web
    def on_data(self, data):
        # Make sure we aren't collecting more tweets than what the user requested
        if self.__tweets_collected < self.__max_tweets:
            tweet = json.loads(data)
            # Print the tweet text to the screen
            print("{0})".format(str(self.__tweets_collected + 1)))
            print("{0}".format(tweet['text']))
            print("User:      {0} (@{1})".format(tweet['user']['name'],tweet['user']['screen_name']))
            print("Retweeted: {0} times".format(tweet['retweet_count']))
            print("Favorited: {0} times".format(tweet['favorite_count']))
            print("Created:   {0}".format(tweet['created_at']))
            print("--------------------------------------------------------------------------------------------------")
            # Store the tweet object in a dict, and increment the tweets_collected counter
            self.__all_collected_tweets_json['Tweet' + str(self.__tweets_collected+1)] = tweet
            self.__tweets_collected += 1
            return True
        else:
            return False

    # After the tweets collected reaches the amount the user requested, store the entire dict in an external
    # JSON file, found in root/data/.
    def store_live_tweets(self):
        try:
            # Open JSON file, delete file contents, write stored Twitter objects to the file, close file
            with open('app/data/election.json', 'w') as f:
                f.write(json.dumps(self.__all_collected_tweets_json))
                f.close()
                return True
        except BaseException as e:
            print("Error in TwitterListener's store_recent_tweets: {0}".format(str(e)))
        return True

    def on_error(self, status):
        print(status)
        return True

    def on_limit(self, status):
        print('Limit threshold exceeded. ', status)

    def on_timeout(self):
        print('Stream disconnected; continuing...')
