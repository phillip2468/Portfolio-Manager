import { Grid, MenuItem, Typography } from '@mui/material'
import { useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { ClientContext } from '../../store/StoreCredentials'
import { FetchFunction } from '../../components/FetchFunction'
import Button from '@mui/material/Button'
import AddStockDialog from '../../components/AddStockDialog'
import TableOfStocks from '../../components/TableOfStocks'
import Columns from './components/Columns'
import AddPortfolio from './components/AddPortfolio'
import CurrentPortfolios from './components/CurrentPortfolios'

const PortfolioPage = () => {
  const { userId } = useContext(ClientContext)

  const [listOfPortfolios, setListOfPortfolios] = useState([])

  const [selectedPortfolio, setSelectedPortfolio] = useState('')

  const [listOfStocks, setListOfStocks] = useState([])

  const [open, setOpen] = useState(false)

  const [selectedRows, setSelectedRows] = useState([])

  const [toggleCleared, setToggleCleared] = useState(false)

  const [stockDialogOpen, setStockDialogOpen] = useState(false)

  const getStocksFromPortfolio = (portfolioName) => {
    FetchFunction('GET', `portfolio/${userId}/${portfolioName}`)
      .then(res => setListOfStocks(res))
      .catch(error => console.log(error))
  }
  const columns = Columns(listOfStocks, setListOfStocks, userId)

  const handleRowsSelected = useCallback(state => {
    setSelectedRows(state.selectedRows)
  }, [])

  const contextActions = useMemo(() => {
    const handleDelete = () => {
      let newData = { ...listOfStocks }
      const listOfIds = Object.values(selectedRows).map(item => item.stock_details.stock_id)

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

  useEffect(() => {
    if (userId !== null) {
      FetchFunction('GET', `portfolio/${userId}`, null)
        .then(res => setListOfPortfolios(res))
        .catch(res => console.log(res))
    }
  }, [userId])

  useEffect(() => {
    if (selectedPortfolio !== '') {
      getStocksFromPortfolio(selectedPortfolio)
    }
  }, [selectedPortfolio, stockDialogOpen])

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

      <AddPortfolio onClick={() => setOpen(true)} onClose={() => setOpen(false)} open={open}/>

      <AddStockDialog onClose={() => setStockDialogOpen(false)} open={stockDialogOpen}
                      selectedPortfolio={selectedPortfolio} userId={userId}/>
      <Grid item>
        <CurrentPortfolios callbackfn={element =>
          <MenuItem
            key={element.portfolio_name}
            value={element.portfolio_name}
          >
            {element.portfolio_name}
          </MenuItem>} listOfPortfolios={listOfPortfolios} onChange={(e) => {
            setSelectedPortfolio(e.target.value)
          }} renderValue={(selected) => {
            if (selected.length === 0) {
              return <em>Select a portfolio</em>
            }
            return selected
          }} value={selectedPortfolio}/>
      </Grid>

      <Grid item>
        <TableOfStocks actions={renderAddStock()} clearSelectedRows={toggleCleared} columns={columns}
                       contextActions={contextActions} data={listOfStocks} onSelectedRowsChange={handleRowsSelected}
                       selectedPortfolio={selectedPortfolio}/>
      </Grid>
    </>
  )
}

export default PortfolioPage
