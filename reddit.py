import praw # pip install praw
import re
from collections import Counter
from nltk.corpus import stopwords # pip install nltk
from nltk.tokenize import word_tokenize

# setting up authentification: (https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)
reddit = praw.Reddit(client_id ='YsxBF1thW9K4hbTCqioZrg',  
                     client_secret ='aGqKVZ3rw9i2ml32egEYIwnwLLLk-w',  
                     user_agent ='subreddit trending topics by u/vitordcg')


def get_subreddit(input_str):
    """
    Extracts the subreddit name from a URL or returns the input directly if it's already a plain name.
    """
    # Regular expression to match subreddit URLs
    url_pattern = re.compile(r'(https?://)?(www\.)?reddit\.com/r/([^/]+)/?')
    
    # Match the input string against the pattern
    match = url_pattern.match(input_str)
    
    if match:
        # Extract subreddit name from the URL
        subreddit_name = match.group(3) # ([^/]+)/?
    else:
        # Use the input directly as the subreddit name
        subreddit_name = input_str

    # Get subreddit object
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit


def fetch_posts_within_date_range(subreddit, start_date, end_date):
    """
    Fetches all posts from a subreddit within a specified date range.
    """
    
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    
    filtered_posts = []
    
    for submission in subreddit.new(limit=None):  # Use limit=None to fetch all new posts
        if start_timestamp <= submission.created_utc <= end_timestamp:
            # post_date = datetime.datetime.fromtimestamp(submission.created_utc)
            filtered_posts.append(submission)
    
    return filtered_posts

def extract_comments_from_posts(posts):
    # Iterate over the top posts
    all_comments = []
    for post in posts:
        post_comments = []
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            post_comments.append(comment.body)
            
        all_comments.append(post_comments)
    
    total_comments = 0
    for post_comments in all_comments:
        total_comments += len(post_comments)
    
    print(f'Number of total comments: {total_comments}')
    
    return all_comments

def merge_all_comments_into_text(all_comments):
    """
    Merges all comments into a single text string.
    """
    merged_text=""

    for post in all_comments:
        merged_text += " ".join(post)
    
    return merged_text

def remove_stopwords(text):
    """
    Removes stopwords from a text
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text, language='english')
    
    non_stopwords = [word for word in words if word.lower() not in stop_words]
    
    filtered_text = " ".join(non_stopwords)
    
    return filtered_text

# Function to create a word frequency dictionary
def get_words_frequency(text):
    """
    Create a word frequency dictionary and sorts it
    """
    # Convert text to lower case
    text = text.lower()
    # Use regex to find words (this handles punctuation properly)
    words = re.findall(r'\b\w+\b', text)
    # Use Counter to count the frequency of each word
    word_freq = Counter(words)
    
    sorted_word_dict = sorted(dict(word_freq).items(), key=lambda item: item[1], reverse=True)
    return sorted_word_dict