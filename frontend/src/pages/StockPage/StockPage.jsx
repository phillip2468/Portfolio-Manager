import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {Container, Divider, Grid} from "@mui/material";
import {TriangleSymbol} from "../../components/SearchBar/styled";
import {MiscDetailsStock, StockInfoContainer, StockPercentageChange} from "./styled";
import Button from "@mui/material/Button";
import {ResponsiveContainer, LineChart, Line, Tooltip, Legend, XAxis, CartesianGrid, YAxis} from "recharts";
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

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="label">{`${dateFormatter(label)}`}</p>
                    <p>${parseFloat(payload[0].value).toFixed(2)}</p>
                </div>
            );
        }

        return null;
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
                    <Grid item>
                        <StockInfoContainer>
                            <div style={{fontSize: "2em"}}>
                                ${stockInfo.market_current_price}
                            </div>
                            <div style={{fontSize: "1.2em"}}>
                                <StockPercentageChange percentageChange={stockInfo.market_change_percentage}>
                                    {stockInfo.market_change_percentage > 0 ?
                                        <TriangleSymbol>&#x25B2;</TriangleSymbol> :
                                        <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                                    {(parseFloat(stockInfo.market_change_percentage) * 100).toFixed(2)}%
                                </StockPercentageChange>
                            </div>
                            <div>
                                {stockInfo.market_change > 0 ? ("+") : ("-")}
                                {parseFloat(stockInfo.market_change).toFixed(3)}
                            </div>
                        </StockInfoContainer>
                        <MiscDetailsStock>
                             {last_updated_fmt} {stockInfo.currency} {stockInfo.exchange}
                        </MiscDetailsStock>
                    </Grid>
                    <Grid item>
                        <Grid container>
                            {list_of_periods.map((element, index) => {
                                return (
                                    <Button key={index} size={"small"} onClick={() => handleGetHistoricalData(element)}>
                                        {element}
                                    </Button>
                                )
                            })}
                        </Grid>
                    </Grid>
                    <Grid item>
                        <ResponsiveContainer height={500} >
                            <LineChart data={historicalData}>
                                <XAxis dataKey={"time"} domain={['dataMin', 'dataMax']} interval={"preserveStartEnd"} tickFormatter={dateFormatter}/>
                                <YAxis domain={['auto', 'auto']}/>
                                <CartesianGrid strokeDasharray="2 2"/>
                                <Tooltip content={<CustomTooltip/>}/>
                                <Legend/>
                                <Line type="monotone" dataKey={"open"} activeDot={{r: 3}} stroke="#8884d8"/>
                            </LineChart>
                        </ResponsiveContainer>
                    </Grid>
                </Grid>

            </Container>
        </Grid>
    )
}

export default StockPage;