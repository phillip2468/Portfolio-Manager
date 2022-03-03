import React from 'react'
import PropTypes from 'prop-types'
import { Grid, MenuItem, Select } from '@mui/material'

const CurrentList = (props) => {
  return (
    <Grid container direction={'row'} justifyContent={'center'} spacing={2}>
      <Select
        data-testid={'selectCurrentList'}
        displayEmpty={true}
        onChange={(e) => props.setCurrentValue(e.target.value)}
        renderValue={(selected) => {
          if (selected.length === 0) {
            return <em>Select an item here...</em>
          }
          return selected
        }}
        sx={{ width: '210px' }}
        value={props.currentValue}
        variant={'standard'}
      >
        <MenuItem disabled value={''}>
          <em>Select...</em>
        </MenuItem>

        {
          props.listOfValues.map(function (element) {
            return (
            <MenuItem
            key={element[props.iterateValue]}
            value={element[props.iterateValue]}
            >
              {element[props.iterateValue]}
          </MenuItem>
            )
          })
        }

      </Select>
    </Grid>
  )
}

CurrentList.propTypes = {
  currentValue: PropTypes.string,
  setCurrentValue: PropTypes.func,
  listOfValues: PropTypes.arrayOf(PropTypes.shape({
    iterateValue: PropTypes.string
  })),
  iterateValue: PropTypes.string
}

export default CurrentList
