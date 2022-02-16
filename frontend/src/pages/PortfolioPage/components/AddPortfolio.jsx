import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material'
import Button from '@mui/material/Button'
import * as PropTypes from 'prop-types'
import { useContext, useEffect, useState } from 'react'
import { FetchFunction } from '../../../components/FetchFunction'
import { ClientContext } from '../../../store/StoreCredentials'

function AddPortfolio (props) {
  const [pfName, setPfName] = useState('')
  const { userId } = useContext(ClientContext)

  const [disabled, setDisabled] = useState(true)

  const controlDisable = () => {
    if (pfName === '') {
      setDisabled(true)
    } else {
      setDisabled(false)
    }
  }

  useEffect(() => {
    controlDisable()
  }, [pfName])

  const submitPfName = () => {
    FetchFunction('POST', `portfolio/${userId}/${pfName}`, null)
      .then(() => props.onClick)
  }

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
                 onChange={(e) => setPfName(e.target.value)}
                 type={'text'}
                 value={pfName}
                 variant={'standard'}
      />

      <DialogActions>
        <Button onClick={props.onClose}>Cancel</Button>
        <Button disabled={disabled} onClick={submitPfName}>Add</Button>
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
