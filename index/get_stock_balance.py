import win32com.client
from slacker import Slacker
from datetime import datetime
import requests

#slacker 메세지
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

myToken = "xoxb-1952383700611-1937427975911-chjYk26M3GQqRZZiicFLYTmI"

def dbgout(message):
  print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
  strbuf = datetime.now().strftime('[%m/%d %H:%M:%S]') + message
  post_message(myToken,"#stock", strbuf)

#계좌조회
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil') #주문관련도구
cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033') #계좌 정보
cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode') #종목코드
cpCash = win32com.client.Dispatch("CpTrade.CpTdNew5331A") #주문 가능 금액

def get_stock_balance(code):
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0] #계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1) #-1:전체, 1:주식, 2:선물/옵션
    cpBalance.SetInputValue(0, acc) #계좌번호
    cpBalance.SetInputValue(1, accFlag[0]) #상품구분 - 주식상품 중 첫번째
    cpBalance.SetInputValue(2, 50) #요청건수
    cpBalance.BlockRequest()

    if code == 'ALL':
        dbgout('계좌명: ' + str(cpBalance.GetHeaderValue(0)))
        dbgout('결제잔고수량: ' + str(cpBalance.GetHeaderValue(1)))
        dbgout('평가금액: ' + str(cpBalance.GetHeaderValue(3)))
        dbgout('평가손익: ' + str(cpBalance.GetHeaderValue(4)))
        dbgout('종목수: ' + str(cpBalance.GetHeaderValue(7)))

    stock = []
    for i in range(cpBalance.GetHeaderValue(7)):
        stock_code = cpBalance.GetDataValue(12, i) #종목코드
        stock_name = cpBalance.GetDataValue(0, i) #종목명
        stock_qty = cpBalance.GetDataValue(15, i) #수량
        if code == 'ALL':
            dbgout(str(i+1) + ' ' + stock_code + '(' + stock_name + ')' + ':' + str(stock_qty))
            stocks.append({'code' : stock_code, 'name' : stock_name, 'qty' : stock_qty})
        if stock_code == code:
            return stock_name, stock_qty
    if code == 'ALL':
        return stocks
    else:
        stock_name = cpCodeMgr.CodeToName(code)
        return stock_name, 0

def get_current_cash():
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]      #계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1) #-1:전체, 1:주식, 2:선물/옵션
    cpCash.SetInputValue(0, acc)            #계좌번호
    cpCash.SetInputValue(1, accFlag[0])     #상품구분 - 주식 상품 중 첫 번째
    cpCash.BlockRequest()

    return cpCash.GetHeaderValue(9)         #증거금 100% 주문 가능 금액

print(get_current_cash())
