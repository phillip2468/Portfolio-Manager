import {useEffect, useState} from "react";
import {Container, Grid, Typography} from "@mui/material";
import Header from "../components/Header";
import MUIDataTable from "mui-datatables";
import styled from "styled-components"

const PercentageText = styled.span`
  display: inline-flex;
  padding: 5px;
  font-size: 1em;
  border-radius: 8px;
  background-color: ${(props) => props.changePercentage > 0 ? "darkseagreen" : "firebrick"};
  color: ${(props) => props.changePercentage > 0 ? "darkgreen" : "darkred"};
`

const TriangleSymbol = styled.div`
  display: inline-block;
  border-right: 8px solid transparent;
  align-self: center;
`

const Homepage = () => {

    const [trendingStocks, setTrendingStocks] = useState([]);

    const columnDefinitions = [
        {name: 'symbol', label: 'Ticker symbol'},
        {name: 'shortName', label: 'Company name'},
        {name: 'regularMarketPrice', label: 'Price'},
        {name: 'regularMarketDayHigh', label: 'High price'},
        {name: 'regularMarketDayLow', label: 'Low price'},
        {
            name: 'regularMarketChange', label: 'Change %', options: {
                customBodyRender: (value, tableMeta, updateValue) => {
                    return (
                        <>
                            <PercentageText changePercentage={value}>
                                {value > 0 ? <TriangleSymbol>&#x25B2;</TriangleSymbol> : <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                                <Typography align={"center"}>{value.toFixed(2)}</Typography>
                            </PercentageText>
                        </>
                    )
                }
            }
        },
        {name: 'marketCap', label: 'Market cap'},
    ]

    useEffect(() => {
        fetch('/trending-tickers')
            .then((res) => res.json())
            .then((res) => {
                setTrendingStocks(Object.values(res))
            })
    }, [])


    return (
        <Grid container spacing={2} direction={"column"}>
            <Grid item>
                <Header/>
            </Grid>

            <Grid item>
                <Container>
                    <MUIDataTable
                        title={"Trending stocks today in the US"}
                        data={trendingStocks}
                        columns={columnDefinitions}
                        options={{
                            download: false,
                            print: false,
                            search: false,
                            sortFilterList: false,
                            viewColumns: false,
                            selectableRows: 'none',
                            rowHover: false,
                            pagination: false,
                            fixedSelectColumn: false,
                            fixedHeader: false,
                            filterArrayFullMatch: false,
                        }
                        }/>
                </Container>
            </Grid>

        </Grid>

    )
}

export default Homepage;