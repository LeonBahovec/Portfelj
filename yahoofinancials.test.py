from yahoofinancials import YahooFinancials
apple = YahooFinancials("AAPL")
print(apple.get_current_price())