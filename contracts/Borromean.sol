pragma solidity ^0.4.24;
pragma experimental ABIEncoderV2;

import "./Curve.sol";

library Borromean{

  function Borr(uint256[2] pubkey, uint256 s, uint256 e)
  internal view 
  returns(uint256[2]){
    Curve.G1Point memory sG = Curve.g1mul(Curve.P1(), s);
    Curve.G1Point memory eP = Curve.g1mul(Curve.G1Point(pubkey[0], pubkey[1]), e);
    Curve.G1Point memory R = Curve.g1add(sG, Curve.g1neg(eP));
    return [R.X, R.Y];
  }

  function VerifyProof(uint256[2][][] rings, uint256[][] tees, uint256 e0, uint256 message)
  public view
  returns(bool)
  {
    uint256[2] memory R;
    uint256 n = rings.length;
    uint256[2][] memory R_0 = new uint[2][](n);
    for (uint256 i = 0; i < n; i ++){
      uint256 e = e0;
      for (uint256 j = 0; j < tees[i].length; j ++){
        R = Borr(rings[i][j], tees[i][j], e);
        e = uint256(keccak256(abi.encodePacked(R, message))) % Curve.N();
      }
      R_0[i] = R;
    }
    return e0 == (uint256(keccak256(abi.encodePacked(R_0, message))) % Curve.N());
  }
}