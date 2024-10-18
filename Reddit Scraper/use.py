import time
from utils import Utils
from reddit_miner import RedditMiner

miner = Utils()

def get_data():
    subreddit = input("Subreddit: ") or 'RandomThoughts'

    print(f"Target: r/{subreddit}")

    start_time = time.time()

    miner.data_hoarder(subreddit, limit=250, category='top', output_file=f"{subreddit}.json")
    # Stress Test lesgoo
    print(f"Data from subreddit '{subreddit}' saved."
              f"(Time taken: {time.time() - start_time:.2f} seconds)")

def get_image(url):
    miner.download_image(url)
    # we could have used this alongside the extracted posts data


def get_post_details(url):
    # This will be useful, i presume
    # Get Comments, and Body Text of certain Posts using the permalink
    permalink = "/r/AskReddit/comments/x7ebbc/what_are_the_most_overused_redundant_and_annoying/"
    post_details = miner.scrape_post_details(permalink)

    print(f"\nTitle: {post_details['title']}")
    body = post_details['body']
    print(f"Body: {body[:200]}{'... (Truncated for display)' if len(body) > 200 else ''}")
    print(f"Comments: {len(post_details['comments'])} comments found")
    for x in range(min(len(post_details['comments']), 10)):
        comment = post_details['comments'][x]
        print(f"\n\nComment {x + 1}:")
        print(f"\tAuthor: {comment['author']}")
        comment_body = comment['body']
        print(f"\tBody: {comment_body[:200]}{'... (Truncated for display)' if len(comment_body) > 200 else ''}")

    with open("post_details.json", "w") as f:
        f.write(str(post_details))



# Other Utility Stuffs
#######################################
def get_user_data(username):
    # Get posts and comments of a certain user
    print(f"Scraping data for user: {username}")
    miner.user_osint(username, limit=3000, output_file='user_data.json')
    print(f"User data for '{username}' saved to 'user_data.json' ")

def get_search_data(search_query):
    # Search on Reddit for Posts related to this
    print(f"Searching Reddit for: {search_query}...")
    search_results = miner.search_reddit(search_query, limit=5)
    print("Search completed.")
    
    for idx, result in enumerate(search_results, start=1):
        print(f"\nResult {idx}:")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Description: {result['description']}")