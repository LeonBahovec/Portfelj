from yahoofinancials import YahooFinancials
apple = YahooFinancials("KRK.WA")
print(apple.get_current_price())
print(apple.get_stock_quote_type_data()["KRK.WA"]["shortName"])
print(apple.get_stock_quote_type_data()["KRK.WA"]["longName"])