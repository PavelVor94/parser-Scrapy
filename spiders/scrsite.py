import scrapy
import json
from pandas import DataFrame
import time


class ScrsiteSpider(scrapy.Spider):
    name = 'scrsite'
    start_urls = ['https://explore.duneanalytics.com/api/queries/20717/embed_with_result?api_key=AMQ1dlZiA1L3kecz2N6gZvADwMk72ulReJzCpIpL']
    BASE_URL = "https://duneanalytics.com/ethereum/address/"
    start = time.time()


    def parse(self, response):
        rows = json.loads(response.text)["query_result"]['data']['rows']
        count = 0
        list_result = []
        for row in rows:
            address = row['address'].split('>')[1].split('<')[0]
            list_result.append({
                "url": self.BASE_URL+address,
                'address': address,
                'balance_six_month_ago': str(row['balance_six_month_ago']) if row['balance_six_month_ago'] else '',
                'balance_three_month_ago': str(row['balance_three_month_ago']) if row['balance_three_month_ago'] else '',
                'balance_one_month_ago': str(row['balance_one_month_ago']) if row['balance_one_month_ago'] else '',
                'total_balance': str(row['total_balance']) if row['total_balance'] else ''
            })
            count+=1
            print(f'сделано {count} из {len(rows)} --- {count/len(rows)*100:.2f}%')
        DataFrame(list_result).to_excel('./result.xlsx' , ';' , index=False)
        print(time.time()-self.start)

