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
    if (listName === '') {
      setDisabledSubmit(true)
    } else {
      setDisabledSubmit(false)
    }
  }

  useEffect(() => {
    controlDisabled()
  }, [listName])

  const submitForm = () => {
    FetchFunction('POST', `${props.listRoute}/${userId}/${listName}`, null)
      .then(() => {
        setListName('')
        props.setDialogOpen(false)
      })
      .catch(error => {
        alert(error)
      })
  }

  return (
    <>
      <Grid item>
        <Button onClick={() => props.setDialogOpen(true)} variant={'contained'}>
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
                     data-testid={'CreateListText'}
                     fullWidth
                     label={props.textFieldLabel}
                     margin={'dense'}
                     onChange={(e) => setListName(e.target.value)}
                     type={'text'}
                     value={listName}
                     variant={'standard'}
          />

          <DialogActions>
            <Button onClick={() => props.setDialogOpen(false)}>Cancel</Button>
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
  listRoute: PropTypes.string,
  dialogOpen: PropTypes.bool,
  setDialogOpen: PropTypes.func
}

export default CreateList
