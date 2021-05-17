import yfinance as yf
msft = yf.Ticker("MSFT")
hist = msft.history(period="1y")
print((hist["Close"]))
print(hist)
print(hist.columns)
print(list(hist.index))
print(list(hist["Close"]))
print(hist[["Close"]].values.tolist())
