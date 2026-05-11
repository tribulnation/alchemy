<p align="center">
  <a href="https://alchemy.tribulnation.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tribulnation/alchemy/refs/heads/main/media/alchemy-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tribulnation/alchemy/refs/heads/main/media/alchemy-light.svg">
      <img alt="Typed Alchemy" src="https://raw.githubusercontent.com/tribulnation/alchemy/refs/heads/main/media/alchemy-light.svg" width="520">
    </picture>
  </a>
</p>

<p align="center">
  <em>A fully typed, validated async client for the Alchemy API.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/typed-alchemy/">
    <img src="https://img.shields.io/pypi/v/typed-alchemy.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/typed-alchemy/">
    <img src="https://img.shields.io/pypi/pyversions/typed-alchemy.svg" alt="Python versions">
  </a>
  <a href="https://alchemy.tribulnation.com/">
    <img src="https://img.shields.io/badge/docs-live-black" alt="Docs">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/pypi/l/typed-alchemy.svg" alt="License">
  </a>
</p>

---

- **Documentation**: [https://alchemy.tribulnation.com](https://alchemy.tribulnation.com)
- **Source Code**: [https://github.com/tribulnation/alchemy](https://github.com/tribulnation/alchemy)

---

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
- **📚 Full API Surface**: `client.portfolio`, `client.prices`, and
  network-scoped groups like `client.nft('ethereum')`.

## Installation

```bash
pip install typed-alchemy
```

## How To

- [API Keys Setup](https://alchemy.tribulnation.com/api-keys/)
- [Look Up Token Prices](https://alchemy.tribulnation.com/how-to/look-up-token-prices/)
- [Inspect Wallet Portfolio](https://alchemy.tribulnation.com/how-to/inspect-wallet-portfolio/)
- [Query NFTs](https://alchemy.tribulnation.com/how-to/query-nfts/)
- [Get Asset Transfers](https://alchemy.tribulnation.com/how-to/get-asset-transfers/)
- [Paginate Through Results](https://alchemy.tribulnation.com/how-to/paginate-through-results/)

## Reference

- [Error Handling](https://alchemy.tribulnation.com/reference/error-handling/)
- [Environment Variables](https://alchemy.tribulnation.com/reference/env-vars/)
- [Generated API Reference](https://alchemy.tribulnation.com/reference/api/)
