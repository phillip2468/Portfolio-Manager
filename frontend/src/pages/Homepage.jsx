import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import SearchBar from "../components/SearchBar";
import {useEffect, useState} from "react";
import DataTable from "react-data-table-component"
import styled from "styled-components"


const TrendingStocks = styled.div`
  display: flex;
  flex-direction: column;
`

const Homepage = () => {
    const [allStocks, setAllStocks] = useState([])

    const [popularStocks, setPopularStocks] = useState([])

    useEffect(()=> {
            fetch('/quote/search')
                .then((res) => res.json())
                .then((res) => {
                    setAllStocks(Object.values(res))
                })
        }
    , [])

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
        <Grid container spacing={2} direction={"column"}>
            <Grid item>
                <Header/>
            </Grid>

            <Grid item sx={{position: "relative"}}>
                <SearchBar
                    placeholder={"Search for stocks"}
                    data={allStocks}
                />
            </Grid>

            <Grid item>
                <Container sx={{width: "600px"}}>
                    <DataTable
                        title={"Popular stocks today"}
                        striped={true}
                        dense={true}
                        highlightOnHover={true}
                        theme={"dark"}
                        columns={columns}
                        data={popularStocks}
                    />
                </Container>
            </Grid>

            <Grid item>
                <Container>
                   <TrendingTable/>
                </Container>
            </Grid>

        </Grid>

    )
}

export default Homepage;