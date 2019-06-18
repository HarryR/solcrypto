pragma solidity ^0.5.8;


import { BN256G2 } from "./BN256G2.sol";


contract BLSValidators
{
    uint256 internal constant FIELD_ORDER = 0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47;

    // a = (FIELD_ORDER+1) // 4
    uint256 internal constant CURVE_A = 0xc19139cb84c680a6e14116da060561765e05aa45a1c72a34f082305b61f3f52;

    struct Validator {
        address owner;
        uint256 amount;
        uint256[4] pubkey;
    }

    uint256 internal aggregate_bitmask;
    uint256[4] internal aggregate_pubkey;

    mapping (uint8 => Validator) internal validators;

    event OnNewValidator(uint8 index, address owner, uint256[4] pk);

    event OnValidatorRemoved(uint8 index);

    constructor () public {
        aggregate_pubkey = [uint256(0), uint256(0), uint256(0), uint256(0)];
    }

    function HashToG1(uint256 s)
        internal view returns (uint256[2] memory)
    {
        uint256 beta = 0;
        uint256 y = 0;
        uint256 x = s % FIELD_ORDER;
        while( true ) {
            (beta, y) = FindYforX(x);
            if(beta == mulmod(y, y, FIELD_ORDER)) {
                return [x, y];
            }
            x = addmod(x, 1, FIELD_ORDER);
        }
    }

    function FindYforX(uint256 x)
        internal view returns (uint256, uint256)
    {
        // beta = (x^3 + b) % p
        uint256 beta = addmod(mulmod(mulmod(x, x, FIELD_ORDER), x, FIELD_ORDER), 3, FIELD_ORDER);
        uint256 y = modPow(beta, CURVE_A, FIELD_ORDER);
        return (beta, y);
    }

    function AddValidator(uint8 index, uint256[4] memory pk, uint256[2] memory sig)
        public payable
    {
        require( msg.value != 0 );        
        require( validators[index].owner == address(0) );
        require( ProvePublicKey(pk, sig) );

        validators[index] = Validator(msg.sender, msg.value, pk);

        // To handle the special case where all validators agree on something
        // We pre-accumulate the keys to avoid doing it every time a signature is validated
        // Maintain a bitmask of their indices 
        uint256[4] memory p;
        (p[0], p[1], p[2], p[3]) = BN256G2.ECTwistAdd(aggregate_pubkey[0], aggregate_pubkey[1],
                                                      aggregate_pubkey[2], aggregate_pubkey[3],
                                                      pk[0], pk[1], pk[2], pk[3]);
        aggregate_pubkey = p;
        aggregate_bitmask = aggregate_bitmask + (uint256(1)<<index);

        emit OnNewValidator(index, msg.sender, pk);
    }

    function RemoveValidator(uint8 index)
        public
    {
        Validator storage who = validators[index];
        require( who.owner == msg.sender );        

        // Remove their key from the aggregate, and their index from the bitmask
        uint256[4] memory p = negate(who.pubkey);
        (p[0], p[1], p[2], p[3]) = BN256G2.ECTwistAdd(aggregate_pubkey[0], aggregate_pubkey[1],
                                                      aggregate_pubkey[2], aggregate_pubkey[3],
                                                      p[0], p[1], p[2], p[3]);
        aggregate_pubkey = p;
        aggregate_bitmask = aggregate_bitmask - (uint256(1)<<index);

        // Save amount before deleting
        // must be deleted first, otherwise opens up re-entrancy bugs
        uint256 amount = who.amount;
        delete validators[index];

        // Return their deposit
        msg.sender.transfer(amount);

        emit OnValidatorRemoved(index);
    }

    function GetValidator(uint8 index)
        public view returns (address, uint256, uint256[4] memory)
    {
        Validator memory who = validators[index];
        return (who.owner, who.amount, who.pubkey);
    }
    
    function HashG2(uint256[4] memory pubkey)
        internal pure returns (uint256)
    {
        return uint256(keccak256(abi.encodePacked(pubkey)));
    }

    function ProvePublicKey(uint256[4] memory pubkey, uint256[2] memory sig)
        public view returns (bool)
    {
        return CheckSignature(HashG2(pubkey), pubkey, sig);
    }
    
    function GetAggregateBitmask( )
        public view returns (uint256)
    {
        return aggregate_bitmask;
    }
    
    function GetAggregatePubkey( )
        public view returns (uint256[4] memory)
    {
        return aggregate_pubkey;
    }
    
    function AggregateKeyForBitmask( uint256 bitmask )
        public view returns (uint256[4] memory ap)
    {
        // In the special case where all aggregators agree on the same signature
        if( bitmask == aggregate_bitmask ) {
            ap = aggregate_pubkey;
        }
        else {
            for(uint8 i = 0; i < 0xFF; i++)
            {
                if( (bitmask >> i) & 1 > 0 )
                {
                    require( validators[i].owner != address(0) );
                    uint256[4] memory p = validators[i].pubkey;
                    (ap[0], ap[1], ap[2], ap[3]) = BN256G2.ECTwistAdd(ap[0], ap[1], ap[2], ap[3],
                                                                      p[0], p[1], p[2], p[3]);
                }
            }
        }
    }
    
    function CheckSignature(uint256 message, uint256[4] memory pubkey, uint256[2] memory sig)
        public view returns (bool)
    {
        return pairing2(HashToG1(message), pubkey, sig, NegativeG2());
    }

    function CheckSignature(uint256 bitmask, uint256[2] memory sig, uint256 message)
        public view returns (bool)
    {
        uint256[4] memory ap;
        require( bitmask > 0 );
        ap = AggregateKeyForBitmask(bitmask);
        return CheckSignature(message, ap, sig);
    }
    
    function CheckSignature(uint256 bitmask, uint256[2] memory sig, bytes memory message_bytes)
        public view returns (bool)
    {
        uint256 message = uint256(keccak256(message_bytes));
        return CheckSignature(bitmask, sig, message);
    }

    // neg(G2)
    function NegativeG2()
        internal pure returns (uint256[4] memory)
    {
        return [0x1800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed,
                0x198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c2,
                0x1d9befcd05a5323e6da4d435f3b617cdb3af83285c2df711ef39c01571827f9d,
                0x275dc4a288d1afb3cbb1ac09187524c7db36395df7be3b99e673b13a075a65ec];
    }

    /// Convenience method for a pairing check for two pairs.
    function pairing2(uint256[2] memory a1, uint256[4] memory a2, uint256[2] memory b1, uint256[4] memory b2)
        internal view returns (bool)
    {
        // Note that G2 points have reversed coefficients when using the Ethereum pairing precompile
        uint256[12] memory input = [
            a1[0], a1[1],               // a1 (G1)
            a2[1], a2[0], a2[3], a2[2], // a2 (G2)

            b1[0], b1[1],               // b1 (G1)
            b2[1], b2[0], b2[3], b2[2]  // b2 (G2)
        ];
        uint[1] memory out;
        assembly {
            if iszero(staticcall(sub(gas, 2000), 8, input, 0x180, out, 0x20)) {
                revert(0, 0)
            }
        }
        return out[0] != 0;
    }

    function modPow(uint256 base, uint256 exponent, uint256 modulus)
        internal view returns (uint256)
    {
        uint256[6] memory input = [32, 32, 32, base, exponent, modulus];
        uint256[1] memory result;
        assembly {
            if iszero(staticcall(not(0), 0x05, input, 0xc0, result, 0x20)) {
                revert(0, 0)
            }
        }
        return result[0];
    }

    function negate(uint256 value)
        internal pure returns (uint256)
    {
        return FIELD_ORDER - (value % FIELD_ORDER);
    }

    function negate(uint256[4] memory p)
        internal pure returns (uint256[4] memory)
    {
        return [p[0], p[1], negate(p[2]), negate(p[3])];
    }
}
