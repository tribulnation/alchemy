# Typed Alchemy

> A fully typed, validated async client for the Alchemy API.

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  prices = await client.prices.by_symbol(symbols=['ETH', 'BTC'])
  transfers = await client.transfers('ethereum').get_asset_transfers({
    'fromBlock': '0x0',
    'toAddress': '0x5c43B1eD97e52d009611D89b74fA829FE4ac56b1',
    'category': ['external'],
    'maxCount': '0x2',
  })
```

## Why Typed Alchemy?

- **🎯 Precise Types**: Typed endpoint inputs and responses.
- **✅ Runtime Validation**: Validated responses by default.
- **⚡ Async First**: Built for concurrent HTTP workflows.
- **📚 Full API Surface**: `client.portfolio`, `client.prices`, `client.nft('ethereum')`, etc.

## Installation

```bash
pip install typed-alchemy
```

## How To

- [API Keys Setup](api-keys.md)
- [Look Up Token Prices](how-to/look-up-token-prices.md)
- [Inspect Wallet Portfolio](how-to/inspect-wallet-portfolio.md)
- [Query NFTs](how-to/query-nfts.md)
- [Get Asset Transfers](how-to/get-asset-transfers.md)
- [Paginate Through Results](how-to/paginate-through-results.md)

## Reference

- [Error Handling](reference/error-handling.md)
- [Environment Variables](reference/env-vars.md)
- [Generated API Reference](reference/api/index.md)
