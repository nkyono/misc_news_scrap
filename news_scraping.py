'''
Uses google news api to get news headlines
uses nltk for sentiment analysis on headline titles
'''

import requests
from pprint import pprint
import json
from datetime import date
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def main():
    print("scraping...")

    f = open("news.txt", "r")
    apiKey = f.readline().strip('\n')


    # https://newsapi.org/docs/endpoints/sources
    sources = []
    google_us_news_index_URL = "https://newsapi.org/v2/sources?category=business&language=en&country=us&apiKey={}".format(apiKey)
    google_response = requests.get(google_us_news_index_URL)
    if(google_response.status_code != 200):
        print(google_response)
        return
    google_json = json.loads(google_response.content)
    for source in range(len(google_json['sources'])):
        sources.append(google_json['sources'][source]['id'])

    print("# of sources: ", len(sources))
    source_string = ','.join(sources)
    print(source_string)

    # overwriting sources so I can test with only one source
    # source_string = "bloomberg"

    query_date_from = date.today().replace(month=date.today().month-1)
    # print(str(query_date))
    # query_date_to = "&" + date.today().replace(month=date.today().month-1)

    # to query for specific words and such
    query = "q=AAPL&"

    # initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()


    # https://newsapi.org/docs/endpoints/everything
    for page in range(1,6):
        google_news_URL = "http://newsapi.org/v2/everything?{}sources={}&from={}&language=en&page={}&apiKey={}".format(query, source_string, query_date_from, page, apiKey)
        # google_news_api = "24b35161aae841d6ac820be7a3c29e23"  # remove? although its free / url has it in it
        print(google_news_URL+'\n')
        google_response = requests.get(google_news_URL)
        if(google_response.status_code != 200):
            print(google_response)
            print(google_response.text)
            return
        # only get a certain number of results, need to use page=___ in request to get other results
        # google_content = open("google_reponse.json", "w")
        google_json = json.loads(google_response.content)
        # json.dump(google_json, google_content)
        # google_content.close()
        for article in range(len(google_json['articles'])):
            print(google_json['articles'][article]['source']['id'])
            print(google_json['articles'][article]['publishedAt'])
            print(google_json['articles'][article]['title'])
            # print(google_json['articles'][article]['description'])

            # get vader scores (sentiment analysis) for article titles
            scores = sid.polarity_scores(google_json['articles'][article]['title'])
            for k in sorted(scores):
                print('{0}: {1}, '.format(k, scores[k]), end='')
                print()
            print("-------------------")


    # Database schema
    # companies : id , name , symbol
    # articles : id , source_id , author , date , title , description , compound_vader , neg_vader , neu_vader , pos_vader 

    # if we also store sources, we could get the average of the vader scores they give for different companies (source x vader x company)
    # would need to be stored in a different table
    # sources table and sources_company_vader table

    # start of cnn request, couldn't get api key
    '''
    cnn_url = "https://services.cnn.com/newsgraph/"
    cnn_response = requests.get(cnn_url)
    cnn_content = open("cnn_response", "w")
    cnn_content.write(str(cnn_response.content))
    cnn_content.close()
    '''



if __name__ == "__main__":
    main()