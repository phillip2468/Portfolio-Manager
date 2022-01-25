import {Container, Grid} from "@mui/material";
import SearchBar from "../components/SearchBar/SearchBar";
import PopularStocksTable from "../components/PopularStocksTable/PopularStocksTable";
import StockPriceChart from "../components/StockPriceChart/StockPriceCharts";
import {DateTime} from "luxon";
import {useEffect, useState} from "react";


const Homepage = () => {

    const listOfData = ['^AXJO', '^GSPC', '^IXIC', 'AUDUSD=X', 'AUDJPY=X']

    const [historicalData, setHistoricalData] = useState(listOfData
        // eslint-disable-next-line
        .reduce((acc, curr) => (acc[curr] = [] , acc), {}))

    useEffect(()=> {
        handleGetHistoricalData("1d")
        // eslint-disable-next-line
    }, [])

    const handleGetHistoricalData = (period) => {
        listOfData.map(async (thisElement, index, array) => {
            const result = await fetch(`/quote/${thisElement}&period=${period}&interval=30m`)
            const response = await result.json()
            const key = array[index]
            setHistoricalData(prevState => ({
                ...prevState, [key]: response}
            ))
        })
    }

    const dateFormatter = date => {
        return DateTime.fromHTTP(date).toLocaleString(DateTime.DATETIME_SHORT);
    };

    return (
        <>
            <Grid item>
                <Grid container direction={"row"}>
                    {Object.keys(historicalData).map(function(key) {
                        return (
                            <div key={key} style={{textAlign: "center"}}>
                                <div>
                                    {key}
                                </div>
                                <div>
                                    {parseFloat(historicalData[key]['market_change_perc']).toFixed(2)}%
                                </div>
                                <div>
                                    {historicalData[key]['currency_symbol']}{historicalData[key]['price_now']}
                                </div>
                                <StockPriceChart
                                    heightOfChart={200}
                                    widthOfChart={220}
                                    historicalData={historicalData[key]['priceList']}
                                    formatTime={dateFormatter}
                                />
                            </div>
                        )
                    })}
                </Grid>
            </Grid>

            <Grid item sx={{position: "relative"}}>
                <SearchBar placeholder={"Search by stock symbols or company names"}/>
            </Grid>

            <Grid item>
                <Container sx={{width: "52%"}}>
                    <PopularStocksTable/>
                </Container>
            </Grid>
        </>
    )
}

export default Homepage;