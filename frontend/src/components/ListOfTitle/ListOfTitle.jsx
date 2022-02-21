import React, { useContext, useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { TextField } from '@mui/material'
import { FetchFunction } from '../FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'

const ListOfTitle = props => {
  const { userId } = useContext(ClientContext)

  const [newTitle, setNewTitle] = useState('')

  console.log(props.currentValue)

  useEffect(() => {
    setNewTitle(props.currentValue)
  }, [props.currentValue])

  const changeTitle = () => {
    if (newTitle !== '') {
      const body = {
        portfolio_name: newTitle
      }
      FetchFunction('PATCH', `portfolio/${userId}/${props.currentValue}`, body)
        .then(res => console.log(res))
        .catch(error => console.log(error))
    }
  }

  return (
    <>
      <TextField
        onBlur={() => changeTitle()}
        onChange={(e) => setNewTitle(e.target.value)}
        value={newTitle}
        variant={'standard'}
      />
    </>
  )
}

ListOfTitle.propTypes = {
  currentValue: PropTypes.string,
  route: PropTypes.string
}

export default ListOfTitle
