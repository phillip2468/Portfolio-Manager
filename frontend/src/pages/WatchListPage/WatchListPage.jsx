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
import Button from '@mui/material/Button'
import { useContext, useEffect, useState } from 'react'
import { FetchFunction } from '../../components/FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'

const WatchListPage = () => {
  const [openWLDialog, setOpenWLDialog] = useState(false)

  const [listOfWL, setListOfWL] = useState([])

  const [selectedWL, setSelectedWL] = useState('')

  const { userId } = useContext(ClientContext)

  useEffect(() => {
    if (userId !== null) {
      FetchFunction('GET', `watchlist/${userId}`, null)
        .then(res => setListOfWL(res))
        .catch(error => console.log(error))
    }
  }, [userId])

  return (
    <>
      <Grid item>
        <Typography align={'center'} variant={'h5'}>
          Watchlist page
        </Typography>
      </Grid>

      <Grid item>
        <Grid container justifyContent={'center'}>
          <Button onClick={() => setOpenWLDialog(true)} variant={'contained'}>
            Create a new watchlist
          </Button>
        </Grid>
      </Grid>

      <Dialog onClose={() => setOpenWLDialog(false)} open={openWLDialog}>
        <DialogTitle>
          Create a new watchlist
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter a title for your watchlist here
          </DialogContentText>

          <TextField autoFocus
                     fullWidth
                     id={'watchlist_name'}
                     label={'Watchlist name'}
                     margin={'dense'}
                     type={'text'}
                     variant={'standard'}/>

          <DialogActions>
            <Button onClick={() => setOpenWLDialog(false)}>Cancel</Button>
            <Button onClick={() => setOpenWLDialog(false)}>Add</Button>
          </DialogActions>
        </DialogContent>
      </Dialog>

      <Grid item>
        <Grid container direction={'row'} justifyContent={'center'} spacing={2}>
          <Select
            displayEmpty
            onChange={(e) => setSelectedWL(e.target.value)}
            renderValue={(selected) => {
              if (selected.length === 0) {
                return <em>Select a portfolio</em>
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

    </>
  )
}

export default WatchListPage
