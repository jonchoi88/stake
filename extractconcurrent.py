#Python 2.7.6
#RestfulClient.py

import requests
from requests.auth import HTTPDigestAuth
from concurrent.futures import ThreadPoolExecutor
import json
import csv
from time import sleep
import sys
import functools
import time

results = []
with open('tickers.csv') as File:
    reader = csv.reader(File)
    results = list(reader)

def send_url_request(url):
    return requests.get(url)


def main():
    url_requests = []
    #get the start date of the week
    startDate = input("Please insert the start date for the week (YYYY-MM-DD)\n Start Date: ")

    #get the end date
    endDate = input("Please insert the end date for the week (YYYY-MM-DD)\n End Date: ")


    urls = []
    i = 1
    while i < len(results):
        stockname = results[i][0]
        # Replace with the correct URL
        url = "https://api.tiingo.com/tiingo/daily/"+stockname+"/prices?endDate="+ endDate +"&startDate=" +startDate +"&token=820fb8ecbdf96305753989c1b0a31df690a97950"
        urls.append(url)
        i = i + 1

    pool = ThreadPoolExecutor(25)

    print("Sending Requests")
    z = 1
    listLength = len(urls)
    for url in urls:
        url_requests.append(pool.submit(send_url_request, url))

        percentComplete = round((z/listLength)*100 , 2)
        print("Requests Sent Completion: " + str(percentComplete) + "%")
        z += 1
    print("Requests Sent")

    print("Awaiting Responses from Tingo")

    for k in range (1, 100):
        while url_requests[int(round((len(url_requests)-1)*(k/100)))].done() == False:
            sleep(0.001)
        print("Responses Complete = " + str(k) + "% complete")
    print("Responses Complete = 100% complete")

    jsonStrings = []
    for response in url_requests:
        responseJson = response.result()
        if not (responseJson.ok):
            emptyList = []
            jsonStrings.append(emptyList)
        else:
            jData = json.loads(responseJson.content)
            jsonStrings.append(jData)

    print("Writing to CSV")
    with open('tickerlist.csv', 'w') as csvfile:

        fieldnames = ['Ticker', 'Percentage Change']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()


        y = 1
        for jsonData in jsonStrings:
            if(len(jsonData) == 0):
                writer.writerow({'Ticker': results[y][0], 'Percentage Change': "NA"})
                y = y + 1
            else:
                open1 = jsonData[0]['adjClose']
                close = jsonData[len(jsonData) - 1]['adjClose']
                difference = close - open1
                percent = ((difference/open1)*100)
                writer.writerow({'Ticker': results[y][0], 'Percentage Change': str(round(percent,2))})
                y = y + 1
main()
