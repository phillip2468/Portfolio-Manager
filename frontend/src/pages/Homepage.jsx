import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
//import TrendingTable from "../components/TrendingTable";
import SearchBar from "../components/SearchBar/SearchBar";
//import {useEffect, useState} from "react";
import PopularStocksTable from "../components/PopularStocksTable";


const Homepage = () => {

    return (
        <Grid container spacing={2} direction={"column"}>
            <Grid item>
                <Header/>
            </Grid>

            <Grid item sx={{position: "relative"}}>
                <SearchBar
                    placeholder={"Search for stocks"}
                />
            </Grid>

            <Grid item>
                <Container sx={{width: "600px"}}>
                    <PopularStocksTable/>
                </Container>
            </Grid>

            <Grid item>
                <Container>
                </Container>
            </Grid>

        </Grid>

    )
}

export default Homepage;