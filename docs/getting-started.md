# Getting Started

This guide gets you from installation to your first Alchemy Data API requests.

## Install The Package

```bash
pip install typed-alchemy
```

## Configure Credentials

Typed Alchemy uses an Alchemy API key for every endpoint.

```bash
export ALCHEMY_API_KEY="your_api_key"
```

## Make A Request

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  prices = await client.prices.by_symbol(symbols=['ETH', 'BTC'])
  print(prices)
```

## Use JSON-RPC Endpoints

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  metadata = await client.token('ethereum').get_token_metadata(
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
  )
  print(metadata)
```

## Context Manager Pattern

The client is designed to be used with `async with` so connections and sessions are opened and closed cleanly:

```python
async with Alchemy.new() as client:
  ...
```

## Next Steps

- Go to [API Keys Setup](api-keys.md) if you have not configured credentials yet
- Read [API Overview](api-overview.md) to understand the client structure
- Browse [How To](how-to/index.md) for common workflows
