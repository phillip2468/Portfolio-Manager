import DataTable from "react-data-table-component";
import {useEffect, useState} from "react";

const PopularStocksTable = () => {

    const [popularStocks, setPopularStocks] = useState([])

    useEffect(()=> {
        fetch('/actively-traded')
            .then((res) => res.json())
            .then((res)=> {
                setPopularStocks(res)
            })
    }, [])

    const columns = [
        {
            'name': 'symbol',
            'selector': row => row.symbol,
            'width': '100px'
        },
        {
            'name': 'Name',
            'selector': row => row.stock_name,
            'compact': true,
            'width': '250px'
        }
        ,
        {
            'name': 'price',
            'selector': row => row.market_current_price,
            'compact': true,
            'width': '100px'
        },
        {
            'name': 'change %',
            'selector': row => row.market_change_percentage,
            'compact': true,
            'width': "100px",
            'format': row => (row.market_change_percentage * 100).toFixed(2)
        }
    ]

    return (
        <>
            <DataTable
                title={"Popular stocks today"}
                striped={true}
                dense={true}
                highlightOnHover={true}
                theme={"dark"}
                columns={columns}
                data={popularStocks}
            />
        </>
    )
}

export default PopularStocksTable;