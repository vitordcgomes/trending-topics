import reddit
import datetime

input_str = input("enter an subreddit url or name: ")
subreddit = reddit.get_subreddit(input_str=input_str)

subreddit_name = subreddit.display_name

# Get terminal inputs
start_date = input("Enter a starting date (format: YYYY-MM-DD): ")
end_date = input("Enter a final date (format: YYYY-MM-DD): ")
N = input(f"Enter a number to display the top N most frequent words in the '{subreddit_name}' subreddit: ")

try:
    # Parse the date input string into a datetime object
    start_date_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
except ValueError:
    print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")

posts = reddit.fetch_posts_within_date_range(subreddit, start_date_object, end_date_object)

all_comments = reddit.extract_comments_from_posts(posts=posts)

text = reddit.merge_all_comments_into_text(all_comments=all_comments)

filtered_text = reddit.remove_stopwords(text=text, lang='portuguese')

word_dict = reddit.get_words_frequency(text=filtered_text)

print(f"Top {N} most frequent words in subreddit '{subreddit_name}':")
for i in range(min(int(N), len(word_dict))): 
    word, frequency = word_dict[i]
    print(f"    {i+1}. '{word}': {frequency}") # print the N most frequent words
    
reddit.generate_wordcloud(word_dict=word_dict)
    
# proposition: instead of picking all the posts and getting the comments inside each of them,
# get the comments directly from the subreddit object within the date range.
