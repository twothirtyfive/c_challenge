pragma solidity >=0.4.22 <0.6.0;

contract Registration {
    
    struct record {
        string id;
        bool taken;
    }
    
    mapping(address => string) users;
    mapping(uint16 => record) records;
    uint16 counter = 16;
    
    constructor () public {
        records[0].id = "0000";
        records[1].id = "0001";
        records[2].id = "0010";
        records[3].id = "0011";
        records[4].id = "0100";
        records[5].id = "0101";
        records[6].id = "0110";
        records[7].id = "0111";
        records[8].id = "1000";
        records[9].id = "1001";
        records[10].id = "1010";
        records[11].id = "1011";
        records[12].id = "1100";
        records[13].id = "1101";
        records[14].id = "1110";
        records[15].id = "1111";
    }
    
    function generate(address addr) public{
        assert (counter != 0);
        assert (bytes(users[addr]).length == 0);

        uint16 rand = (uint16 (uint(blockhash(block.number-1))%16));
        while(records[rand].taken) {
            if(rand == 15) { rand = 0; } else { rand += 1; }
        }
        
        records[rand].taken = true;
        users[addr] = records[rand].id;
        
        counter -= 1;
    }
    
    function get_user(address addr) view public returns (string memory) {
        return users[addr];
    }
    
    function get_info() view public returns (uint16, uint16) {
        return (16 - counter, counter);
    }

}
