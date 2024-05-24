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

text = reddit.merge_all_comments_into_text(all_comments=all_comments)
# print(text)

filtered_text = reddit.remove_stopwords(text)
# print(filtered_text)

word_dict = reddit.get_words_frequency(filtered_text)

N=100
for i in range(min(N, len(word_dict))): 
    print(word_dict[i]) # print the N most frequent words
    
# proposition: instead of picking all the posts and getting the comments inside each of them,
# get the comments directly from the subreddit object within the date range.
