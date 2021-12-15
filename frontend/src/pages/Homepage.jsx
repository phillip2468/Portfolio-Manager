import {useEffect, useState} from "react";
import Button from '@mui/material/Button';
import {Container} from "@mui/material";

const Homepage = () => {

    const [tickers, setTickers] = useState(undefined)

    const getAusTickers = async () => {
        const result = await fetch('/aus_tickers');
        const response = await result.json();
        console.log(response[0])
        setTickers(response)
    }

    useEffect(()=>{
        console.log('Mounted!')
    }, [tickers])

    return (
        <Container>
            <Button onClick={getAusTickers}>
                Submit button
            </Button>
            {tickers && tickers.map((item) => {
                return (
                    <div>
                        {item.code}
                    </div>
                )
            })}
        </Container>
    )
}

export default Homepage;