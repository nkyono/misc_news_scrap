'''
supposedly using id to search is faster
took a while for it to complete last time
maybe switching to id would be beneficial
or at least using id for next selenium thing
'''

import csv
import requests
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_nasdaq_selenium():
    ff_opt = webdriver.FirefoxOptions()
    ff_opt.set_headless()
    firefox = webdriver.Firefox(options=ff_opt)
    stock_symbol = 'AAPL'
    url = 'https://www.nasdaq.com/market-activity/stocks/{}/historical'.format(stock_symbol)
    firefox.get(url)
    print(firefox.title)

    # 1y button xpath:
    # /html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]
    # firefox.find_element_by_xpath('/html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]').click()
    # OHLC table:
    # /html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody
    stock_data = firefox.find_element_by_xpath('/html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody')
    print(stock_data.get_attribute('innerHTML'))
    # OHLC table row:
    # /html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]

    # going through the HTML, I found the "historical-data__download" class and "/api/v1/historical/AAPL/stocks/2019-07-06/2020-07-06" link
    # allows the download of a .csv of the data
    # https://www.nasdaq.com/api/v1/historical/AAPL/stocks/2019-07-06/2020-07-06

    firefox.quit()


def get_nasdaq_stock_data(stock):
    start_date = date.today().replace(year=date.today().year-1)
    end_date = date.today()
    stock_symbol = stock

    print("getting {}...".format(stock_symbol))

    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    url_check = 'https://www.nasdaq.com'
    # print(url_check)
    url = 'https://www.nasdaq.com/api/v1/historical/{}/stocks/{}/{}'.format(stock_symbol, start_date, end_date)
    # print(url)

    check = requests.get(url_check, headers=user_agent)
    if(check.status_code != 200):
        print(check)
        print(check.text)
        return
    # print(check.status_code)

    nasdaq_response = requests.get(url, headers=user_agent)
    if(nasdaq_response.status_code != 200):
        print(nasdaq_response)
        print(nasdaq_response.text)
        return
    # print(nasdaq_response.status_code)

    with open('./nasdaq/{}_historical.csv'.format(stock_symbol), 'wb') as f:
        f.write(nasdaq_response.content)

