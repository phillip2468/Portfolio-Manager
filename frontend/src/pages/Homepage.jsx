import {Container, Grid, TextField} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import SearchIcon from '@mui/icons-material/Search';
import styled from "styled-components"

const StyledInput = styled(TextField)`
  fieldset {
    border-radius: 2em;
  }
`

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
                    <StyledInput
                        placeholder={"Search for stocks"}
                        fullWidth={true}
                        InputProps={{
                            startAdornment: <SearchIcon position="start" style={{paddingRight: "10px"}}/>,
                        }}
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