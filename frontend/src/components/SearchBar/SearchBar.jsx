import React, {useEffect, useState} from 'react';
import {
    DataResult,
    OuterContainer,
    SearchResultsGrid,
    StocksNameTicker,
    StocksPercentage,
    StocksPrice,
    TriangleSymbol
} from "./styled";
import {useNavigate} from "react-router-dom";
import SearchInputBox from "./components/SearchInputBox";
//https://stackoverflow.com/questions/42987939/styled-components-organization


const SearchBar = ({placeholder}) => {

    const navigate = useNavigate();
    const [typedInput, setTypedInput] = useState("");
    const [filteredData, setFilteredData] = useState([]);
    const [allStocksInfo, setAllStocksInfo] = useState([])
    const [showResults, setShowResults] = useState(false);

    useEffect(() => {
            fetch('/search')
                .then((res) => res.json())
                .then((res) => {
                    setAllStocksInfo(Object.values(res))
                })
        }
        , [])


    const handleSearch = (event) => {
        const searchTerm = event.target.value;
        setTypedInput(searchTerm);

        const newFilter = allStocksInfo.filter((value) => {
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
            <SearchInputBox placeholder={placeholder} value={typedInput} onChange={handleSearch}
                            onBlur={() => setShowResults(false)} onFocus={() => setShowResults(true)}/>
            <div style={{position: "relative", display: showResults === false ? "none" : "block"}}>
                {typedInput.length !== 0 && (
                    <DataResult>
                        {filteredData.map((item, key) => {
                            return <SearchResultsGrid
                                key={key}
                                onClick={() => navigate(`/${item.symbol}`)}
                            >
                                <StocksNameTicker>
                                    <div>{item.stock_name}</div>
                                    <div>{item.symbol}</div>
                                </StocksNameTicker>

                                <StocksPrice>
                                    ${parseFloat(item.price).toFixed(2)}
                                </StocksPrice>

                                <StocksPercentage percentageChange={item.change}>
                                    {item.change > 0 ? <TriangleSymbol>&#x25B2;</TriangleSymbol> :
                                        <TriangleSymbol>&#x25BC;</TriangleSymbol>}
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