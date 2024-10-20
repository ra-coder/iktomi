// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

// Импортируем необходимую библиотеку OpenZeppelin для ERC721
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Itkomi is ERC721 {
    uint private _tokenIdCounter;

    // Мета-данные для токена (например, URL изображения)
    mapping (uint => string) private _tokenURIs;
    mapping (uint => bool) public valid; 

    constructor() ERC721("iktomi-diplomas-template", "DIPLOMAS_TMPL") {}

    modifier checkDiplomas(uint tokenId) {
        require(tokenId <= _tokenIdCounter, "invalid diplomas");
        _;
    }

    // Функция для создания нового NFT
    function mint(address to, string memory _tokenURI) public {
        uint256 tokenId = _tokenIdCounter;
        _mint(to, tokenId); 
        _tokenURIs[tokenId] = _tokenURI; 
        valid[tokenId] = true;
        _tokenIdCounter += 1; 
    }

    // Функция для получения мета-данных токена
    function tokenURI(uint256 tokenId) checkDiplomas(tokenId) public view override returns (string memory) {
        return _tokenURIs[tokenId];
    }

    function revoked(uint _tokenId) checkDiplomas(_tokenId) public {
        require(valid[_tokenId] == true, "diplomas already revoked");
        valid[_tokenId] = false;
    }
}
