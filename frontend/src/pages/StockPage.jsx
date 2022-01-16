import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {Container, Grid} from "@mui/material";

const StockPage = () => {
    const {stockName} = useParams()
    const [stockInfo, setStockInfo] = useState([]);

    useEffect(()=> {
        fetch(`/quote/${stockName}`)
            .then(res => res.json())
            .then(res => setStockInfo(Object.values(res)))
    }, [])

    return (
        <Grid item>
            <Container maxWidth={"xs"}>
                {stockName}
            </Container>
        </Grid>
    )
}

export default StockPage;