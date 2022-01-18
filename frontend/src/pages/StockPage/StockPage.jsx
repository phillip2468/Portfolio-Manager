import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {Container, Divider, Grid} from "@mui/material";
import Button from "@mui/material/Button";
import StockPriceChart from "../../components/StockPriceChart/StockPriceCharts";
import StockIntervals from "./components/IntervalForChart/StockIntervals";
import StockPriceDetails from "./components/StockPriceDetails/StockPriceDetails";


const { DateTime } = require("luxon");





const StockPage = () => {
    const {stockName} = useParams()
    const [stockInfo, setStockInfo] = useState([]);
    const last_updated_fmt = DateTime.fromHTTP(stockInfo.last_updated).toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS);
    const list_of_periods = ['1d', '5d', '7d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'];
    const [historicalData, setHistoricalData] = useState([]);

    useEffect(()=> {
        fetch(`/quote/${stockName}`)
            .then(res => res.json())
            .then(res => setStockInfo(res[0]));
        fetch(`/quote/${stockName}&period=1d&interval=30m`)
            .then(res => res.json())
            .then(res => setHistoricalData(res));
    }, [stockName])

    const handleGetHistoricalData = (period) => {
        fetch(`/quote/${stockName}&period=${period}&interval=30m`)
            .then(res => res.json())
            .then(res => setHistoricalData(res))
    }

    const dateFormatter = date => {
        return DateTime.fromHTTP(date).toLocaleString(DateTime.DATETIME_SHORT);
    };


    return (
        <Grid item>
            <Container maxWidth={"md"} sx={{border: "1px solid white"}}>
                <Grid container spacing={2} direction={"column"}>


                    <Grid item>
                        <div>
                            {stockInfo.symbol}
                        </div>
                        <div style={{fontSize: "2em"}}>
                            {stockInfo !== [] && stockInfo.stock_name}
                        </div>
                    </Grid>
                    <Divider light={true}/>


                    <StockPriceDetails
                        stockInfo={stockInfo}
                        lastUpdatedFmt={last_updated_fmt}
                    />


                    <StockIntervals listOfIntervals={list_of_periods} callbackfn={(element, index) => {
                        return (
                            <Button key={index} size={"small"} onClick={() => handleGetHistoricalData(element)}>
                                {element}
                            </Button>
                        )
                    }}/>

                    <StockPriceChart
                        historicalData={historicalData}
                        formatTime={dateFormatter}
                        heightOfChart={500}
                    />

                </Grid>
            </Container>
        </Grid>
    )
}

export default StockPage;