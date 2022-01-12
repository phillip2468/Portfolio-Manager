import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import SearchBar from "../components/SearchBar";

const Homepage = () => {

    const data = [
        {
            key: "Hi",
            value: "there",
        },
        {
            key: "John",
            value: "Smite"
        },
        {
            key: "Sam",
            value: "Meloma"
        }
    ]

    return (
        <Grid container spacing={2} direction={"column"}>
            <Grid item>
                <Header/>
            </Grid>

            <Grid item>
                <Container>
                    <SearchBar
                        placeholder={"Search for stocks"}
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