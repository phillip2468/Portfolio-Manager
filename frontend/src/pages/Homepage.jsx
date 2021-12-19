import {useEffect, useState} from "react";
import Button from '@mui/material/Button';
import {Container, Grid, Input} from "@mui/material";
import Header from "../components/Header";

const Homepage = () => {

    const [tickers, setTickers] = useState(undefined)

    const getAusTickers = async () => {
        const result = await fetch('/aus-tickers');
        const response = await result.json();
        setTickers(response)
    }

    useEffect(() => {
        console.log('Mounted!')
    }, [tickers])

    useEffect(() => {
        fetch('/trending-tickers')
            .then((res) => res.json())
            .then((res) => console.log(res))
    }, [])

    return (
        <>
            <Header/>
            <Container>
                <Grid
                container
                justifyContent={'center'}
                alignItems={'center'}
                direction={'column'}>
                    {tickers && tickers.map((item, index) => {
                        return (<div key={index}>
                            {item.code}
                        </div>)
                    })}
                    <Button onClick={getAusTickers}>
                        Submit button
                    </Button>
                </Grid>
            </Container>

        </>

    )
}

export default Homepage;