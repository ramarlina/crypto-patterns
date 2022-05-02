#!/usr/bin/env python
# coding: utf-8

# Imports

# In[7]:


from web3.auto import w3
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_structured_data
import json 
from eth_account._utils.structured_data.hashing import hash_domain

web3 = Web3(Web3.HTTPProvider("https://data-seed-prebsc-1-s1.binance.org:8545/"))


# Signer account

# In[9]:


private_key = w3.sha3(text="random")
signer_address = Account.from_key(private_key).address


# Sample transaction data we'd like to sign

# In[2]:


contract_address = '0x833Bcee325Cb66406452f63432959E899aEE01d8'
abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"typeHash","type":"bytes32"},{"indexed":false,"internalType":"string","name":"typeStr","type":"string"}],"name":"RequestTypeRegistered","type":"event"},{"inputs":[],"name":"GENERIC_PARAMS","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"}],"name":"_getEncoded","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"execute","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"ret","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"}],"name":"getNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"recoverAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"typeName","type":"string"},{"internalType":"string","name":"typeSuffix","type":"string"}],"name":"registerRequestType","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"typeHashes","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gas","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IForwarder.ForwardRequest","name":"req","type":"tuple"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"bytes32","name":"requestTypeHash","type":"bytes32"},{"internalType":"bytes","name":"suffixData","type":"bytes"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"verify","outputs":[],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')

verifierContract = web3.eth.contract(abi=abi, address=contract_address)

domain_name = "Test" 
domain_chainId = 97

tx = {
    'primaryType': 'ForwardRequest', 
    'types': {'EIP712Domain': [{'name': 'name', 'type': 'string'}, {'name': 'version', 'type': 'string'}, {'name': 'chainId', 'type': 'uint256'}, {'name': 'verifyingContract', 'type': 'address'}], 
              'ForwardRequest': [{'name': 'from', 'type': 'address'}, {'name': 'to', 'type': 'address'}, {'name': 'value', 'type': 'uint256'}, {'name': 'gas', 'type': 'uint256'}, {'name': 'nonce', 'type': 'uint256'}, {'name': 'data', 'type': 'bytes'}]}, 'domain': {'name': domain_name, 'version': '1', 'chainId': domain_chainId, 'verifyingContract': contract_address}, 
    'message': {'from': '0x9fdA2cCe1566D220403442C90eC3260c6642D672', 'to': '0x23d96F7Fdd50495Ec78B54199F156fe2F2C58d57', 'value': 0, 'gas': 1000000, 'nonce': 3, 'data': '0xa9059cbb000000000000000000000000911a0ee2dbf4e552fd08ef5534c2635d578cc650000000000000000000000000000000000000000000000000Ab043Eb3a7650000'}
}


# Web3py: **encode_structured_data** throws as type error because it expects the value of `data` to be of type `bytes`

# In[3]:


try:
    encoded_data=encode_structured_data(tx)
except TypeError as e: 
    print(e.__str__()) 


# In[4]:


# convert string to bytes
if isinstance(tx["message"]["data"], str):
    tx["message"]["data"] = tx["message"]["data"].encode("utf8")

encoded_data = encode_structured_data(tx)
signature = w3.eth.account.sign_message(encoded_data, private_key).signature.hex()
signature


# In[11]:


type_hash = w3.keccak(text='ForwardRequest(address from,address to,uint256 value,uint256 gas,uint256 nonce,bytes data)').hex()
domain_hash = hash_domain(tx).hex()  

recoveredAddress = verifierContract.functions.recoverAddress(tx["message"], domain_hash, type_hash, '0x', signature).call()


# In[12]:


print(f"Signer Address: {signer_address}\nRecovered Address from Signature: {recoveredAddress}")


# In[ ]:




