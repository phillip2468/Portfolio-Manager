import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Homepage from "./pages/Homepage";
import StockPage from "./pages/StockPage/StockPage"
import {Container, createTheme, Grid, Paper, ThemeProvider} from "@mui/material";
import {useMemo} from "react";
import Header from "./components/Header/Header";
import LoginPage from "./pages/LoginPage";
import {ClientWrapper} from "./store/StoreCredentials";

function App() {

    const theme = useMemo(
        () =>
            createTheme({
                palette: {
                    mode: 'dark'
                },
            }),
        [],
    );
    return (
        <ClientWrapper>
            <Router>
                <ThemeProvider theme={theme}>
                    <Paper style={{minHeight: "150vh"}}>
                        <Grid container spacing={4} direction={"column"}>

                            <Grid item>
                                <Header/>
                            </Grid>

                            <Grid item>
                                <Container maxWidth={"lg"} sx={{border: "1px solid white"}}>
                                    <Grid container spacing={4} direction={"column"}>
                                        <Routes>
                                            <Route exact path={'/'} element={<Homepage/>}/>
                                            <Route path={'/:stockName'} element={<StockPage/>}/>
                                            <Route path={'/login'} element={<LoginPage/>}/>
                                        </Routes>
                                    </Grid>
                                </Container>
                            </Grid>

                        </Grid>
                    </Paper>
                </ThemeProvider>
            </Router>
        </ClientWrapper>
    );
}

export default App;
