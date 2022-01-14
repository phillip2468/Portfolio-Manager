import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import SearchBar from "../components/SearchBar";
import {useEffect, useState} from "react";

const Homepage = () => {
    const [allStocks, setAllStocks] = useState([])

    useEffect(()=> {
            fetch('/quote/search')
                .then((res) => res.json())
                .then((res) => {
                    setAllStocks(Object.values(res))
                })
        }
    , [])

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
                <Container>
                   <TrendingTable/>
                </Container>
            </Grid>

        </Grid>

    )
}

export default Homepage;