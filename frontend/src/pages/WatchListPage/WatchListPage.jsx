import { Grid, MenuItem, Select } from '@mui/material'
import Button from '@mui/material/Button'
import { useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { FetchFunction } from '../../components/FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'
import TableOfStocks from '../../components/TableOfStocks/TableOfStocks'
import AddStockDialog from '../../components/AddStockDialog/AddStockDialog'
import Columns from './components/Columns'
import Title from '../../components/Title/Title'
import CreateList from '../../components/CreateList/CreateList'

const WatchListPage = () => {
  const { userId } = useContext(ClientContext)

  const [openListDialog, setOpenListDialog] = useState(false)

  const [listOfWL, setListOfWL] = useState([])

  const [selectedWL, setSelectedWL] = useState('')

  const [listOfStocks, setListOfStocks] = useState([])

  const [selectedRows, setSelectedRows] = useState([])

  const [toggleCleared, setToggleCleared] = useState(false)

  const [stockDialogOpen, setStockDialogOpen] = useState(false)

  useEffect(() => {
    if (userId !== null) {
      FetchFunction('GET', `watchlist/${userId}`, null)
        .then(res => setListOfWL(res))
        .catch(error => console.log(error))
    }
  }, [userId, openListDialog])

  useEffect(() => {
    if (selectedWL !== '') {
      FetchFunction('GET', `watchlist/${userId}/${selectedWL}`, null)
        .then(res => setListOfStocks(res))
        .catch(error => console.log(error))
    }
  }, [selectedWL, stockDialogOpen, openListDialog])

  const columns = Columns(listOfStocks)

  const renderAddStock = () => {
    if (selectedWL) {
      return (
        <Button
          onClick={() => setStockDialogOpen(true)}
          variant={'outlined'}>Add a new stock</Button>
      )
    }
  }

  const handleRowsSelected = useCallback(state => {
    setSelectedRows(state.selectedRows)
  }, [])

  const contextActions = useMemo(() => {
    const handleDelete = () => {
      let newData = { ...listOfStocks }
      const listOfIds = Object.values(selectedRows).map(item => item.stock_details.stock_id)

      const promises = listOfIds.map(id =>
        FetchFunction('DELETE', `watchlist/${userId}/${selectedWL}/${id}`, null)
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

  return (
    <>
      <Grid item>
        <Title title={'Watchlist page'}/>
      </Grid>

      <Grid item>
        <Grid container justifyContent={'center'}>
          <CreateList
            buttonText={'Create a new watchlist'}
            dialogContent={'Enter a title for your watchlist here'}
            dialogOpen={openListDialog}
            dialogTitle={'Add a new watchlist'}
            listRoute={'watchlist'}
            setDialogOpen={setOpenListDialog}
            textFieldLabel={'Watchlist name'}
          />
        </Grid>
      </Grid>

      <AddStockDialog
        onClose={() => setStockDialogOpen(false)}
        open={stockDialogOpen}
        route={'watchlist'}
        selectedItem={selectedWL}
        userId={userId}
      />

      <Grid item>
        <Grid container direction={'row'} justifyContent={'center'} spacing={2}>
          <Select
            displayEmpty
            onChange={(e) => setSelectedWL(e.target.value)}
            renderValue={(selected) => {
              if (selected.length === 0) {
                return <em>Select a watchlist</em>
              }
              return selected
            }}
            sx={{ width: '210px' }}
            value={selectedWL}
            variant={'standard'}
          >
            <MenuItem disabled value="">
              <em>Select...</em>
            </MenuItem>
            {
              listOfWL.map(element =>
                <MenuItem
                  key={element.watchlist_name}
                  value={element.watchlist_name}
                >
                  {element.watchlist_name}
                </MenuItem>
              )}
          </Select>
        </Grid>
      </Grid>

      <Grid item>
        <TableOfStocks
          actions={renderAddStock()}
          clearSelectedRows={toggleCleared}
          columns={columns}
          contextActions={contextActions}
          data={listOfStocks}
        onSelectedRowsChange={handleRowsSelected}
        selectedItem={selectedWL}/>
      </Grid>

    </>
  )
}

export default WatchListPage
