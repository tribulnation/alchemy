# Paginate Through Results

Some Alchemy endpoints return page cursors. Pass the returned cursor into the
next request to continue.

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  first_page = await client.transfers('ethereum').get_asset_transfers({
    'fromBlock': '0x0',
    'toAddress': '0x5c43B1eD97e52d009611D89b74fA829FE4ac56b1',
    'category': ['external'],
    'maxCount': '0x2',
  })
  print(first_page)
```

`client.transfers('ethereum').get_asset_transfers_paged(...)` returns an async
iterable of transfer chunks:

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  pages = client.transfers('ethereum').get_asset_transfers_paged({
    'fromBlock': '0x0',
    'toAddress': '0x5c43B1eD97e52d009611D89b74fA829FE4ac56b1',
    'category': ['external'],
    'maxCount': '0x2',
  })
  async for transfers in pages:
    print(transfers)
```

You can also await a paginated response to flatten all pages into one list:

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  transfers = await client.transfers('ethereum').get_asset_transfers_paged({
    'fromBlock': '0x0',
    'toAddress': '0x5c43B1eD97e52d009611D89b74fA829FE4ac56b1',
    'category': ['external'],
    'maxCount': '0x2',
  })
  print(transfers)
```

Portfolio endpoints expose `.paged(...)` on the endpoint object:

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  pages = client.portfolio.tokens.paged({
    'addresses': [
      {
        'address': '0x1E6E8695FAb3Eb382534915eA8d7Cc1D1994B152',
        'networks': ['eth-mainnet'],
      }
    ],
    'pageSize': 10,
  })
  async for tokens in pages:
    print(tokens)
```

NFT and token helpers follow the one-page method name:

```python
from alchemy import Alchemy

async with Alchemy.new() as client:
  nfts = await client.nft('ethereum').get_nfts_for_owner_paged(
    owner='vitalik.eth',
    page_size=10,
  )
  balances = await client.token('ethereum').get_token_balances_paged([
    '0x1E6E8695FAb3Eb382534915eA8d7Cc1D1994B152',
    'erc20',
    {'maxCount': 10},
  ])
```
