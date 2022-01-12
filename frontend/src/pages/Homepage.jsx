import {Container, Grid} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import SearchIcon from '@mui/icons-material/Search';
import styled from "styled-components";


const Homepage = () => {
    const data = [
        {
            key: "john",
            value: "John Doe",
        },
        {
            key: "jane",
            value: "Jane Doe",
        },
        {
            key: "mary",
            value: "Mary Phillips",
        },
        {
            key: "robert",
            value: "Robert",
        },
        {
            key: "karius",
            value: "Karius",
        },
    ];
    return (
        <Grid container spacing={2} direction={"column"}>
            <Grid item>
                <Header/>
            </Grid>

            <Grid item>
                <Container maxWidth={'xs'}>
                    <div style={{display: "flex"}}>
                        <input
                            placeholder={"Search for stocks"}
                            style={{flex: 1, fontSize: "large"}}
                        />
                    </div>
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