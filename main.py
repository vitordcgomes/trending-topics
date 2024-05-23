import reddit
import datetime

input_str = input("enter an subreddit url or name: ")
subreddit = reddit.get_subreddit(input_str=input_str)

subreddit_name = subreddit.display_name
print(f"The subreddit name is: {subreddit_name}")


# Get date input from the terminal
start_date = input("Enter a starting date (format: YYYY-MM-DD): ")
end_date = input("Enter a final date (format: YYYY-MM-DD): ")

try:
    # Parse the date input string into a datetime object
    start_date_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
except ValueError:
    print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")

posts = reddit.fetch_posts_within_date_range(subreddit, start_date_object, end_date_object)

print(f'Number of posts: {len(posts)}')

all_comments = reddit.extract_comments_from_posts(posts=posts)

# # Iterate over the top posts
# for post in posts:
#     # print(type(post))
#     print(f'Title: {post.title}')
#     print(f'Author: {post.author}')
#     print(f'URL: {post.url}')
#     # print(f'date: {post.date}')
#     print('------------------')

# proposition: instead of picking all the posts and getting the comments inside each of them,
# get the comments directly from the subreddit object within the date range.
