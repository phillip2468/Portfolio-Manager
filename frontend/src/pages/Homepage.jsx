import {Container, Grid} from "@mui/material";
import SearchBar from "../components/SearchBar/SearchBar";
import PopularStocksTable from "../components/PopularStocksTable/PopularStocksTable";
import StockPriceChart from "../components/StockPriceChart/StockPriceCharts";
import {DateTime} from "luxon";
import {useEffect, useState} from "react";


const Homepage = () => {

    const listOfData = ['^AXJO', '^GSPC', '^IXIC', 'AUDUSD=X', 'AUDJPY=X']

    const [historicalData, setHistoricalData] = useState(listOfData
        .reduce((acc, curr) => (acc[curr] = [] , acc), {}))

    useEffect(()=> {
        handleGetHistoricalData("1d")
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
                                {key}
                                <StockPriceChart
                                    heightOfChart={200}
                                    widthOfChart={230}
                                    historicalData={historicalData[key]}
                                    formatTime={dateFormatter}
                                />
                            </div>
                        )
                    })}
                </Grid>
            </Grid>

            <Grid item sx={{position: "relative"}}>
                <SearchBar placeholder={"Search for stocks"}/>
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