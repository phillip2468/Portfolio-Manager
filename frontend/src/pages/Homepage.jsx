import {useEffect, useState} from "react";
import {Container, Grid, Typography} from "@mui/material";
import Header from "../components/Header";
import MUIDataTable from "mui-datatables";

const Homepage = () => {

    const [trendingStocks, setTrendingStocks] = useState([]);

    const columnDefinitions = [
        {name: 'symbol', label: 'Ticker symbol'},
        {name: 'shortName', label: 'Company name'},
        {name: 'regularMarketPrice', label: 'Price'},
        {name: 'regularMarketDayHigh', label: 'High price'},
        {name: 'regularMarketDayLow', label: 'Low price'},
        {name: 'regularMarketChange', label: 'Change %', options: {
            customBodyRender: (value, tableMeta, updateValue) => {
                return (
                    <Typography>{value.toFixed(2)}</Typography>
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