import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Homepage from "./pages/Homepage";
import StockPage from "./pages/StockPage"
import {createTheme, Paper, ThemeProvider} from "@mui/material";
import {useMemo} from "react";

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
                        <Routes>
                            <Route exact path={'/'} element={<Homepage/>}/>
                            <Route path={'/:stockName'} element={<StockPage/>}/>
                        </Routes>
                </Paper>
            </ThemeProvider>
        </Router>
    );
}

export default App;
