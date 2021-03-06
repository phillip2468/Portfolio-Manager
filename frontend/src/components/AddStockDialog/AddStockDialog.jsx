import { Autocomplete, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material'
import Button from '@mui/material/Button'
import * as PropTypes from 'prop-types'
import { FetchFunction } from '../FetchFunction'
import { useEffect, useState } from 'react'

const AddStockDialog = (props) => {
  const [searchValue, setSearchValue] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [selectedStock, setSelectedStock] = useState([])

  useEffect(() => {
    if (searchValue !== '') {
      FetchFunction('GET', `search/${searchValue}`, null)
        .then(res => setSuggestions(res))
    }
  }, [searchValue])

  const handleSubmit = () => {
    FetchFunction('POST', `${props.route}/${props.userId}/${props.selectedItem}/${selectedStock.stock_id}`)
      .then(() => {
        return props.onClose()
      })
      .catch((error) => {
        alert(error.msg)
      })
  }

  return <Dialog onClose={() => {
    setSearchValue('')
    setSelectedStock([])
    props.onClose()
  }} open={props.open}>
    <DialogTitle>Add a new stock to {props.selectedItem}</DialogTitle>
    <DialogContent>
      <Autocomplete
        getOptionLabel={(option) => `${option.symbol} - ${option.stock_name}`}
        onChange={(event, value) => setSelectedStock(value)}
        options={suggestions}
        renderInput={(params) => <TextField {...params} label="Stock" onChange={e => {
          if (e.target.value !== '') {
            setSearchValue(e.target.value)
          }
        }
        }/>}
        sx={{ width: '500px', paddingTop: '10px' }}
      />
    </DialogContent>
    <DialogActions>
      <Button onClick={() => {
        setSearchValue('')
        setSelectedStock([])
        props.onClose()
      }}>Cancel</Button>
      <Button disabled={typeof selectedStock.stock_id !== 'number'} onClick={handleSubmit}>Add stock</Button>
    </DialogActions>
  </Dialog>
}

AddStockDialog.propTypes = {
  route: PropTypes.string,
  onClose: PropTypes.func,
  open: PropTypes.bool,
  selectedItem: PropTypes.string,
  userId: PropTypes.number
}

export default AddStockDialog
