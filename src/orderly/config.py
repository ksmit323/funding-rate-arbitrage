class Config(object):
    def __init__(
        self,
        base_url="https://testnet-api-evm.orderly.org",
        broker_id="woofi_pro",
        chain_id=421614,  # Arbitrum Sepolia
    ) -> None:
        self.base_url = base_url
        self.broker_id = broker_id
        self.chain_id = chain_id
