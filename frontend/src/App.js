import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Homepage from "./pages/Homepage";
import {createTheme, Paper, ThemeProvider, useMediaQuery} from "@mui/material";
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
        <ThemeProvider className="App" theme={theme}>
            <Paper style={{minHeight: "100vh"}}>
                <Router>
                    <Routes>
                        <Route exact path={'/'} element={<Homepage/>}/>
                    </Routes>
                </Router>
            </Paper>
        </ThemeProvider>
    );
}

export default App;
