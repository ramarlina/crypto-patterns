# Signing EIP-712 data using Web3py with opengsn's Forwarder Contract


## Meta-transactions AKA gasless transactions:
Meta-transactions is a concept that allows one user to send a transaction on behalf of another user, and pay themselves for the gas cost.

More on meta-transactions:
* https://docs.openzeppelin.com/learn/sending-gasless-transactions
* https://betterprogramming.pub/ethereum-erc-20-meta-transactions-4cacbb3630ee

One important step in using meta-transactions is verifying signature, making sure the user that initiated the transaction ('from') is the signer of the message.


## Dependencies:
* Web3 in Python: https://github.com/ethereum/web3.py
* OpenGSN's sample Forwarder contract: https://github.com/opengsn/forwarder


## TLDR;
Call **encode_structured_data**, then sign output using **w3.eth.account.sign_message**.


One caveat being, you want to convert bytes abi parameters to bytes in python first:

```python
tx["message"]["data"] = tx["message"]["data"].encode("utf8") 
```

Then do:

```python
encoded_data = encode_structured_data(tx)
signature = w3.eth.account.sign_message(encoded_data, private_key).signature.hex()
```

# Demonstration

Imports


```python
from web3.auto import w3
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_structured_data
import json 
from eth_account._utils.structured_data.hashing import hash_domain

# bsc testnet
web3 = Web3(Web3.HTTPProvider("https://data-seed-prebsc-1-s1.binance.org:8545/"))
```

Pointing to the forwarder contract deployed on testnet


```python
contract_address = '0x833Bcee325Cb66406452f63432959E899aEE01d8'
abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"typeHash","type":"bytes32"},{"indexed":false,"internalType":"string","name":"typeStr","type":"string"}],"name":"RequestTypeRegistered","type":"event"},{"inputs":[],"name":"GENERIC_PARAMS","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"}],"name":"_getEncoded","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"execute","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"ret","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"}],"name":"getNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"recoverAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"typeName","type":"string"},{"internalType":"string","name":"typeSuffix","type":"string"}],"name":"registerRequestType","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"typeHashes","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"verify","outputs":[],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')

verifierContract = web3.eth.contract(abi=abi, address=contract_address)
```

Let's use some random private key to sign the message:


```python
private_key = w3.sha3(text="random")
signer_address = Account.from_key(private_key).address 
```

Let's create the message we'd like to sign:


```python
domain_name = "Test" 
domain_chainId = 97

tx = {
    'primaryType': 'ForwardRequest', 
    'types': {'EIP712Domain': [{'name': 'name', 'type': 'string'}, {'name': 'version', 'type': 'string'}, {'name': 'chainId', 'type': 'uint256'}, {'name': 'verifyingContract', 'type': 'address'}], 
              'ForwardRequest': [{'name': 'from', 'type': 'address'}, {'name': 'to', 'type': 'address'}, {'name': 'value', 'type': 'uint256'}, {'name': 'gas', 'type': 'uint256'}, {'name': 'nonce', 'type': 'uint256'}, {'name': 'data', 'type': 'bytes'}]}, 'domain': {'name': domain_name, 'version': '1', 'chainId': domain_chainId, 'verifyingContract': contract_address}, 
    'message': {'from': '0x9fdA2cCe1566D220403442C90eC3260c6642D672', 'to': '0x23d96F7Fdd50495Ec78B54199F156fe2F2C58d57', 'value': 0, 'gas': 1000000, 'nonce': 3, 'data': '0xa9059cbb000000000000000000000000911a0ee2dbf4e552fd08ef5534c2635d578cc650000000000000000000000000000000000000000000000000Ab043Eb3a7650000'}
}
```

**encode_structured_data** will throw an error because it expects the value of `data` to be of type `bytes`


```python
try:
    encoded_data=encode_structured_data(tx)
except TypeError as e: 
    print(e.__str__()) 
```

We need to convert string to bytes in Python


```python
if isinstance(tx["message"]["data"], str):
    tx["message"]["data"] = tx["message"]["data"].encode("utf8")
```

Sigin the message now works:


```python
encoded_data = encode_structured_data(tx)
signature = w3.eth.account.sign_message(encoded_data, private_key).signature.hex()
signature
```

## Test with a deployed contract on BSC testnet


```python
type_hash = w3.keccak(text='ForwardRequest(address from,address to,uint256 value,uint256 gas,uint256 nonce,bytes data)').hex()
domain_hash = hash_domain(tx).hex()  

recovered_address = verifierContract.functions.recoverAddress(tx["message"], domain_hash, type_hash, '0x', signature).call()
```


```python
print(f"Signer Address: {signer_address}\nRecovered Address from Signature: {recovered_address}")
```

# Executing payload in Solidity

To submit the transaction to the blockchain, all you need to do is execute the "call" function in solidity:


```python
req.call{gas : req.gas, value : req.value}(abi.encodePacked(req.data, req.from));
```
