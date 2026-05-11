# Typed Alchemy

Typed Alchemy is an async, typed, runtime-validated Python client for Alchemy
Data APIs.

```bash
pip install typed-alchemy
```

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  prices = await client.prices.by_symbol(symbols=['ETH', 'BTC'])
```

Set `ALCHEMY_API_KEY` in your environment, or pass `api_key=` to the
constructor.

Documentation: https://alchemy.tribulnation.com
Repository: https://github.com/tribulnation/alchemy
