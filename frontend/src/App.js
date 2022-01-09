import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Homepage from "./pages/Homepage";
import {createTheme, Paper, ThemeProvider} from "@mui/material";
import {useMemo} from "react";
import PredictorPage from "./pages/PredictorPage";

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
        <ThemeProvider theme={theme}>
            <Paper style={{minHeight: "150vh"}}>
                <Router>
                    <Routes>
                        <Route exact path={'/'} element={<Homepage/>}/>
                        <Route exact path={'/predict'} element={<PredictorPage/>}/>
                    </Routes>
                </Router>
            </Paper>
        </ThemeProvider>
    );
}

export default App;
