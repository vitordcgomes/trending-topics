import praw # pip install praw
import re
import datetime

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

    print(f'Number of list of comments: {len(all_comments)}')
    
    total_comments = 0
    for post_comments in all_comments:
        total_comments += len(post_comments)
    
    print(f'Number of total comments: {total_comments}')
    
    return all_comments
