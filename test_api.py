from services.mercado_bitcoin import MercadoBitcoin

mb = MercadoBitcoin()

j = mb.chamar_api_mercado_bitcoin('BRLBTC', 1, 1577836800, 1606565306)

print(j['candles'])