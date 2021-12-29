import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";

const Homepage = () => {

    return (
        <Grid container spacing={2} direction={"column"}>
            <Grid item>
                <Header/>
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