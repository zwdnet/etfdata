import backtrader as bt

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    print(cerebro.broker.getvalue())
    cerebro.run()
    print(cerebro.broker.getvalue())
    