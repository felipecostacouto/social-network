import pickle
import preprocessor as p


class PrestigeHandler:

    def __init__(self, tweets):
        self.detector = pickle.load(open('fake-news_detector.pickle', 'rb'))
        self.vectorizer = pickle.load(open('count-vectorizer.pickle', 'rb'))
        self.tweets = tweets

    def pre_process_tweet(self, tweet):
        p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG)
        return p.clean(tweet.text)

    def get_user_prestige(self):

        count = 0
        for tweet in self.tweets:
            tweet = self.pre_process_tweet(tweet)

            transform = self.vectorizer.transform([tweet]).toarray()
            predict = self.detector.predict(transform)

            if predict == 'fake':
                count = count + 1

        return count / len(self.tweets)
