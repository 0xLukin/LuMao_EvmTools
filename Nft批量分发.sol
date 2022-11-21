// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract NftMatch {
    IERC721 nft;

    constructor() {}

    function matchNft(
        address _nftAddress,
        address[] _add,
        uint[] _id
    ) returns () {
        nft = IERC721(_nftAddress);
        for (uint i = 0; i < _add.length; i++) {
            if (_add[i] != address(0) || _id[i] != 0) {
              nft.transferFrom(msg.sender, _add[i], _id[i])
            }
        }
    }
}
