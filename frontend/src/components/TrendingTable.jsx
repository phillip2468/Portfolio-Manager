import MUIDataTable from 'mui-datatables'
import { useEffect, useState } from 'react'
import { Typography } from '@mui/material'
import styled from 'styled-components'
import millify from 'millify'

const PercentageText = styled.span`
  display: inline-flex;
  padding: 5px;
  font-size: 1em;
  border-radius: 8px;
  background-color: ${(props) => props.changePercentage > 0 ? 'darkseagreen' : 'firebrick'};
  color: ${(props) => props.changePercentage > 0 ? 'darkgreen' : 'darkred'};
`

const TriangleSymbol = styled.div`
  display: inline-block;
  border-right: 8px solid transparent;
  align-self: center;
`

const TrendingTable = () => {
  const [trendingStocks, setTrendingStocks] = useState([])

  const columnDefinitions = [
    { name: 'symbol', label: 'Ticker symbol' },
    { name: 'shortName', label: 'Company name' },
    { name: 'regularMarketPrice', label: 'Price' },
    { name: 'regularMarketDayHigh', label: 'High price' },
    { name: 'regularMarketDayLow', label: 'Low price' },
    {
      name: 'regularMarketChange',
      label: 'Change %',
      options: {
        customBodyRender: (value, tableMeta, updateValue) => {
          return (
                        <>
                            <PercentageText changePercentage={value}>
                                {value > 0
                                  ? <TriangleSymbol>&#x25B2;</TriangleSymbol>
                                  : <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                                <Typography align={'center'}>{value.toFixed(2)}</Typography>
                            </PercentageText>
                        </>
          )
        }
      }
    },
    {
      name: 'marketCap',
      label: 'Market cap',
      options: {
        customBodyRender: (value, tableMeta, updateValue) => {
          return (
                        <>
                            {value && millify(value, {
                              precision: 3
                            })}
                        </>
          )
        }
      }
    }
  ]

  useEffect(() => {
    fetch('/trending-tickers')
      .then((res) => res.json())
      .then((res) => {
        setTrendingStocks(Object.values(res))
      })
  }, [])

  const options = {
    download: false,
    print: false,
    search: false,
    sortFilterList: false,
    viewColumns: false,
    selectableRows: 'none',
    rowHover: false,
    fixedSelectColumn: false,
    fixedHeader: false,
    filterArrayFullMatch: false
  }

  return (
        <>
            <MUIDataTable
                title={'Trending stocks today (from Yahoo finance)'}
                data={trendingStocks}
                columns={columnDefinitions}
                options={options}
            />
        </>
  )
}

export default TrendingTable
