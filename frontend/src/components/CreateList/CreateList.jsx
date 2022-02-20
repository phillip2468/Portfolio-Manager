import React, { useContext, useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import Button from '@mui/material/Button'
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Grid, TextField } from '@mui/material'
import { FetchFunction } from '../FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'

const CreateList = (props) => {
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
        props.dialogOpen = true
      })
      .catch(error => {
        alert(error)
      })
  }

  const closeDialog = () => {
    props.dialogOpen = false
  }

  const openDialog = () => {
    props.dialogOpen = true
  }

  return (
    <>
      <Grid item>
        <Button onClick={openDialog} variant={'contained'}>
          {props.buttonText}
        </Button>
      </Grid>

      <Dialog open={props.dialogOpen}>
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
            <Button onClick={closeDialog}>Cancel</Button>
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
  listRoute: PropTypes.string,
  dialogOpen: PropTypes.bool
}

export default CreateList
