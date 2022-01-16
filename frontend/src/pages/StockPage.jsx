import {useParams} from "react-router-dom";

const StockPage = () => {
    const {stockName} = useParams()
    return (
        <div>
            {stockName}
        </div>
    )
}

export default StockPage;