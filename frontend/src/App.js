import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Homepage from './pages/Homepage'
import StockPage from './pages/StockPage/StockPage'
import { Container, createTheme, Grid, Paper, ThemeProvider } from '@mui/material'
import { useMemo } from 'react'
import Header from './components/Header/Header'
import LoginPage from './pages/LoginPage'
import { ClientWrapper } from './store/StoreCredentials'
import RegisterPage from './pages/RegisterPage'
import PortfolioPage from './pages/PortfolioPage/PortfolioPage'
import WatchListPage from './pages/WatchListPage/WatchListPage'
import TrendingPage from './pages/TrendingPage'

function App () {
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: 'dark'
        }
      }),
    []
  )
  return (
            <Router>
                <ClientWrapper>
                    <ThemeProvider theme={theme}>
                        <Paper style={{ minHeight: '150vh' }}>
                            <Grid container direction={'column'} spacing={4}>

                                <Grid item>
                                    <Header/>
                                </Grid>

                                <Grid item>
                                    <Container maxWidth={'lg'}>
                                        <Grid container direction={'column'} spacing={4}>
                                            <Routes>
                                                <Route element={<Homepage/>} exact path={'/'}/>
                                                <Route element={<StockPage/>} path={'/:stockName'}/>
                                                <Route element={<LoginPage/>} path={'/login'}/>
                                                <Route element={<RegisterPage/>} path={'/register'}/>
                                                <Route element={<PortfolioPage/>} path={'/portfolio'}/>
                                                <Route element={<WatchListPage/>} path={'/watchlist'}/>
                                                <Route element={<TrendingPage/>} path={'/trends'}/>
                                            </Routes>
                                        </Grid>
                                    </Container>
                                </Grid>

                            </Grid>
                        </Paper>
                    </ThemeProvider>
                </ClientWrapper>
            </Router>
  )
}

export default App
