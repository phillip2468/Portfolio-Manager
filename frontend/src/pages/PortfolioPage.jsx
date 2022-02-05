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
import { ClientContext } from '../store/StoreCredentials'
import { FetchFunction } from '../components/FetchFunction'
import Button from '@mui/material/Button'

const PortfolioPage = () => {
  const { userId } = useContext(ClientContext)

  const [listOfPortfolios, setListOfPortfolios] = useState([])

  const [selectedPortfolio, setSelectedPortfolio] = useState('')

  const [listOfStocks, setListOfStocks] = useState([])

  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (userId !== null) {
      FetchFunction('GET', `portfolio/${userId}`, null)
        .then(res => setListOfPortfolios(res))
        .catch(res => console.log(res))
    }
  }, [userId])

  const getStocksFromPortfolio = (portfolioName) => {
    FetchFunction('GET', `portfolio/${userId}/${portfolioName}`)
      .then(res => setListOfStocks(res))
      .catch(error => console.log(error))
  }

  const columns = [
    {
      name: 'symbol',
      selector: row => row.stock_details.symbol
    },
    {
      name: 'exchange',
      selector: row => row.stock_details.exchange
    },
    {
      name: 'Name',
      selector: row => row.stock_details.stock_name,
      compact: true
    },
    {
      name: 'price',
      selector: row => row.stock_details.market_current_price,
      compact: true
    },
    {
      name: 'change %',
      selector: row => row.stock_details.market_change_percentage,
      compact: true,
      format: row => (row.stock_details.market_change_percentage * 100).toFixed(2)
    },
    {
      name: 'Unit price',
      selector: row => row.units_price,
      compact: true
    },
    {
      name: 'Units purchased',
      selector: row => row.units_purchased
    }
  ]

  console.log(listOfStocks)

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
              onChange={(e) => {
                setSelectedPortfolio(e.target.value)
                getStocksFromPortfolio(e.target.value)
              }}
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
          data={listOfStocks}
          highlightOnHover={true}
          pointerOnHover={true}
          theme={'dark'}
          title={`${selectedPortfolio} portfolio's`}
        />
      </Grid>
    </>
  )
}

export default PortfolioPage