def get_nasdaq100():
    # https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index
    print("getting nasdaq100...")


    try: 
        ff_opt = webdriver.FirefoxOptions()
        ff_opt.headless = True
        firefox = webdriver.Firefox(options=ff_opt)
        url = 'https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index'
        firefox.get(url)
        # print(firefox.title)

        # waits for table to load
        # had issues with no rows showing because I guess the table hadn't loaded in yet
        try:
            WebDriverWait(firefox, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/article/div[2]/div/div[3]/div[3]/div[2]/table/tbody/tr")))
        except TimeoutException:
            print("Waiting for table timeout")
            return  
        # 1y button xpath:
        # /html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]
        # firefox.find_element_by_xpath('/html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]').click()
        # OHLC table:
        # /html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody
        tbody_rows = len(firefox.find_elements_by_xpath("/html/body/div[1]/div/main/div/article/div[2]/div/div[3]/div[3]/div[2]/table/tbody/tr"))
        # don't need all the columns just first two. I'll just hard code instead of for loop
        # tbody_cols = len(firefox.find_elements_by_xpath('/html/body/div[1]/div/main/div/article/div[2]/div/div[3]/div[3]/div[2]/table/tbody/tr/td'))
        # print("rows: ", tbody_rows)
        with open('nasdaq100.csv','w') as file:
            writer = csv.writer(file)
            for row in range(tbody_rows):
                symbol = firefox.find_element_by_xpath('/html/body/div[1]/div/main/div/article/div[2]/div/div[3]/div[3]/div[2]/table/tbody/tr[{}]/th/a'.format(row+1))
                name = firefox.find_element_by_xpath('/html/body/div[1]/div/main/div/article/div[2]/div/div[3]/div[3]/div[2]/table/tbody/tr[{}]/td[1]'.format(row+1))
                # print(symbol.text + " " + name.text)
                writer.writerow([symbol.text, name.text])
        file.close()
    except:
        print("Something bad happened")
    finally:
        firefox.quit()

    # OHLC table row:
    # /html/body/div[1]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]

    # going through the HTML, I found the "historical-data__download" class and "/api/v1/historical/AAPL/stocks/2019-07-06/2020-07-06" link
    # allows the download of a .csv of the data
    # https://www.nasdaq.com/api/v1/historical/AAPL/stocks/2019-07-06/2020-07-06

def get_all_nasdaq():
    print("get all nasdaq100...")

    with open('nasdaq100.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        for row in rows:
            get_nasdaq_stock_data(row[0])


def get_nyse():
    print("getting nyse...")

    try: 
        ff_opt = webdriver.FirefoxOptions()
        ff_opt.headless = True
        firefox = webdriver.Firefox(options=ff_opt)
        # not directly from nyse; will this cause problems in the future? probably
        url = 'https://www.marketbeat.com/stocks/NYSE/'
        firefox.get(url)
        # print(firefox.title)

        # //*[@id="form1"]/div[3]/div/table/tbody/tr[1]
        # /html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[1]
        try:
            WebDriverWait(firefox, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr")))
        except TimeoutException:
            print("Waiting for table timeout")
            return  

        tbody_rows = len(firefox.find_elements_by_xpath("/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr"))
        
        with open('nyse.csv','w') as file:
            writer = csv.writer(file)
            # need check for ads in the table
            for row in range(tbody_rows):
                if("bottom-sort" not in firefox.find_element_by_xpath('/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[{}]'.format(row+1)).get_attribute("class")):
                    num_att = 3
                    if("company-thumbnail" not in firefox.find_element_by_xpath('/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[{}]/td[1]/a/div[1]'.format(row+1)).get_attribute("class")):
                        num_att = 2
                    symbol = firefox.find_element_by_xpath('/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[{}]/td[1]/a/div[{}]'.format(row+1, num_att-1))
                    name = firefox.find_element_by_xpath('/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[{}]/td[1]/a/div[{}]'.format(row+1, num_att))
                    sector = firefox.find_element_by_xpath('/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[{}]/td[2]/a'.format(row+1))
                    industry = firefox.find_element_by_xpath('/html/body/div[1]/main/article/form/div[3]/div/table/tbody/tr[{}]/td[3]'.format(row+1))
                    # print(symbol.text + " " + name.text)
                    writer.writerow([symbol.text, name.text, sector.text, industry.text])
        file.close()
    except Exception as e:
        print("Something bad happened")
        print(e)
    finally:
        firefox.quit()

def get_nyse_stock_data(stock):
    print("getting {}...".format(stock))
    # don't want to deal with the date stuff on nyse, but it defaults to a year
    # start_date = date.today().replace(year=date.today().year-1)
    # end_date = date.today()

    # https://www.nyse.com/quote/XNYS:DIS
    url = "https://www.nyse.com/quote/XNYS:{}".format(stock)

    # row
    # /html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[1]
    # /html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[250]
    # date, open, high, low, close, volume 
    # /html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[1]/div[1]

    try: 
        ff_opt = webdriver.FirefoxOptions()
        ff_opt.headless = True
        firefox = webdriver.Firefox(options=ff_opt)
        firefox.get(url)
        # print(firefox.title)

        try:
            WebDriverWait(firefox, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div")))
        except TimeoutException:
            print("Waiting for table timeout")
            return  

        rows = len(firefox.find_elements_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div"))
        
        with open('./nyse/{}_historical.csv'.format(stock),'w') as file:
            writer = csv.writer(file)
            # need check for ads in the table
            # Date, Close/Last, Volume, Open, High, Low
            writer.writerow(["Date", "Close/Last", "Volume", "Open", "High", "Low"])
            for row in range(rows):
                day = firefox.find_element_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[{}]/div[1]".format(row+1))
                open_price = firefox.find_element_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[{}]/div[2]".format(row+1))
                high_price = firefox.find_element_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[{}]/div[3]".format(row+1))
                low_price = firefox.find_element_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[{}]/div[4]".format(row+1))
                close_price = firefox.find_element_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[{}]/div[5]".format(row+1))
                volume = firefox.find_element_by_xpath("/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[4]/div[3]/div/div/div[2]/div/div[{}]/div[6]".format(row+1))
                writer.writerow([day.text, close_price.text, volume.text, open_price.text, high_price.text, low_price.text])
        file.close()
    except Exception as e:
        print("Something bad happened")
        print(e)
    finally:
        firefox.quit()

def get_all_nyse():
    print("get all nyse...")
    with open('timeouts.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        for row in rows:
            get_nyse_stock_data(row[0])

def main():
    print("scrapping stock historical data...")
    
    '''Nasdaq'''
    '''puts nasdaq100 into csv'''
    # get_nasdaq100()
    '''gets select nasdaq stock information and puts in csv'''
    # get_nasdaq_stock_data('AAPL')
    '''gets historical data for all nasdaq100 stocks
        *** to implement
        '''
    # get_all_nasdaq()
    # get_nasdaq_selenium()
    print()

    '''NYSE'''
    '''puts top NYSE stocks into csv'''
    # get_nyse()
    '''gets select nyse stock info and puts in csv'''
    # get_nyse_stock_data('DIS')
    '''gets historical data for all nyse ~250 stocks
        *** to implement
        '''
    get_all_nyse()

if __name__ == "__main__":
    main()