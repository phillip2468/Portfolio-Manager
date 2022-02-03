import React, { useState } from 'react'
import {
  DataResult,
  OuterContainer,
  SearchResultsGrid,
  StocksNameTicker,
  StocksPercentage,
  StocksPrice,
  TriangleSymbol
} from './styled'
import { useNavigate } from 'react-router-dom'
import SearchInputBox from './components/SearchInputBox'
import * as PropTypes from 'prop-types'
// https://stackoverflow.com/questions/42987939/styled-components-organization

const SearchBar = ({ placeholder }) => {
  const navigate = useNavigate()
  const [typedInput, setTypedInput] = useState('')

  const [otherData, setOtherData] = useState([])

  const handleSearch = (event) => {
    const searchTerm = event.target.value
    setTypedInput(searchTerm)

    fetch(`/search/${typedInput}`)
      .then((res) => res.json())
      .then((res) => setOtherData(res))
  }

  return (
        <OuterContainer>
            <SearchInputBox onChange={handleSearch} placeholder={placeholder} value={typedInput}
                           />
            <div style={{ position: 'relative', display: 'block' }}>
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
                                        ${parseFloat(item.market_current_price).toFixed(2)}
                                    </StocksPrice>

                                    <StocksPercentage percentageChange={item.market_change_percentage}>
                                        {item.market_change_percentage > 0
                                          ? <TriangleSymbol>&#x25B2;</TriangleSymbol>
                                          : <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                                        {(parseFloat(item.market_change_percentage) * 100).toFixed(2)}
                                    </StocksPercentage>
                            </SearchResultsGrid>
                        })}
                    </DataResult>
                )
                }
            </div>
        </OuterContainer>
  )
}

SearchBar.propTypes = {
  placeholder: PropTypes.string
}

export default SearchBar
