import requests
import time 
from googlesearch import search

class RedditMiner:
    def __init__(self, user_agent='Mozilla/5.0', proxy=None):
        self.headers = {'User-Agent': user_agent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Add proxy configuration if provided
        if proxy:
            self.session.proxies.update({
                'http': proxy,
                'https': proxy
            })

    def search_reddit(self, query, limit=10, after=None, before=None, lang="en", sleep_interval=0):
        time_filter = f" after:{after}" if after else ""
        time_filter += f" before:{before}" if before else ""

        google_query = f'site:reddit.com {query}{time_filter}'
        search_results = search(google_query, num_results=limit, lang=lang, sleep_interval=sleep_interval, advanced=True)
        
        results = [{'title': result.title, 'link': result.url, 'description': result.description} for result in search_results]
        return results

    def scrape_post_details(self, permalink):
        url = f"https://www.reddit.com{permalink}.json"
        response = self.session.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch post data: {response.status_code}")
            return None

        post_data = response.json()
        main_post = post_data[0]['data']['children'][0]['data']
        title = main_post['title']
        body = main_post.get('selftext', '')
        comments = self._extract_comments(post_data[1]['data']['children'])
        
        return {'title': title, 'body': body, 'comments': comments}

    def _extract_comments(self, comments):
        extracted_comments = []
        for comment in comments:
            if comment['kind'] == 't1':
                extracted_comments.append({
                    'author': comment['data']['author'],
                    'body': comment['data']['body'],
                    'replies': self._extract_comments(comment['data']['replies']['data']['children']) if comment['data']['replies'] else []
                })
        return extracted_comments

    def scrape_user_data(self, username, limit=10):
        base_url = f"https://www.reddit.com/user/{username}/.json"
        params = {'limit': limit, 'after': None}
        all_items = []
        count = 0

        while count < limit:
            response = self.session.get(base_url, params=params)
            
            # Check for status code errors
            if response.status_code != 200:
                print(f"Failed to fetch data for user {username}: {response.status_code}")
                break

            try:
                data = response.json()
            except ValueError:
                print(f"Failed to parse JSON response for user {username}.")
                break
            
            if 'data' not in data or 'children' not in data['data']:
                print(f"No 'data' or 'children' field found in response for user {username}.")
                break

            items = data['data']['children']
            if not items:
                print(f"No more items found for user {username}.")
                break

            for item in items:
                kind = item['kind']
                item_data = item['data']
                if kind == 't3':  # This represents a post
                    post_url = f"https://www.reddit.com{item_data.get('permalink', '')}"
                    all_items.append({
                        'type': 'post',
                        'title': item_data.get('title', ''),
                        'subreddit': item_data.get('subreddit', ''),
                        'url': post_url,
                        'created_utc': item_data.get('created_utc', '')
                    })
                elif kind == 't1':  # This represents a comment
                    comment_url = f"https://www.reddit.com{item_data.get('permalink', '')}"
                    all_items.append({
                        'type': 'comment',
                        'subreddit': item_data.get('subreddit', ''),
                        'body': item_data.get('body', ''),
                        'created_utc': item_data.get('created_utc', ''),
                        'url': comment_url
                    })
                count += 1
                if count >= limit:
                    break

            params['after'] = data['data'].get('after')
            if not params['after']:
                break
        
        return all_items

    def fetch_reddit_data(self, subreddit, limit=10, category='hot', time_filter='all'):
        if category not in ['hot', 'top']:
            raise ValueError("Category must be either 'hot' or 'top'")


        batch_size = 100
        total_fetched = 0
        after = None
        all_posts = []


        while total_fetched < limit:
            
            if category == 'hot':
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={batch_size}&after={after}&raw_json=1"
            else:  # category == 'top'
                url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time_filter}&limit={batch_size}&after={after}&raw_json=1"

            response = self.session.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code}")
                return all_posts

            data = response.json()
            posts = data['data']['children']

            if not posts:
                break 


            for post in posts:
                post_data = post['data']
                post_info = {
                    'title': post_data['title'],
                    'author': post_data['author'],
                    'permalink': post_data['permalink'],
                    'score': post_data['score'],
                    'num_comments': post_data['num_comments'],
                    'created_utc': post_data['created_utc']
                }

                # Check if the post contains an image and add image URL if present
                if post_data.get('post_hint') == 'image' and 'url' in post_data:
                    post_info['image_url'] = post_data['url']
                elif 'preview' in post_data and 'images' in post_data['preview']:
                    post_info['image_url'] = post_data['preview']['images'][0]['source']['url']

                # Check if the post contains a thumbnail
                if 'thumbnail' in post_data and post_data['thumbnail'] and post_data['thumbnail'] != 'self':
                    post_info['thumbnail_url'] = post_data['thumbnail']
                
                all_posts.append(post_info)
                total_fetched+=1
                

                if total_fetched>=limit:
                    break

            after = data['data'].get('after')
            print(f"> Posts Fetched: {total_fetched}")

            if not after:
                print("No 'after' left.")
                break
            time.sleep(0.5) # will this help? i dont know, worked on my machine
        return all_posts
