import React, { useContext, useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import Button from '@mui/material/Button'
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Grid, TextField } from '@mui/material'
import { FetchFunction } from '../FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'

const CreateList = (props) => {
  const [openDialog, setOpenDialog] = useState(false)

  const [listName, setListName] = useState('')

  const { userId } = useContext(ClientContext)

  const [disableSubmit, setDisabledSubmit] = useState(true)

  const controlDisabled = () => {
    if (listName !== '') {
      setDisabledSubmit(false)
    } else {
      setDisabledSubmit(true)
    }
  }

  useEffect(() => {
    controlDisabled()
  }, [listName])

  const submitForm = () => {
    FetchFunction('POST', `${props.listRoute}/${userId}/${listName}`, null)
      .then(() => {
        setListName('')
        setOpenDialog(false)
      })
      .catch(error => {
        alert(error)
      })
  }

  return (
    <>
      <Grid item>
        <Button onClick={() => setOpenDialog(true)} variant={'contained'}>
          {props.buttonText}
        </Button>
      </Grid>

      <Dialog open={openDialog}>
        <DialogTitle>
          {props.dialogTitle}
        </DialogTitle>

        <DialogContent>
          <DialogContentText>
            {props.dialogContent}
          </DialogContentText>

          <TextField autoFocus
                     fullWidth
                     id={'portfolio_name'}
                     label={props.textFieldLabel}
                     margin={'dense'}
                     onChange={(e) => setListName(e.target.value)}
                     type={'text'}
                     value={listName}
                     variant={'standard'}
          />

          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button disabled={disableSubmit} onClick={submitForm}>Add</Button>
          </DialogActions>
        </DialogContent>

      </Dialog>

    </>
  )
}

CreateList.propTypes = {
  buttonText: PropTypes.string,
  dialogTitle: PropTypes.string,
  dialogContent: PropTypes.string,
  textFieldLabel: PropTypes.string,
  listID: PropTypes.string,
  listRoute: PropTypes.string
}

export default CreateList
