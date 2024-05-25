from nltk.tokenize import word_tokenize # pip install nltk
from nltk.corpus import stopwords # run: import nltk + nltk.download('stopwords') in a python terminal
from wordcloud import WordCloud # pip install wordcloud
from dotenv import load_dotenv # pip install python-dotenv
from collections import Counter
# import matplotlib.pyplot as plt
import praw # pip install praw
import re
import os


# Setting up authentification: (https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)
load_dotenv()
reddit = praw.Reddit(client_id = os.getenv('REDDIT_CLIENT_ID'),  
                     client_secret = os.getenv('REDDIT_CLIENT_SECRET'),  
                     user_agent = os.getenv('REDDIT_USER_AGENT'))


def get_subreddit(input_str):
    """
    Extracts the subreddit name from a URL or returns the input directly if it's already a plain name.
    """
    
    url_pattern = re.compile(r'(https?://)?(www\.)?reddit\.com/r/([^/]+)/?') # Regular expression to match subreddit URLs
    
    match = url_pattern.match(input_str) # Match the input string against the pattern above
    
    if match:
        # Extract subreddit name from the URL
        subreddit_name = match.group(3) # ([^/]+)/?
    else:
        subreddit_name = input_str # Use the input directly as the subreddit name

    subreddit = reddit.subreddit(subreddit_name) # Get subreddit object
    
    return subreddit


def fetch_posts_within_date_range(subreddit, start_date, end_date):
    """
    Fetches all posts from a subreddit within a specified datetime object date range.
    """
    
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    
    filtered_posts = []
    number_of_posts = 0
    for submission in subreddit.new(limit=None):  # Use limit=None to fetch all new posts
        if start_timestamp <= submission.created_utc <= end_timestamp:
            # post_date = datetime.datetime.fromtimestamp(submission.created_utc)
            filtered_posts.append(submission)
            number_of_posts+=1
        
    print(f"Number of posts: {number_of_posts}")
    
    return filtered_posts


def extract_comments_from_posts(posts):
    """
    Get all the comments from a list of post objects
    """
    # Iterate over the posts
    all_comments = []
    total_comments = 0
    for post in posts:
        post_comments = []
        post.comments.replace_more(limit=None) # handles posts with large number of comments
        for comment in post.comments.list():
            post_comments.append(comment.body)
            total_comments+=1
            
        all_comments.append(post_comments)
    
    print(f'Number of comments: {total_comments}')
    
    return all_comments


def merge_all_comments_into_text(all_comments):
    """
    Merges all comments from a list of list of comments into a single text string.
    """
    merged_text=""

    for post in all_comments:
        merged_text += " ".join(post)
    
    return merged_text


def remove_stopwords(text, lang):
    """
    Removes stopwords from a text in the given language
    """
    stop_words = set(stopwords.words(lang)) # 'english' // 'portuguese'
    words = word_tokenize(text, language=lang)
    
    non_stopwords = [word for word in words if word.lower() not in stop_words]
    
    filtered_text = " ".join(non_stopwords)
    
    return filtered_text


def get_words_frequency(text):
    """
    Create a word frequency dictionary from a given text and sorts it
    """
    text = text.lower() # Convert text to lower case
    words = re.findall(r'\b\w+\b', text) # Use regex to find words (this handles punctuation properly)
    word_freq = Counter(words) # Use Counter to count the frequency of each word
    
    sorted_word_dict = sorted(dict(word_freq).items(), key=lambda item: item[1], reverse=True)
    
    return sorted_word_dict


def generate_wordcloud(word_dict):
    """
    Generate a word cloud with the most frequent words in the subreddit comments from a word-frequency dictionary
    """
    wordcloud = WordCloud()
    
    wordcloud.generate_from_frequencies(dict(word_dict))
    
    wordcloud.to_file("wordcloud.png")
    
    # plt.imshow(wordcloud)
    # plt.axis('off')
    # plt.show()