import re
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

class BWF:
    def __init__(self,rank_high,rank_low,type):
        self.rank_hign = rank_high              ######### rank begin
        self.rank_low = rank_low
        self.weekday=int(time.strftime("%W"))-1 ######### week day info 
        self.type=type

    def compute_page(self):                     ######### change page per 25 players
        if self.rank_hign%25==0:
           page_a=self.rank_hign // 25
        else:
           page_a = self.rank_hign // 25+1
        if self.rank_low%25==0:
           page_b=self.rank_low // 25
        else:
           page_b = self.rank_low // 25+1
        return page_a,page_b

    def get_type(self):                         ########## distinguish the player type 
        if self.type=='1':
            number_index='6'
            type_text='men-s-singles'
        if self.type=='2':
            number_index = '7'
            type_text='women-s-singles'
        if self.type=='3':
            number_index = '8'
            type_text='men-s-doubles'
        if self.type=='4':
            number_index = '9'
            type_text='women-s-doubles'
        if self.type=='5':
            number_index = '10'
            type_text='mixed-doubles'
        type=[number_index,type_text]       ##### a list
        return type

    def rank_pattern(self,type):               ############ distinguish the soup pattern according different player types
        if type[0]=='6' or type[0]=='7':
            rank_pattern = re.compile('\n(.*)\n\n\n\n\n                \t(.*)\t\t\t\t\n\n\n\n\n\n\n\n\n                        (.*)                    \n\n\n\n\n\n(.*)\n\n\n\n            (.*)        \n\n(.*)\n\n\n(.*)\n\n\n')
        if type[0]=='8' or type[0]=='9' or type[0]=='10':
            rank_pattern = re.compile('\n(.*)\n\n\n\n\n                \t(.*) \n                \n\n\n\n\n                \t(.*)                \n\n\n\n\n\n\n\n(.*)\n\n\n(.*)\n\n\n\n\n\n(.*)\n\n\n\n            (.*)        \n\n(.*)\n\n\n(.*)\n\n\n')
        return rank_pattern


    def get_rank(self,page_a,page_b,type,Rank_pattern):              ######## catch information using soup
        rank=[]
        page=page_b-page_a+1
        n=0
        for i in range(page_a,page_b+1):
            url='https://bwfbadminton.com/rankings/2/bwf-world-rankings/%s/%s/2019/%s/?rows=25&page_no=%s' %(type[0],type[1],self.weekday,i)
           
            try:
                html = requests.get(url,headers=headers).text
            except:
                print('The network is down, please try later!')
                break
            else:
                soup = BeautifulSoup(html, 'html.parser')
                date_pattern = re.compile('Last updated :  (.*)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nBWF WORLD RANKINGS\n')
                rank_pattern = Rank_pattern
                result = rank_pattern.findall(soup.get_text())
                update_date = date_pattern.findall(soup.get_text())
                rank = rank + result
                n=n+1
                print('get the %s page of %s page(s)' %(n,page))
        return rank,update_date,i,type[0]

    def printf(self,rank,update_date,type_number):             ######### print the information 
        print('\n'+'Last update time: ' + update_date[0]+'\n')
        if type_number=='6' or type_number=='7':
            print('BWF_RANK    COUNTRY    NAME    CHANGE    WIN-LOSE    PRIZE    POINTS/TOURNAMENTS ' + '\n')
            print_item = rank
            for item in print_item:
                if int(item[0]) <= self.rank_low and int(item[0]) >= self.rank_hign:
                    print('    '.join(item))
        else:
            print('BWF_RANK    COUNTRY    NAME    CHANGE    WIN-LOSE    PRIZE    POINTS/TOURNAMENTS ' + '\n')
            print_item = rank
            for item in print_item:
                if int(item[0]) <= self.rank_low and int(item[0]) >= self.rank_hign:
                    double1=[item[0],item[1],item[3],item[5],item[6],item[7],item[8]]
                    double2=[item[0],item[1],item[4],item[5],item[6],item[7],item[8]]
                    print('    '.join(double1))
                    print('    '.join(double2)+'\n')


########### Let's do it!
try:
   type=input('\n'+'men single: 1'+'  '+'women single:2'+'  '+'men double:3'+'  '+'women double:4'+'  '+'mixed double:5'+'\n'+'and ENTER the number you want to check:'+'\n')

   rank_range=input('\n'+'Type the range of ranking'+'\n'+'such as:'+'\n'+'1,10'+'\n'+'and press Enter:'+'\n')
except:
   print('Sorry,Only Can Input Integer And Check Your Input Format.')
else:
   rank_upper=int(rank_range.split(',')[0])
   rank_lower=int(rank_range.split(',')[1])
   bwf=BWF(rank_upper,rank_lower,type)

   page_a,page_b=bwf.compute_page()      ## page
   Type=bwf.get_type()                   ## type
   rank_pattern=bwf.rank_pattern(Type)   ## pattern
   rank,update_date,i,type_number=bwf.get_rank(page_a,page_b,Type,rank_pattern)  ## information got
   if i==page_b:
       bwf.printf(rank,update_date,type_number)                                 ## done!

