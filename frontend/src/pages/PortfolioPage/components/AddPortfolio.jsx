import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material'
import Button from '@mui/material/Button'
import * as PropTypes from 'prop-types'

function AddPortfolio (props) {
  return <Dialog onClose={props.onClose} open={props.open}>
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
        <Button onClick={props.onClose}>Cancel</Button>
        <Button onClick={props.onClick}>Add</Button>
      </DialogActions>
    </DialogContent>
  </Dialog>
}

AddPortfolio.propTypes = {
  onClose: PropTypes.func,
  open: PropTypes.bool,
  onClick: PropTypes.func
}

export default AddPortfolio
