import React, {useEffect, useState} from 'react';
import SearchIcon from "@material-ui/icons/Search";
import {
    DataResult,
    OuterContainer,
    SearchBox,
    SearchIconBox,
    SearchInput,
    SearchResultsGrid, StocksNameTicker, StocksPercentage, StocksPrice,
    TriangleSymbol
} from "./styled";
//https://stackoverflow.com/questions/42987939/styled-components-organization



const SearchBar = ({placeholder}) => {

    const [typedInput, setTypedInput] = useState("");
    const [filteredData, setFilteredData] = useState([]);
    const [searchable, setSearchable] = useState([])

    useEffect(()=> {
            fetch('/quote/search')
                .then((res) => res.json())
                .then((res) => {
                    setSearchable(Object.values(res))
                })
        }
    , [])


    const handleSearch = (event) => {
        const searchTerm = event.target.value;
        setTypedInput(searchTerm);

        const newFilter = searchable.filter((value) => {
            return value.stock_name.toLowerCase().includes(typedInput.toLowerCase())
        })
        if (typedInput === "") {
            setFilteredData([]);
        } else {
            setFilteredData(newFilter);
        }
    }

    return (
        <OuterContainer>
            <SearchBox>
                <SearchInput
                    type={"text"}
                    placeholder={placeholder}
                    value={typedInput}
                    onChange={handleSearch}
                />
                <SearchIconBox>
                    <SearchIcon/>
                </SearchIconBox>
            </SearchBox>
            <div style={{position: "relative"}}>
                {typedInput.length !== 0 && (
                    <DataResult>
                        {filteredData.map((item, key)=> {
                            return <SearchResultsGrid
                                key={key}>
                                <StocksNameTicker>
                                    <div>{item.stock_name}</div>
                                    <div>{item.symbol}</div>
                                </StocksNameTicker>
                                <StocksPrice>
                                    ${parseFloat(item.price).toFixed(2)}
                                </StocksPrice>
                                <StocksPercentage percentageChange={item.change}>
                                    {item.change > 0 ? <TriangleSymbol>&#x25B2;</TriangleSymbol> : <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                                    {(parseFloat(item.change) * 100).toFixed(2)}
                                </StocksPercentage>
                            </SearchResultsGrid>
                        })}
                    </DataResult>
                )
                }
            </div>
        </OuterContainer>
    );
};

export default SearchBar;