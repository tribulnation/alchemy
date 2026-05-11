# API Overview

This page explains the Typed Alchemy client structure.

## Design

Typed Alchemy organizes endpoints by Alchemy API surface rather than by raw URL
path. That keeps the surface discoverable in an IDE and matches how Alchemy
documents the Data APIs.

A typical shape looks like this:

```python
client.<group>.<method>(...)
client.<network_group>('ethereum').<method>(...)
```

Examples:

1. `client.prices.by_symbol(...)`
2. `client.portfolio.token_balances(...)`
3. `client.nft('ethereum').get_nfts_for_owner(...)`
4. `client.token('ethereum').get_token_metadata(...)`
5. `client.transfers('ethereum').get_asset_transfers(...)`
6. `client.utility('ethereum').get_transaction_receipts(...)`
7. `client.simulation('ethereum').asset_changes(...)`

## Coverage

Current spec and client coverage is 41 Alchemy Data API endpoints:

1. Portfolio REST: 5 endpoints.
2. Prices REST: 3 endpoints.
3. NFT REST v3: 24 endpoints.
4. Transfers JSON-RPC: 1 endpoint.
5. Token JSON-RPC: 3 endpoints.
6. Utility JSON-RPC: 1 endpoint.
7. Simulation JSON-RPC: 4 endpoints.

## Validation

By default, responses are validated into typed Python structures. Pass
`validate=False` on the client or on a single method call to skip validation.

## Public vs Authenticated Endpoints

All Alchemy endpoints in this client require an API key. Pass `api_key=` or set
`ALCHEMY_API_KEY`.

## Generated Reference

The complete endpoint reference belongs under [Reference > API](reference/api/index.md).

That section is generated from the implementation so it stays aligned with the
real client surface.
