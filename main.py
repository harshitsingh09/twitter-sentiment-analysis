import csv
import re
from textblob import TextBlob
import matplotlib.pyplot as plt

class SentimentAnalysis:
    def __init__(self):
        self.tweets = []

    def DownloadData(self, filename, limit=None):
        # Open CSV file for reading
        with open(filename, 'r', encoding='utf-8') as csvFile:
            csvReader = csv.DictReader(csvFile)
            
            # Counter to keep track of the number of entries processed
            count = 0
            
            # Loop through each tweet in the CSV
            for row in csvReader:
                # Check if a limit is set and if we have reached it
                if limit is not None and count >= limit:
                    break
                
                # Access tweet text from the 'content' column
                tweetText = row['content']

                # Clean the tweet text
                cleaned_tweet = self.cleanTweet(tweetText)

                # Perform sentiment analysis
                analysis = TextBlob(cleaned_tweet)
                sentiment_score = analysis.sentiment.polarity

                # Classify sentiment
                sentiment = self.classifySentiment(sentiment_score)

                # Store sentiment for further processing
                self.tweets.append(sentiment)

                # Increment the counter
                count += 1

    def cleanTweet(self, tweet):
        # Remove links, special characters, etc., from the tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def classifySentiment(self, score):
        # Classify sentiment based on the sentiment score
        if score >= 0.875:
            return "Strongly Positive"
        elif 0.375 <= score < 0.875:
            return "Positive"
        elif 0.125 <= score < 0.375:
            return "Weakly Positive"
        elif -0.125 <= score < 0.125:
            return "Neutral"
        elif -0.625 <= score < -0.125:
            return "Negative"
        elif -0.875 <= score < -0.625:
            return "Strongly Negative"
        else:
            return "Weakly Negative"


    def plotSentimentGraph(self):
        # Count the number of each sentiment category
        sentiment_counts = {'Positive': 0, 'Weakly Positive': 0, 'Strongly Positive': 0, 'Neutral': 0, 
                            'Negative': 0, 'Weakly Negative': 0, 'Strongly Negative': 0}

        # Loop through each sentiment in the tweets
        for sentiment in self.tweets:
            # Increment sentiment counts
            sentiment_counts[sentiment] += 1

        # Remove categories with zero counts
        sentiment_counts = {key: value for key, value in sentiment_counts.items() if value != 0}

        # Define colors for each sentiment category
        colors = ['#00ff00', '#99ff99', '#11ff99', '#ffcc99', '#ff0000', '#ffb3e6', '#ff6666']

        # Plot a pie chart only if there are non-zero counts
        if sentiment_counts:
            plt.figure(figsize=(8, 8))
            plt.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%', startangle=0, colors=colors)

            # Add a circle at the center to make it look like a donut chart
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            plt.gca().add_artist(centre_circle)

            plt.title("Sentiment Analysis")
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.show()
        else:
            print("No non-zero sentiment counts to plot.")



if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData("tweets.csv", limit=500)
    sa.plotSentimentGraph()
