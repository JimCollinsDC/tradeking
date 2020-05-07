from flask import Flask
from flask import render_template
from models.tradeking import TradeKingAPI
from markupsafe import escape
import os
"""
https://github.com/public-apis/public-apis/blob/145ea881b2b15034d7207f7f7b6a781994fbb574/README.md#cryptocurrency
https://domainsdb.info/
https://api.domainsdb.info/v1/domains/search?domain=facebook
https://api.coindesk.com/v1/bpi/currentprice/usd.json
"""

"""
use json.loads
use add_url_rule()
use relative paths
"""
# from python-dotenv import load_dotenv
# load_dotenv()


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/test')
def testoauth():
    mykey = os.environ.get("TK_CONSUMER_KEY")
    return 'my key: ' + mykey


@app.route('/testdata')
def display_testdata():
    tk = TradeKingAPI()
    btcdata = tk.accounts()
    return btcdata.json()
    # btcdata.text


@app.route('/data')
def display_data():
    tk = TradeKingAPI()
    btc_data = tk.accounts()
    return render_template('DisplayBTCData.html', btcdata=btc_data)


@app.route('/clock')
def display_clock():
    tk = TradeKingAPI()
    clock_data = tk.market_clock()
    return render_template('DisplayBTCData.html', btcdata=clock_data)


@app.route('/quote/<symb>')
def display_quote(symb):
    print('symb: ', symb, flush=True)
    print('symb: ', escape(symb), flush=True)
    tk = TradeKingAPI()
    ext_quotes_data = tk.market_ext_quotes(escape(symb),)
    return render_template('DisplayBTCData.html', btcdata=ext_quotes_data.json())


@app.route('/options/<sym>')
def display_options(sym):
    tk = TradeKingAPI()
    fids = 'ask,bid,vol,strikeprice'
    options_data = tk.market_options_search(symbol=sym, fids=fids)
    print('options url: ', options_data.url)
    return render_template('DisplayBTCData.html', btcdata=options_data.json())


@app.route('/options_strikes/<sym>')
def display_options_strikes(sym):
    tk = TradeKingAPI()
    fids='ask,bid,vol,strikeprice'
    options_strikes = tk.market_options_strikes(symbol=sym)
    print('options_strikes url: ', options_strikes.url)
    return render_template('DisplayBTCData.html', btcdata=options_strikes.json())


@app.route('/options_expire/<sym>')
def display_options_expirations(sym):
    tk = TradeKingAPI()
    options_expire = tk.market_options_expirations(sym)
    return render_template('DisplayBTCData.html', btcdata=options_expire)


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
