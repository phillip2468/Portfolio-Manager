import { Grid, Typography } from '@mui/material'
import * as PropTypes from 'prop-types'
import React from 'react'

const StockIntervals = (props) => {
  return <Grid item>
        <Grid container spacing={1}>
            <Grid item>
              <Typography sx={{ textAlign: 'center' }}>List of periods</Typography>
            </Grid>
            {props.listOfIntervals.map(props.callbackfn)}
        </Grid>
    </Grid>
}

StockIntervals.propTypes = {
  listOfIntervals: PropTypes.arrayOf(PropTypes.string),
  callbackfn: PropTypes.func
}

export default StockIntervals
