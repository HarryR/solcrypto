pragma solidity ^0.4.14;

import {altbn128 as Curve} from "./altbn128.sol";

// https://en.wikipedia.org/wiki/Proof_of_knowledge#Schnorr_protocol
library Schnorr
{
    // Costs ~85000 gas, 2x ecmul, + mulmod, addmod, hash etc. overheads
	function CreateProof( bytes32 secret, bytes32 message )
	    constant
	    returns (uint256[2] out_pubkey, uint256 out_s, uint256 out_e)
	{
		Curve.G1Point memory xG = Curve.g1mul(Curve.P1(), uint256(secret) % Curve.N());
		out_pubkey[0] = xG.X;
		out_pubkey[1] = xG.Y;
		uint256 k = uint256(keccak256(message, secret));
		Curve.G1Point memory kG = Curve.g1mul(Curve.P1(), k);
		out_e = uint256(keccak256(out_pubkey, kG.X, kG.Y, message));
		out_s = Curve.submod(k, mulmod(uint256(secret), uint256(out_e), Curve.N()));
	}
	
	// Costs ~85000 gas, 2x ecmul, 1x ecadd, + small overheads
	function VerifyProof( uint256[2] pubkey, bytes32 message, uint256 s, uint256 e )
	    constant
	    returns (bool)
	{
	    Curve.G1Point memory sG = Curve.g1mul(Curve.P1(), s % Curve.N());
	    Curve.G1Point memory xG = Curve.G1Point(pubkey[0], pubkey[1]);
	    Curve.G1Point memory kG = Curve.g1add(sG, Curve.g1mul(xG, e));
	    bytes32 check_e = keccak256(pubkey, kG.X, kG.Y, message);
	    return bytes32(e) == check_e;
	}
}