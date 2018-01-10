pragma solidity ^0.4.19;

import "./Curve.sol"

// https://gist.github.com/ryanxcharles/1c0f95d0892b4a92d70a
// http://www.nicolascourtois.com/bitcoin/paycoin_privacy_monero_6_ICISSP17.pdf
library Stealth
{
    function PubDerive (uint256[2] pubkey, bytes32 nonce)
        public constant
        returns (uint256[2])
    {
        Curve.G1Point memory spk = Curve.g1add(Curve.G1Point(pubkey[0], pubkey[1]), Curve.g1mul(Curve.P1(), uint256(nonce)));
        return [spk.X, spk.Y];
    }
    
    function PrivDerive (bytes32 secret_key, bytes32 nonce)
        public pure
        returns (bytes32)
    {
        return bytes32(addmod(uint256(secret_key), uint256(nonce), Curve.N()));
    }
    
    function SharedSecret (bytes32 my_secret, uint256[2] their_public)
        public constant
        returns (uint256[2])
    {
        Curve.G1Point memory xP = Curve.g1mul(Curve.G1Point(their_public[0], their_public[1]), uint256(my_secret));
        return [xP.X, xP.Y];
    }
}