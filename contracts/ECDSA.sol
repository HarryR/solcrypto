pragma solidity ^0.4.19;


library ECDSA
{
    /**
    * This unpacks the 'v' parameter from the upper bit of 's' which means
    * a signature can be packed into two 256bit words.
    */
    function recover( bytes32 hash, uint256 r, uint256 sv )
        internal pure
        returns (address)
    {
        uint256 oneshl255 = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
        uint8 v;
        if( (sv & oneshl255) > 0 ) {
            v = 28;
            sv ^= oneshl255;
        }
        else {
            v = 27;
        }
        return ecrecover(hash, v, bytes32(r), bytes32(sv));
    }   
}
