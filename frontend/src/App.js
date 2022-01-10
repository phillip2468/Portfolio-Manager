import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
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
                <BrowserRouter>
                    <Routes>
                        <Route exact path={'/'} element={<Homepage/>}/>
                        <Route path={'/predict'} element={<PredictorPage/>}/>
                    </Routes>
                </BrowserRouter>
            </Paper>
        </ThemeProvider>
    );
}

export default App;
