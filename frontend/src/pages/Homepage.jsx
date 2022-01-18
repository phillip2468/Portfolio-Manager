import {Container, Grid} from "@mui/material";
import SearchBar from "../components/SearchBar/SearchBar";
import PopularStocksTable from "../components/PopularStocksTable/PopularStocksTable";


const Homepage = () => {

    return (
        <>
            <Grid item sx={{position: "relative"}}>
                <SearchBar placeholder={"Search for stocks"}/>
            </Grid>

            <Grid item>
                <Container sx={{width: "52%"}}>
                    <PopularStocksTable/>
                </Container>
            </Grid>
        </>
    )
}

export default Homepage;