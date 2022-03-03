import React from 'react'
import PropTypes from 'prop-types'
import { Grid, Typography } from '@mui/material'
import Button from '@mui/material/Button'

const StockTimeButtons = props => {
  return (
    <Grid container spacing={1}>
      <Grid item>
        <Typography sx={{ textAlign: 'center' }}>{props.label}</Typography>
      </Grid>

      {props.listOfTimes.map(function (element, index) {
        return (
          <Grid item key={index}>
            <Button
              disabled={props.duration === element}
              onClick={e => props.setDuration(e.target.value)}
              size={'small'}
              value={element}
              variant={'outlined'}
            >{element}
            </Button>
          </Grid>
        )
      })}
    </Grid>
  )
}

StockTimeButtons.propTypes = {
  listOfTimes: PropTypes.arrayOf(PropTypes.string),
  label: PropTypes.string,
  setDuration: PropTypes.func,
  duration: PropTypes.string
}

export default StockTimeButtons
