import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {Divider} from "@mui/material";
import Button from "@mui/material/Button";
import StockPriceChart from "../../components/StockPriceChart/StockPriceCharts";
import StockIntervals from "./components/StockIntervals";
import StockPriceDetails from "./components/StockPriceDetails";
import StockDetails from "./components/StockDetails";


const {DateTime} = require("luxon");

const StockPage = () => {
    const {stockName} = useParams()
    const [stockInfo, setStockInfo] = useState([]);
    const last_updated_fmt = DateTime.fromISO(stockInfo.last_updated).toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS);
    const list_of_periods = ['1d', '5d', '7d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'];
    const [historicalData, setHistoricalData] = useState([]);

    useEffect(() => {
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

    {console.log(last_updated_fmt)}
    {console.log(typeof stockInfo.last_updated)}

    return (
        <>
            <StockDetails
                stockInfo={stockInfo}
            />

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
                widthOfChart={1000}
            />
        </>
    )
}

export default StockPage;