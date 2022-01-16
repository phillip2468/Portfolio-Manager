import {useParams} from "react-router-dom";
import {useEffect} from "react";
import {Container, Grid} from "@mui/material";

const StockPage = () => {
    const {stockName} = useParams()

    useEffect(()=> {

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