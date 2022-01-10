import {useEffect, useState} from "react";
import {XAxis, YAxis, LineChart, Line, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from "recharts";
import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import Button from "@mui/material/Button";
import {Typography} from "@material-ui/core";

const PredictorPage = () => {

    const [data, setData] = useState([])
    const [actualPrices, setActualPrices] = useState([])
    const [predictedPrices, setPredictedPrices] = useState([])

    const [errorMessage, setErrorMessage] = useState('')

    useEffect( ()=> {}
    , [])

    const getData = () => {
        fetch("/ai-data")
            .then(res => res.json())
            .then(res => {
                setActualPrices(res["actual"])
                setPredictedPrices(res["predicted"])
                setData(res["next_day"])
            })
            .catch((error) => setErrorMessage(error))
    }

    return (
        <>
            <Grid container spacing={4} direction={"column"}>
                <Grid item>
                    <Header/>
                </Grid>
            </Grid>

            <Container>
                <Typography>
                    {"Type in a stock to analyse " + data}
                    {errorMessage}
                    <Button onClick={() => getData()}>
                        Submit
                    </Button>
                </Typography>

                <ResponsiveContainer height={500}>
                    <LineChart height={300} >
                        <XAxis type="number" dataKey={"day"} domain={['auto', 'auto']}/>
                        <YAxis domain={[50, 'auto']}/>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <Tooltip/>
                        <Legend />
                        <Line type="monotone" data={actualPrices} dataKey="price" stroke="darkgreen" activeDot={{r: 8}} name={"Actual"}/>
                        <Line type="monotone" data={predictedPrices} dataKey="price" stroke="#8884d8" name={"Predicted"}/>
                    </LineChart>
                </ResponsiveContainer>
            </Container>

        </>
    )
}

export default PredictorPage;