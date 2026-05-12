from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

TokenSpec = Literal['erc20', 'NATIVE_TOKEN', 'DEFAULT_TOKENS'] | list[str]

class TokenBalancesOptions(TypedDict):
  """Pagination options."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""
  maxCount: NotRequired[int]
  """Maximum number of token balances to return. Capped at 100."""

class TokenBalance(TypedDict):
  contractAddress: str
  """Token contract address."""
  tokenBalance: str | None
  """Hex-encoded token balance, or null if an error occurred fetching this token."""

class TokenBalancesResponse(TypedDict):
  address: str
  """The queried wallet address."""
  tokenBalances: list[TokenBalance]
  """List of token balances for the wallet."""
  pageKey: NotRequired[str]
  """Pagination cursor for retrieving the next page of balances. Present only when more results exist."""

adapter = validator(TokenBalancesResponse)

class GetTokenBalances(Endpoint):
  async def get_token_balances(
    self,
    address: str,
    token_spec: TokenSpec = 'erc20',
    *,
    options: TokenBalancesOptions | None = None,
    validate: bool | None = None
  ) -> TokenBalancesResponse:
    """Returns ERC-20 token balances (or native token balance) for a wallet address via the `alchemy_getTokenBalances` JSON-RPC method.

    Args:
      address: Wallet address to inspect.
      token_spec: Token selection: all ERC-20 tokens, native token, default tokens, or explicit contract addresses.
      options: Pagination options.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/token-api/token-api-endpoints/alchemy-get-token-balances)
      """
    params = [address, token_spec]
    if options is not None:
      params.append(options)
    r = await self.rpc_request('alchemy_getTokenBalances', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
