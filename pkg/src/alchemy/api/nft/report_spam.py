from alchemy.core import Endpoint, validator

adapter = validator(str)

class ReportSpam(Endpoint):
  async def report_spam(
    self,
    *,
    address: str,
    is_spam: bool,
    validate: bool | None = None
  ) -> str:
    """Reports a contract address as spam to Alchemy's spam classification system.
    
    Args:
      address: Contract address to report.
      is_spam: Whether to mark the address as spam (true) or clear the spam flag (false).
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-spam-endpoints/report-spam-v-3)
      """
    params: dict = {
      'address': address,
      'isSpam': is_spam,
    }
    r = await self.request('GET', '/reportSpam', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
