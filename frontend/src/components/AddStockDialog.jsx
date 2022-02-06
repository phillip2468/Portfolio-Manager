import {
  Autocomplete,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField
} from '@mui/material'
import Button from '@mui/material/Button'
import * as PropTypes from 'prop-types'
import { FetchFunction } from './FetchFunction'
import { useEffect, useState } from 'react'

const AddStockDialog = (props) => {
  const [value, setValue] = useState('A')
  const [suggestions, setSuggestions] = useState([])

  useEffect(() => {
    FetchFunction('GET', `search/${value}`, null)
      .then(res => setSuggestions(res))
      .catch(error => console.log(error))
  }, [value])

  return <Dialog onClose={props.onClose} open={props.open}>
    <DialogTitle>Add a new stock to {props.selectedPortfolio}</DialogTitle>
    <DialogContent>
      <Autocomplete
        getOptionLabel={(option) => option.stock_name}
        onChange={(event, value) => console.log(event)}
        options={suggestions}
        renderInput={(params) => <TextField {...params} label="Movie" onChange={e => {
          if (e.target.value !== '' || e.target.value !== null) {
            setValue(e.target.value)
          }
        }
        }/>}
        sx={{ width: '200px', paddingTop: '10px' }}
      />
    </DialogContent>
    <DialogActions>
      <Button onClick={props.onClose}>Cancel</Button>
      <Button onClick={props.onClose}>Add stock</Button>
    </DialogActions>
  </Dialog>
}

AddStockDialog.propTypes = {
  onClose: PropTypes.func,
  open: PropTypes.bool,
  selectedPortfolio: PropTypes.string
}

export default AddStockDialog
