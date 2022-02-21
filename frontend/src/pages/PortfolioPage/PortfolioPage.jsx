import { Grid } from '@mui/material'
import { useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { ClientContext } from '../../store/StoreCredentials'
import { FetchFunction } from '../../components/FetchFunction'
import Button from '@mui/material/Button'
import AddStockDialog from '../../components/AddStockDialog'
import TableOfStocks from '../../components/TableOfStocks'
import Columns from './components/Columns'
import Title from '../../components/Title/Title'
import CreateList from '../../components/CreateList/CreateList'
import CurrentList from '../../components/CurrentList/CurrentList'

const PortfolioPage = () => {
  const { userId } = useContext(ClientContext)

  const [openListDialog, setOpenListDialog] = useState(false)

  const [listOfPortfolios, setListOfPortfolios] = useState([])

  const [selectedPortfolio, setSelectedPortfolio] = useState('')

  const [listOfStocks, setListOfStocks] = useState([])

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
  }, [userId, openListDialog])

  useEffect(() => {
    if (selectedPortfolio !== '') {
      getStocksFromPortfolio(selectedPortfolio)
    }
  }, [selectedPortfolio, stockDialogOpen])

  // noinspection JSValidateTypes
  return (
    <>
      <Grid item>
        <Title title={'Portfolio page'}/>
      </Grid>

      <Grid item>
        <Grid container justifyContent={'center'}>
          <CreateList
            buttonText={'Create a new portfolio'}
            dialogContent={'Enter a title for your portfolio here'}
            dialogOpen={openListDialog}
            dialogTitle={'Add a new portfolio'}
            listRoute={'portfolio'}
            setDialogOpen={setOpenListDialog}
            textFieldLabel={'Portfolio name'}
          />
        </Grid>
      </Grid>

      <AddStockDialog onClose={() => setStockDialogOpen(false)} open={stockDialogOpen}
                      route={'portfolio'} selectedItem={selectedPortfolio} userId={userId}/>

      <Grid item>
        <CurrentList
          currentValue={selectedPortfolio}
          iterateValue={'portfolio_name'}
          listOfValues={listOfPortfolios}
          setCurrentValue={setSelectedPortfolio}
        />
      </Grid>

      <Grid item>
        <TableOfStocks actions={renderAddStock()} clearSelectedRows={toggleCleared} columns={columns}
                       contextActions={contextActions} data={listOfStocks} onSelectedRowsChange={handleRowsSelected}
                       selectedItem={selectedPortfolio}/>
      </Grid>
    </>
  )
}

export default PortfolioPage
