import {useState} from "react";
import Button from '@mui/material/Button';

const Homepage = () => {

    const [tickers, setTickers] = useState(undefined)

    const getAusTickers = () => {
        fetch('/aus_tickers')
            .then((res) => setTickers(res))
    }

    return (
        <div>
            <Button onClick={getAusTickers}>
                Submit button
            </Button>
            {tickers !== undefined && tickers.map((index, item) => {
                return (
                    <div key={index}>
                        <div>
                            {item.ticker}
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

export default Homepage;