import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Homepage from "./pages/Homepage";
import StockPage from "./pages/StockPage"
import {createTheme, Grid, Paper, ThemeProvider} from "@mui/material";
import {useMemo} from "react";
import Header from "./components/Header/Header";

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
        <Router>
            <ThemeProvider theme={theme}>
                <Paper style={{minHeight: "150vh"}}>
                    <Grid container spacing={4} direction={"column"}>
                        <Grid item>
                            <Header/>
                        </Grid>

                        <Routes>
                            <Route exact path={'/'} element={<Homepage/>}/>
                            <Route path={'/:stockName'} element={<StockPage/>}/>
                        </Routes>
                    </Grid>
                </Paper>
            </ThemeProvider>
        </Router>
    );
}

export default App;
