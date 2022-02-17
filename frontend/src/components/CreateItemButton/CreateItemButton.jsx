import React from 'react'
import PropTypes from 'prop-types'
import { Grid } from '@mui/material'
import Button from '@mui/material/Button'

CreateItemButton.propTypes = {
  text: PropTypes.string,
  onClick: PropTypes.func
}

function CreateItemButton (props) {
  return (
    <div>
      <Grid container justifyContent={'center'}>
        <Button data-testid={'CreateItemButton'} onClick={props.onClick} variant={'contained'}>
          {props.text}
        </Button>
      </Grid>
    </div>
  )
}

export default CreateItemButton
