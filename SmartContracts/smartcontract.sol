pragma solidity ^0.5.0;

pragma experimental ABIEncoderV2;

contract HelloWorld {
    string[][] private data;

    // Constructor to initialize the data with user-provided values
    constructor(string[][] memory _initialData) public {
        setData(_initialData);
    }

    // Function to get the current data
    function getData() public view returns (string[][] memory) {
        return data;
    }

    // Function to set new data
    function setData(string[][] memory _newData) public {
        data = _newData;
    }
}
