import requests
import requests.auth
from pprint import pprint
import json
from datetime import date
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import urllib

f = open("reddit.txt", "r")

user_agent = f.readline().strip('\n')
access_token = ""
sid = SentimentIntensityAnalyzer()

t1 = f.readline().strip('\n')
t2 = f.readline().strip('\n')

user = f.readline().strip('\n')
pw = f.readline().strip('\n')

f.close()

def request_token():
    client_auth = requests.auth.HTTPBasicAuth(t1, t2)
    post_data = {"grant_type": "password", "username": user, "password": pw}
    headers = {"User-Agent": user_agent}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    pprint(response.json())

    reddit_token = json.loads(response.content)
    access_token = reddit_token['access_token']
    token_type = reddit_token['token_type'] 

    access_token = token_type + " " + access_token

def get_subreddit_post(subreddit, post_id):
    print("getting comments from r/" + subreddit)
    params = {'sort': 'top', 'depth': '1', 'limit': '10'}
    headers = {"Authorization": access_token, "User-Agent": user_agent}
    response = requests.get("https://www.reddit.com/r/{}/comments/{}.json".format(subreddit, post_id), headers=headers, params=params)
    print(response.url)
    if(response.status_code != 200):
        print(response)
        print(response.text)
        return
    
    post_content = open("post.json", "w")
    post_json = json.loads(response.content)
    json.dump(post_json, post_content)

    for comment in post_json[1]['data']['children']:
        if("more" in comment['kind']):
            return
        print(str(comment['data']['author']))
        print(str(comment['data']['ups']))
        print(str(comment['data']['body']))

        scores = sid.polarity_scores(str(comment['data']['body']))
        for k in sorted(scores):
            print('{0}: {1}, '.format(k, scores[k]), end='')
            print()
        print("-------------------")
    # for comment in post_json['data']['children']:


def get_hot_post(subreddit):
    print("getting posts from r/" + subreddit)
    params = {'t': 'day', 'limit': '1'}
    headers = {"Authorization": access_token, "User-Agent": user_agent}
    response = requests.get("https://www.reddit.com/r/{}/top/.json".format(subreddit), headers=headers, params=params)
    print(response.url)
    if(response.status_code != 200):
        print(response)
        print(response.text)
        return
    reddit_content = open("reddit_content.json", "w")
    reddit_json = json.loads(response.content)
    json.dump(reddit_json, reddit_content)
    # pprint(reddit_json)
    # for article in 
    for article in reddit_json['data']['children']:
        print(article['data']['id'])
        print(str(article['data']['title']))
        get_subreddit_post(subreddit, article['data']['id'])


def main():
    print("reddit scrapping...")
    request_token()
    subreddit = "technology"
    get_hot_post(subreddit)
    # get_subreddit_posts(subreddit, post)

if __name__ == "__main__":
    main()