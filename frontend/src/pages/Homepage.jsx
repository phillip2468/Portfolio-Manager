import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import Button from "@mui/material/Button";
import {useNavigate} from "react-router-dom";

const Homepage = () => {

    const navigate = useNavigate();
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

            <Button onClick={()=> navigate("/predict")}>
                Here
            </Button>

        </Grid>

    )
}

export default Homepage;