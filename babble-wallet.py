#!/usr/bin/env python3
"""
Babble Wallet – An experimental Bitcoin wallet that uses the first 12 words you ever spoke as your seed phrase.

WARNING: This wallet is experimental.
         Using your first 12 words as a seed phrase is likely insecure if those words are common or known.
         Do NOT use this wallet for holding significant funds.

MIT License
"""

import sys
from mnemonic import Mnemonic
import bip32utils

def main():
    print("====================================")
    print("   Welcome to Babble Wallet")
    print("====================================")
    print("This wallet uses your first 12 words spoken as your seed phrase.")
    print("WARNING: This method is experimental and may not be secure.\n")

    # Prompt the user for their 12-word phrase.
    seed_phrase_input = input("Enter the first 12 words you ever spoke (separated by spaces): ").strip()
    words = seed_phrase_input.split()
    if len(words) != 12:
        print("Error: You must enter exactly 12 words.")
        sys.exit(1)

    # Join the words back into a mnemonic string.
    seed_phrase = " ".join(words)

    # Initialize the BIP39 mnemonic helper
    mnemo = Mnemonic("english")

    # Check if the mnemonic passes the BIP39 checksum.
    if not mnemo.check(seed_phrase):
        print("\nWARNING: The provided 12-word phrase does not pass the standard BIP39 checksum test.")
        print("Proceeding anyway. (This may affect wallet determinism and compatibility.)\n")

    # Generate the binary seed (using an empty passphrase).
    seed = mnemo.to_seed(seed_phrase, passphrase="")

    # Create the BIP32 master key from the seed.
    root_key = bip32utils.BIP32Key.fromEntropy(seed)

    # Derive keys along the BIP44 path for Bitcoin: m/44'/0'/0'/0/0
    try:
        purpose_key   = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN)  # m/44'
        coin_type_key = purpose_key.ChildKey(0 + bip32utils.BIP32_HARDEN)  # m/44'/0'
        account_key   = coin_type_key.ChildKey(0 + bip32utils.BIP32_HARDEN)  # m/44'/0'/0'
        change_key    = account_key.ChildKey(0)                            # m/44'/0'/0'/0
        address_key   = change_key.ChildKey(0)                             # m/44'/0'/0'/0/0
    except Exception as e:
        print("Error during key derivation:", str(e))
        sys.exit(1)

    # Get the Bitcoin address and the private key in Wallet Import Format (WIF).
    btc_address = address_key.Address()
    private_key_wif = address_key.WalletImportFormat()

    # Display the wallet details.
    print("\n====================================")
    print("       Your Babble Wallet")
    print("====================================")
    print(f"Seed Phrase (your first 12 words):\n  {seed_phrase}\n")
    print(f"Bitcoin Receiving Address:\n  {btc_address}\n")
    print(f"Private Key (WIF format):\n  {private_key_wif}\n")
    print("====================================")
    print("IMPORTANT: Keep your private key secret!")
    print("           Anyone with access to it can control your funds.\n")
    print("This wallet is experimental. Do not use it for significant amounts of Bitcoin.")
    
if __name__ == "__main__":
    main()
