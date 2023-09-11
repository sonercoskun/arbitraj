from binance.client import Client
import time

api_key = 
api_secret = 

def calculate_arbitrage(client, anapara, odenecek_komisyon):
    pairs = {
        'FTMBUSD': {'min_amount': 100.0},
        'FTMTRY': {'min_amount': 100.0},
        'BUSDTRY': {'min_amount': 100.0}
    }

    ticker_ftm_busd = float(client.get_symbol_ticker(symbol='FTMBUSD')['price'])
    ticker_ftm_try = float(client.get_symbol_ticker(symbol='FTMTRY')['price'])
    ticker_busd_try = float(client.get_symbol_ticker(symbol='BUSDTRY')['price'])
    ftm_busd = float(client.get_symbol_ticker(symbol='FTMBUSD')['price'])

    calculated_ftm_busd = ticker_ftm_try / ticker_busd_try
    coin_miktarı = anapara * ticker_busd_try
    islem_kosulu = (ftm_busd - calculated_ftm_busd) * coin_miktarı > odenecek_komisyon

        # Değerleri print et
    #print("ftm/busd", ftm_busd)
    #print("ftm/try", ticker_ftm_try)
    #print("busd/try", ticker_busd_try)
    print("cftm/busd", calculated_ftm_busd)
    print("işlem koşulu", ftm_busd - calculated_ftm_busd)

    if ftm_busd < calculated_ftm_busd and (ftm_busd - calculated_ftm_busd) * coin_miktarı > odenecek_komisyon:
        ftm_amount = min(pairs['FTMBUSD']['min_amount'], pairs['FTMTRY']['min_amount'] / ticker_ftm_try)
        if ftm_amount > 0:
            buy_order = client.create_order(
                symbol='FTMBUSD',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=ftm_amount,
                price=ftm_busd
            )
            ftm_busd_amount = float(buy_order['executedQty'])
            sell_order = client.create_order(
                symbol='FTMTRY',
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=ftm_busd_amount,
                price=ticker_ftm_try
            )
            ftm_try_amount = float(sell_order['executedQty'])

            busd_amount = ftm_try_amount * ticker_busd_try
            busd_order = client.create_order(
                symbol='BUSDTRY',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=busd_amount,
                price=ticker_busd_try
            )

            print("Arbitraj1 işlemi gerçekleştirildi.")

    elif ftm_busd > calculated_ftm_busd and (ftm_busd - calculated_ftm_busd) * coin_miktarı > odenecek_komisyon:
        ftm_try_amount = min(pairs['FTMTRY']['min_amount'], pairs['FTMBUSD']['min_amount'] / ftm_busd)
        if ftm_try_amount > 0:
            buy_order = client.create_order(
                symbol='FTMTRY',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=ftm_try_amount,
                price=ticker_ftm_try
            )
            ftm_try_amount = float(buy_order['executedQty'])
            sell_order = client.create_order(
                symbol='FTMBUSD',
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=ftm_try_amount,
                price=ftm_busd
            )
            ftm_busd_amount = float(sell_order['executedQty'])
            busd_amount = ftm_busd_amount * ticker_busd_try
            busd_order = client.create_order(
                symbol='BUSDTRY',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=busd_amount,
                price=ticker_busd_try
            )

            print("Arbitraj2 işlemi gerçekleştirildi.")

    else:
        print("Arbitraj fırsatı bulunmamaktadır.")

client = Client(api_key, api_secret)
anapara = 100
odenecek_komisyon = 0.2
timeout_seconds = 1  
last_order_time = time.time()  

while True:
    current_time = time.time()
    elapsed_time = current_time - last_order_time

    if elapsed_time >= timeout_seconds:
        calculate_arbitrage(client, anapara, odenecek_komisyon)
        last_order_time = current_time

    time.sleep(0.1)
