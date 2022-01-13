import {Container, Grid, TextField} from "@mui/material";
import Header from "../components/Header";
import TrendingTable from "../components/TrendingTable";
import SearchBar from "../components/SearchBar";

const StyledInput = styled(TextField)`
  fieldset {
    border-radius: 2em;
  }
`
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
                    <SearchBar
                        placeholder={"Search for stocks"}
                        data={data}
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