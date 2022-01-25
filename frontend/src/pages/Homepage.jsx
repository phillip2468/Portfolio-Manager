import {Container, Grid} from "@mui/material";
import SearchBar from "../components/SearchBar/SearchBar";
import PopularStocksTable from "../components/PopularStocksTable/PopularStocksTable";
import StockPriceChart from "../components/StockPriceChart/StockPriceCharts";
import {DateTime} from "luxon";
import {useContext, useEffect, useState} from "react";
import Button from "@mui/material/Button";
import {ClientContext} from "../store/StoreCredentials";
import {FetchFunction} from "../components/FetchFunction";


const Homepage = () => {

    const listOfData = ['^AXJO', '^GSPC', '^IXIC', 'AUDUSD=X', 'AUDJPY=X']

    let {token} = useContext(ClientContext);

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

    const getDetails = () => {
        FetchFunction('GET', '/auth/user-details', token, null)
            .then(res => console.log(res))
            .catch(e => console.log(e))
    }

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
                                    widthOfChart={220}
                                    historicalData={historicalData[key]}
                                    formatTime={dateFormatter}
                                />
                            </div>
                        )
                    })}
                </Grid>
            </Grid>

            <Button onClick={() => getDetails()}>
                get
            </Button>

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