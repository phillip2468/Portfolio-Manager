import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid, InputLabel, MenuItem, Select,
  TextField,
  Typography
} from '@mui/material'
import DataTable from 'react-data-table-component'
import { useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ClientContext } from '../store/StoreCredentials'
import { FetchFunction } from '../components/FetchFunction'
import Button from '@mui/material/Button'

const PortfolioPage = () => {
  const navigate = useNavigate()

  const [popularStocks, setPopularStocks] = useState([])
  const { userId } = useContext(ClientContext)

  // eslint-disable-next-line no-unused-vars
  const [listOfPortfolios, setListOfPortfolios] = useState([])

  const [selectedPortfolio, setSelectedPortfolio] = useState('')

  // eslint-disable-next-line no-unused-vars
  const [listOfStocks, setListOfStocks] = useState([])

  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (userId !== null) {
      FetchFunction('GET', `portfolio/${userId}`, null)
        .then(res => setListOfPortfolios(res))
        .catch(res => console.log(res))
    }
  }, [userId])

  useEffect(() => {
    fetch('/actively-traded')
      .then((res) => res.json())
      .then((res) => {
        setPopularStocks(res)
      })
  }, [])

  // eslint-disable-next-line no-unused-vars
  const getStocksFromPortfolio = (portfolioName) => {
    FetchFunction('GET', `portfolio/${userId}/${portfolioName}`)
      .then(res => setListOfStocks(res))
      .catch(error => console.log(error))
  }

  const columns = [
    {
      name: 'symbol',
      selector: row => row.symbol,
      width: '100px'
    },
    {
      name: 'Name',
      selector: row => row.stock_name,
      compact: true,
      width: '250px'
    },
    {
      name: 'price',
      selector: row => row.market_current_price,
      compact: true,
      width: '100px'
    },
    {
      name: 'change %',
      selector: row => row.market_change_percentage,
      compact: true,
      width: '100px',
      format: row => (row.market_change_percentage * 100).toFixed(2)
    }
  ]

  return (
    <>
      <Grid item>
        <Typography align={'center'} variant={'h5'}>
          Portfolio page
        </Typography>
      </Grid>

      <Grid item>
        <Grid container justifyContent={'center'}>
          <Button onClick={() => setOpen(true)} variant={'contained'}>
            Create a new watchlist
          </Button>
        </Grid>
      </Grid>

      <Dialog onClose={() => setOpen(false)} open={open}>
        <DialogTitle>
          Add a new portfolio
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter a title for your portfolio here
          </DialogContentText>

          <TextField autoFocus
          fullWidth
          id={'portfolio_name'}
          label={'Portfolio name'}
          margin={'dense'}
          type={'text'}
          variant={'standard'}/>

          <DialogActions>
            <Button onClick={() => setOpen(false)}>Cancel</Button>
            <Button onClick={() => setOpen(true)}>Add</Button>
          </DialogActions>
        </DialogContent>
      </Dialog>

      <Grid item>
        <Grid container direction={'row'} justifyContent={'center'} spacing={2}>
          <Grid item>
            <InputLabel id="demo-simple-select-label">Select a portfolio here</InputLabel>
          </Grid>

          <Grid item>
            <Select
              autoWidth={true}
              onChange={(e) => setSelectedPortfolio(e.target.value)}
              value={selectedPortfolio}
            >
              {
                listOfPortfolios.map(element =>
                  <MenuItem
                    key={element.portfolio_name}
                    value={element.portfolio_name}
                  >
                    {element.portfolio_name}
                  </MenuItem>
                )}
            </Select>
          </Grid>

        </Grid>
      </Grid>

      <Grid item>
        <DataTable
          columns={columns}
          data={popularStocks}
          dense={true}
          highlightOnHover={true}
          onRowClicked={(row) => navigate(`/${row.symbol}`)}
          pointerOnHover={true}
          striped={true}
          theme={'dark'}
          title={'Popular stocks today'}
        />
      </Grid>
    </>
  )
}

export default PortfolioPage
