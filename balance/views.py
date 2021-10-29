from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib import request as req

# Create your views here.
def get_data(symbol):
    headers=('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

    url='http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)

    opener = req.build_opener()
    opener.addheaders = [headers]

    with opener.open(url) as doc:
        soup = BeautifulSoup(doc, 'lxml', from_encoding='euc-kr')
        cur_price = soup.find('strong', id='_nowVal')
        cur_rate = soup.find('strong', id='_rate')
        stock = soup.find('title')
        stock_name = stock.text.split(':')[0].strip()
        return cur_price.text, cur_rate.text.strip(), stock_name

def main_view(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()
    rows = []
    total = 0
    
    for x in mylist:
        cur_price, cur_rate, stock_name = get_data(x[0])
        price = cur_price.replace(',','')
        stock_count = format(int(x[1][0]), ',')
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')
        rows.append([stock_name, x[0], cur_price, stock_count, cur_rate, stock_sum])
        total = total + int(price) * int(x[1][0])
    
    total_amount = format(total, ',')
    values = {'rows' : rows, 'total' : total_amount}
    return render(request, 'balance.html', values)
    
    