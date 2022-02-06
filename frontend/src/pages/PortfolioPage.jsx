import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid,
  MenuItem,
  Select,
  TextField,
  Typography
} from '@mui/material'
import DataTable from 'react-data-table-component'
import { useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { ClientContext } from '../store/StoreCredentials'
import { FetchFunction } from '../components/FetchFunction'
import Button from '@mui/material/Button'
import AddStockDialog from '../components/AddStockDialog'
import { Link } from 'react-router-dom'

function findById (array, id) {
  return array.findIndex((d) => d.portfolio_id === id)
}

const PortfolioPage = () => {
  const { userId } = useContext(ClientContext)

  const [listOfPortfolios, setListOfPortfolios] = useState([])

  const [selectedPortfolio, setSelectedPortfolio] = useState('')

  const [listOfStocks, setListOfStocks] = useState([])

  const [open, setOpen] = useState(false)

  const [selectedRows, setSelectedRows] = useState([])

  const [toggleCleared, setToggleCleared] = useState(false)

  const [stockDialogOpen, setStockDialogOpen] = useState(false)

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

  useEffect(() => {
    if (selectedPortfolio !== '') {
      getStocksFromPortfolio(selectedPortfolio)
    }
  }, [selectedPortfolio, stockDialogOpen])

  const columns = useMemo(() => {
    const handleCellEditable = (field) => (row) => (e) => {
      if (e.target.value >= 0) {
        const newRow = { ...row }
        newRow[field] = e.target.value

        const newData = listOfStocks.slice(0)
        newData[findById(listOfStocks, row.portfolio_id)] = newRow
        setListOfStocks(newData)

        const body = {
          units_price: newRow.units_price,
          units_purchased: newRow.units_purchased
        }
        FetchFunction('PATCH', `portfolio/${userId}/${newRow.portfolio_name}/${newRow.stock_details.stock_id}`, body)
          .then(res => console.log(res))
          .catch(error => alert(error))
      }
    }

    return [
      {
        name: 'symbol',
        selector: row => row.stock_details.symbol,
        sortable: true,
        cell: row => <Link target="_blank" to={`/${row.stock_details.symbol}`}>{row.stock_details.symbol}</Link>
      },
      {
        name: 'exchange',
        selector: row => row.stock_details.exchange,
        sortable: true
      },
      {
        name: 'Name',
        selector: row => row.stock_details.stock_name,
        wrap: true,
        sortable: true
      },
      {
        name: 'Last',
        selector: row => row.stock_details.market_current_price,
        sortable: true
      },
      {
        name: 'Currency',
        selector: row => row.stock_details.currency,
        sortable: true
      },
      {
        name: 'Todays change %',
        selector: row => row.stock_details.market_change_percentage,
        sortable: true,
        format: row => (row.stock_details.market_change_percentage * 100).toFixed(2)
      },
      {
        name: 'Unit price',
        selector: row => row.units_price,
        sortable: true,
        cell: (row) => (
          <TextField
            onChange={handleCellEditable('units_price')(row)}
            value={row.units_price}
          />
        )
      },
      {
        name: 'Units',
        selector: row => row.units_purchased,
        sortable: true,
        cell: (row) => (
          <TextField
               onChange={handleCellEditable('units_purchased')(row)}
               value={row.units_purchased}
               />
        )
      },
      {
        name: 'Value',
        selector: row => (row.units_purchased * row.units_price),
        sortable: true,
        format: row => ((parseFloat(row.units_purchased) * row.units_price).toFixed(2))
      },
      {
        name: 'Change %',
        selector: row => (100 - ((row.stock_details.market_current_price / row.units_price) * 100)),
        sortable: true,
        format: row => (100 - ((row.stock_details.market_current_price / row.units_price) * 100)).toFixed(2)
      }
    ]
  }, [listOfStocks])

  const handleRowsSelected = useCallback(state => {
    setSelectedRows(state.selectedRows)
  }, [])

  const contextActions = useMemo(() => {
    const handleDelete = () => {
      let newData = { ...listOfStocks }
      const listOfIds = Object.values(selectedRows).map(item => item.stock_details.stock_id)
      console.log(listOfIds)

      const promises = listOfIds.map(id =>
        FetchFunction('DELETE', `portfolio/${userId}/${selectedPortfolio}/${id}`, null)
      )
      Promise.all(promises).then(results => console.log(results))

      newData = Object.values(newData).filter(item => !selectedRows.includes(item))
      setListOfStocks(newData)
      setToggleCleared(!toggleCleared)
    }

    return (
      <Button onClick={handleDelete} style={{ background: 'darkred' }} variant={'contained'}>Delete</Button>
    )
  }, [listOfStocks, selectedRows, toggleCleared])

  const renderAddStock = () => {
    if (selectedPortfolio) {
      return (
        <Button
          onClick={() => setStockDialogOpen(true)}
          variant={'outlined'}>Add a new stock</Button>
      )
    }
  }

  // noinspection JSValidateTypes
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

      <AddStockDialog onClose={() => setStockDialogOpen(false)} open={stockDialogOpen}
                      selectedPortfolio={selectedPortfolio} userId={userId}/>
      <Grid item>
        <Grid container direction={'row'} justifyContent={'center'} spacing={2}>
          <Select
            displayEmpty
            onChange={(e) => {
              setSelectedPortfolio(e.target.value)
            }}
            renderValue={(selected) => {
              if (selected.length === 0) {
                return <em>Select a portfolio</em>
              }
              return selected
            }}
            sx={{ width: '150px', paddingLeft: '10px' }}
            value={selectedPortfolio}
            variant={'standard'}
          >
            <MenuItem disabled value="">
              <em>Select...</em>
            </MenuItem>
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

      <Grid item>
        <DataTable
          actions={renderAddStock()}
          clearSelectedRows={toggleCleared}
          columns={columns}
          contextActions={contextActions}
          data={listOfStocks}
          highlightOnHover={true}
          onSelectedRowsChange={handleRowsSelected}
          pagination={true}
          pointerOnHover={true}
          selectableRows={true}
          subHeaderAlign={'center'}
          theme={'dark'}
          title={`${selectedPortfolio} portfolio's`}
        />
      </Grid>
    </>
  )
}

export default PortfolioPage
