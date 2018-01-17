pragma solidity ^0.4.14;

import "./Curve.sol";
import "./Schnorr.sol";

// https://www.iacr.org/cryptodb/archive/2002/ASIACRYPT/50/50.pdf
library AOSRing
{
	function Verify( uint256[] pubkeys, uint256[] tees, uint256 seed, uint256 message )
		public constant
		returns (bool)
	{
		require( pubkeys.length % 2 == 0 );
		require( pubkeys.length > 0 );
		// TODO: verify seed
		// TODO: fit message to Curve.N()
		uint256 c = seed;
		uint256 nkeys = pubkeys.length / 2;
		for( uint256 i = 0; i < nkeys; i++ ) {
			uint256 j = i * 2;
			c = Schnorr.CalcProof([pubkeys[j], pubkeys[j+1]], message, tees[i], c);
		}
		return c == seed;
	}
}