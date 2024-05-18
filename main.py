import praw # pip install praw

# setting up authentification: (https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)
reddit = praw.Reddit(client_id ='YsxBF1thW9K4hbTCqioZrg',  
                     client_secret ='aGqKVZ3rw9i2ml32egEYIwnwLLLk-w',  
                     user_agent ='subreddit trending topics by u/vitordcg')

print(reddit)

input_url = input("enter an url: ")
submission = reddit.submission(url=input_url)

subreddit_name = submission.subreddit.display_name

print(f"The subreddit name is: {subreddit_name}")

subreddit = reddit.subreddit(subreddit_name)

top_posts = subreddit.top(limit=50)

# Iterate over the top posts
for post in top_posts:
    print(f'Title: {post.title}')
    print(f'Author: {post.author}')
    print(f'Score: {post.score}')
    print(f'URL: {post.url}')
    print('------------------')