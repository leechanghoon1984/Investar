import win32com.client

cpStock = win32com.client.Dispatch("DsCbo1.StockMst")

def get_current_price(code):
    cpStock.SetInputValue(0, code)
    cpStock.BlockRequest()

    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11)
    item['ask'] = cpStock.GetHeaderValue(16)
    item['bid'] = cpStock.GetHeaderValue(17)

    return item['cur_price'], item['ask'], item['bid']

print(get_current_price('A305080'))
