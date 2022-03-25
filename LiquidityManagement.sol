// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

interface LPFactory { 
    function createPair(address tokenA, address tokenB) external returns (address pair);
    function getPair(address tokenA, address tokenB) external view returns (address pair);
}

interface LPRouter { 
    function addLiquidity(
        address tokenA,
        address tokenB,
        uint amountADesired,
        uint amountBDesired,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB, uint liquidity);
}

interface IERC20 { 
    function approve(address spender, uint256 amount) external returns (bool); 
    function allowance(address owner, address spender) external view returns (uint256);
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool); 
}

contract LiquidityManagement is Ownable {

    LPRouter public router;
    LPFactory public factory;

    address public factoryAddress;
    address public routerAddress;
    address public pairAddress;

    address public tokenAAddress;
    address public tokenBAddress;

    IERC20 public tokenA;
    IERC20 public tokenB;

    constructor(
        address _tokenAAddress, 
        address _tokenBAddress,
        address _factoryAddress,  // Factory: 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f for uniswapv2 
        address _routerAddress    // Router: 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D for uniswapv2
     ){ 
   
        updatePair(_tokenAAddress, _tokenBAddress);
        updateDex(_factoryAddress, _routerAddress); 

    }
 
    function updatePair(address _tokenAAddress, address _tokenBAddress) public onlyOwner {
        tokenAAddress = _tokenAAddress; 
        tokenBAddress = _tokenBAddress;

        tokenA = IERC20(tokenAAddress);
        tokenB = IERC20(tokenBAddress);

        if ((factoryAddress != address(0)) && (routerAddress != address(0))){
            setDexAddresses(factoryAddress, routerAddress);
        } 
    }

    function updateDex(address _factoryAddress, address _routerAddress) public onlyOwner { 
        factoryAddress = _factoryAddress;
        routerAddress = _routerAddress;

        factory = LPFactory(factoryAddress);

        pairAddress = factory.getPair(tokenAAddress, tokenBAddress);

        // if pair does not exist yet, create it
        if (pairAddress == address(0)){
            pairAddress = factory.createPair(tokenAAddress, tokenBAddress);
        }
 
        // router
        router = LPRouter(routerAddress); 

        tokenA.approve(routerAddress, type(uint256).max);
        tokenB.approve(routerAddress, type(uint256).max); 
    } 
    
    function addLiquidity(uint amountTokenA, uint amountTokenB) public payable returns (bool){ 

        require(tokenA.allowance(msg.sender, address(this)) > amountTokenA, "Not enough allowance for tokenA");
        require(tokenB.allowance(msg.sender, address(this)) > amountTokenB, "Not enough allowance for tokenB");
        
        require(tokenA.transferFrom(msg.sender, address(this), amountTokenA), "Transfer failed for token A"); 
        require(tokenB.transferFrom(msg.sender, address(this), amountTokenB), "Transfer failed for token B");  

        router.addLiquidity(
            tokenAAddress,
            tokenBAddress,
            amountTokenA,
            amountTokenB,
            0,
            0,
            msg.sender,
            block.timestamp
        );
        return true; 
    } 
}
