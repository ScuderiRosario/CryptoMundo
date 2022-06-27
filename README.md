# CryptoMundo
CryptoMundo is a simple and easy tool to analyze cryptocurrency data in real time which provides a simple and informative dashboard.

Every 3 minutes CryptoMundo updates the data of the top 10 cryptocurrencies, enriching them with addinional information (e.g. information about whhat people think on twitter and price forecasts). At each cycle the system creates (and **updates**) a linear regression model **constantly updated** with data from the last 360 days.

# How it work?

![progettotap](https://user-images.githubusercontent.com/105871424/176013226-73938bf9-0047-4823-b590-ea8b4ace62f1.jpg)

### Data Source and API
  - [Coingecko](https://pypi.org/project/pycoingecko/) ---> Extract live info about cryptocurrencies
  - [Twitter](https://pypi.org/project/snscrape/) ---> Extract tweet about top 10 cryptocurrencies
  - [Yahoo! Finance](https://pypi.org/project/yfinance/) ---> Extract historical data
  - 
### Tools
  - **Apache Spark** ---> for fast machine learning
  - **Apache Kafka** ---> to pass data from one party to another
  - **ELK Stack** ---> to create the dashboard

