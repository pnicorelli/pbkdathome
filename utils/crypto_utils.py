from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip44, Bip44Coins, Bip44Changes,
    Bip84, Bip84Coins
)
from typing import Tuple, List

class CryptoUtils:
    @staticmethod
    def validate_mnemonic(mnemonic: str) -> bool:
        return Bip39MnemonicValidator().IsValid(mnemonic)
    
    @staticmethod
    def generate_seed(mnemonic: str) -> bytes:
        return Bip39SeedGenerator(mnemonic).Generate()
    
    @staticmethod
    def get_bip44_addresses(seed_bytes: bytes, coin: str, wallets: int) -> Tuple[str, List[dict]]:
        try:
            coin_type = getattr(Bip44Coins, coin.upper())
            bip44_obj = Bip44.FromSeed(seed_bytes, coin_type)
            
            addresses = []
            for i in range(wallets):
                bip44_addr = bip44_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
                addresses.append({
                    'index': i,
                    'address': bip44_addr.PublicKey().ToAddress(),
                    'private_key': bip44_addr.PrivateKey().Raw().ToHex()
                })
            return None, addresses
        except AttributeError:
            return f'Coin not supported: {coin}', None
        except Exception as e:
            return str(e), None

    @staticmethod
    def get_bip84_addresses(seed_bytes: bytes, coin: str, wallets: int) -> Tuple[str, List[dict]]:
        try:
            coin_type = getattr(Bip84Coins, coin.upper())
            bip84_obj = Bip84.FromSeed(seed_bytes, coin_type)
            
            addresses = []
            for i in range(wallets):
                bip84_addr = bip84_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
                addresses.append({
                    'index': i,
                    'address': bip84_addr.PublicKey().ToAddress(),
                    'private_key': bip84_addr.PrivateKey().Raw().ToHex()
                })
            return None, addresses
        except AttributeError:
            return f'Coin not supported: {coin}', None
        except Exception as e:
            return str(e), None
