pragma solidity ^0.4.14;

import "./Curve.sol";

# We want to prove that (G,H,A,B) is a DDH-tuple, i.e. A=xG AND B=xH without revealing secret x
# Reference: https://www.cs.jhu.edu/~susan/600.641/scribes/lecture10.pdf

library ChaumPedersen
{

	function CreateProof(Curve.G1Point G, Curve.G1Point H, uint256 secret, uint256 message )
	    constant internal
	    returns (Curve.G1Point out_G, Curve.G1Point out_H, uint256[2] out_xG, uint256[2] out_xH, uint256 out_s, uint256 out_e)
	{
	    out_G = G;
	    out_H = H;
		Curve.G1Point memory xG = Curve.g1mul(G, secret % Curve.N());
		out_xG[0] = xG.X;
		out_xG[1] = xG.Y;
		Curve.G1Point memory xH = Curve.g1mul(H, secret % Curve.N());
		out_xH[0] = xH.X;
		out_xH[1] = xH.Y;
		uint256 k = uint256(keccak256(abi.encodePacked(message, secret))) % Curve.N();
		Curve.G1Point memory kG = Curve.g1mul(G, k);
		Curve.G1Point memory kH = Curve.g1mul(H, k);
		out_e = uint256(keccak256(abi.encodePacked(out_xG[0], out_xG[1],out_xH[0], out_xH[1] kG.X, kG.Y, kH.X, kH.Y, message)));
		out_s = Curve.submod(k, mulmod(secret, out_e, Curve.N()));
	}


	function CalcProof(Curve.G1Point G, Curve.G1Point H, Curve.G1Point xG, Curve.G1Point xH, uint256 message, uint256 s, uint256 e )
	    constant internal
	    returns (uint256)
	{
	    Curve.G1Point memory sG = Curve.g1mul(G, s % Curve.N());
	    Curve.G1Point memory kG = Curve.g1add(sG, Curve.g1mul(xG, e));

	    Curve.G1Point memory sH = Curve.g1mul(H, s % Curve.N());
	    Curve.G1Point memory kH = Curve.g1add(sG, Curve.g1mul(xH, e));

	    return uint256(keccak256(abi.encodePacked(xG.X, xG.Y, xH.X, xH.Y, kG.X, kG.Y, kH.X, kH.Y, message)));
	}

	function VerifyProof(Curve.G1Point G, Curve.G1Point H, Curve.G1Point xG, Curve.G1Point xH, uint256 message, uint256 s, uint256 e )
	    constant internal
	    returns (bool)
	{
	    return e == CalcProof(G, H, xG, xH, s, e, message);
	}
}