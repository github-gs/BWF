#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:04:15 2018

@author: gaosheng
"""

import re
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

class BWF:
    def __init__(self,rank_high,rank_low):
        self.rank_hign = rank_high
        self.rank_low = rank_low
    def compute_page(self):
        if self.rank_hign%25==0:
           page_a=self.rank_hign // 25
        else:
           page_a = self.rank_hign // 25+1
        if self.rank_low%25==0:
           page_b=self.rank_low // 25
        else:
           page_b = self.rank_low // 25+1
        return page_a,page_b

    def get_rank(self,page_a,page_b):
        rank=[]
        page=page_b-page_a+1
        n=0
        for i in range(page_a,page_b+1):
            try:
                html = requests.get('https://bwfbadminton.com/rankings/2/bwf-world-rankings/6/men-s-singles/2018/33/?rows=25&page_no=%s' % i,headers=headers).text
            except:
                print('The network is down, please try later!')
                break
            else:
                soup = BeautifulSoup(html, 'html.parser')
                date_pattern = re.compile('Last updated :  (.*)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nBWF WORLD RANKINGS')
                rank_pattern = re.compile('\n(.*)\n\n\n\n\n                \t(.*)\t\t\t\t\n\n\n\n\n\n\n\n\n                        (.*)                    \n\n\n\n\n\n')
                result = rank_pattern.findall(soup.get_text())
                update_date = date_pattern.findall(soup.get_text())
                rank = rank + result
                n=n+1
                print('get %s of %s' %(n,page))
        return rank,update_date,i

    def print(self,rank,update_date):
        print_item=rank
        for item in print_item:
            if int(item[0])<=self.rank_low and int(item[0])>=self.rank_hign:
              print('Last update time: ' + update_date[0] + '   BWF_RANK: ' + item[0] + '   COUNTRY: ' + item[1] + '   NAME: ' + item[2])
try:
   rank_range=input('\n'+'Type the range of ranking'+'\n'+'such as:'+'\n'+'1,10'+'\n'+'and press Enter:'+'\n')
except:
   print('Sorry,Only Can Input Integer And Check Your Input Format.')
else:
   rank_upper=int(rank_range.split(',')[0])
   rank_lower=int(rank_range.split(',')[1])
   bwf=BWF(rank_upper,rank_lower)
   page_a,page_b=bwf.compute_page()
   rank,update_date,i=bwf.get_rank(page_a,page_b)
   if i==page_b:
       bwf.print(rank, update_date)

