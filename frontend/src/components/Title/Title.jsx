import React from 'react'
import { Typography } from '@mui/material'
import PropTypes from 'prop-types'

const Title = props => {
  return (
    <div>
      <Typography align={'center'} data-testid={'Title'} variant={'h4'}>
        {props.title}
      </Typography>
    </div>
  )
}

Title.propTypes = {
  title: PropTypes.string
}

export default Title
