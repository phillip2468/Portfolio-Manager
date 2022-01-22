import React, {useState} from 'react';
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
    const [showResults, setShowResults] = useState(false);

    const [otherData, setOtherData] = useState([]);

    const handleSearch = (event) => {
        const searchTerm = event.target.value;
        setTypedInput(searchTerm);

        fetch(`/search/${typedInput}`)
            .then((res) => res.json())
            .then((res) => setOtherData(res))
    }

    return (
        <OuterContainer>
            <SearchInputBox placeholder={placeholder} value={typedInput} onChange={handleSearch}
                            onBlur={() => setShowResults(false)} onFocus={() => {setShowResults(true)}}/>
            <div style={{position: "relative", display: showResults === false ? "none" : "block"}}>
                {typedInput.length !== 0 && (
                    <DataResult>
                        {otherData.map((item, key) => {
                            return <SearchResultsGrid
                                key={key}
                                onMouseDown={() => navigate(`/${item.symbol}`)}
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