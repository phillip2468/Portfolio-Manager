import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {Container, Divider, Grid} from "@mui/material";
import {TriangleSymbol} from "../../components/SearchBar/styled";
import {StockPercentageChange} from "./styled";
const { DateTime } = require("luxon");

const StockPage = () => {
    const {stockName} = useParams()
    const [stockInfo, setStockInfo] = useState([]);

    useEffect(()=> {
        fetch(`/quote/${stockName}`)
            .then(res => res.json())
            .then(res => setStockInfo(res[0]))
    }, [])

    const thing = DateTime.fromFormat("Sat, 15 Jan 2022 13:07:04", "EEE, dd MMM yyyy TT", {locale: 'en-AU'})
    console.log(thing)

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
                        <div style={{display: "flex", columnGap: "2%", alignItems: "center"}}>
                            <div style={{fontSize: "2em"}}>
                                ${stockInfo.market_current_price}
                            </div>
                            <div style={{fontSize: "1.2em"}}>
                                <StockPercentageChange percentageChange={stockInfo.market_change_percentage}>
                                    {stockInfo.market_change_percentage > 0 ? <TriangleSymbol>&#x25B2;</TriangleSymbol> : <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                                    {(parseFloat(stockInfo.market_change_percentage) * 100).toFixed(2)}
                                </StockPercentageChange>
                            </div>
                            <div>
                                {thing.toString()}
                            </div>
                            {stockInfo.market_change} last updated at {stockInfo.last_updated}
                        </div>
                    </Grid>
                </Grid>

            </Container>
        </Grid>
    )
}

export default StockPage;