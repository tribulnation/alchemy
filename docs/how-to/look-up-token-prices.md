# Look Up Token Prices

Use `client.prices` for Alchemy Prices API methods. These methods are global
and do not take a network selector.

## Current Prices By Symbol

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  prices = await client.prices.by_symbol(symbols=['ETH', 'BTC'])
  print(prices['data'])
```

## Current Prices By Contract

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  prices = await client.prices.by_address({
    'addresses': [
      {
        'network': 'eth-mainnet',
        'address': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
      }
    ],
  })
  print(prices['data'])
```

## Historical Prices

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  history = await client.prices.historical({
    'symbol': 'ETH',
    'startTime': 1746748800,
    'endTime': 1747008000,
    'interval': '1d',
  })
  print(history['data'])
```
