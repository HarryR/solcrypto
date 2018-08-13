pragma solidity ^0.4.19;

import "./Curve.sol"

library Pederson {

    /**
     * @dev        Generate Pedersen Commitment C = r * H + x * G
     * @param      a     Random point for generating another generator H
     * @param      x     Message to commit to
     * @param      r     Random value
     * @return     res   uint256 commitment
     */
    function commitWithGen(uint256 a, uint256 x, uint256 r) returns(uint256[2]) internal {
        // Generate H = a * g
        Curve.G1Point H = Curve.g1mul(G1.P1(), a);

        // Generate left point r * H
        Curve.G1Point lf = Curve.g1mul(H, r);

        // Generate right point x * g
        Curve.G1Point rt = Curve.g1mul(G1.P1(), x);

        // Generate C = r * H + x * G
        Curve.G1Point c = Curve.g1add(lf, rt);

        return (c.X, c.Y);
    }

    /**
     * @dev        Generate Pedersen Commitment C = r * H + x * G
     * @param      H     Supposedly another random generator
     * @param      x     Message to commit to
     * @param      r     Random value
     * @return     res   uint256 commitment
     */
    function commitWithH(uint256 H, uint256 x, uint256 r) returns(uint256[2]) internal {
        // Generate left point r * H
        Curve.G1Point lf = Curve.g1mul(H, r);

        // Generate right point x * G
        Curve.G1Point rt = Curve.g1mul(G1.P1(), x);

        // Generate C = r * H + x * G
        Curve.G1Point c = Curve.g1add(lf, rt);

        return (c.X, c.Y);
    }
    
    function verifyWithGen(uint256[2] commitment, uint256 x, uint256 r, uint256 a) returns(bool) internal {
        // Generate H = a * g
        Curve.G1Point H = Curve.g1mul(G1.P1(), a);

        // Generate left point r * H
        Curve.G1Point lf = Curve.g1mul(H, r);

        // Generate right point x * g
        Curve.G1Point rt = Curve.g1mul(G1.P1(), x);

        // Generate C = r * H + x * G
        Curve.G1Point c = Curve.g1add(lf, rt);

        return (c.X == commitment[0] && c.Y == commitment[1]);
    }

    function verifyWithH(uint256[2] commitment, uint256 x, uint256 r, uint256 H) returns(bool) internal {
        // Generate left point r * H
        Curve.G1Point lf = Curve.g1mul(H, r);

        // Generate right point x * g
        Curve.G1Point rt = Curve.g1mul(G1.P1(), x);

        // Generate C = r * H + x * G
        Curve.G1Point c = Curve.g1add(lf, rt);

        return (c.X == commitment[0] && c.Y == commitment[1]);
    }
}
