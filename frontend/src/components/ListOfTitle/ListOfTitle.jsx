import React, { useContext, useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { TextField } from '@mui/material'
import { FetchFunction } from '../FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'

const ListOfTitle = props => {
  const { userId } = useContext(ClientContext)

  const [newTitle, setNewTitle] = useState('')

  useEffect(() => {
    setNewTitle(props.currentValue)
  }, [props.currentValue])

  const changeTitle = () => {
    if (newTitle !== '') {
      const body = {
        portfolio_name: newTitle
      }
      FetchFunction('PATCH', `${props.route}/${userId}/${props.currentValue}`, body)
        .then(res => {
          console.log(res)
          props.setChangedValue(prevState => !prevState)
        })
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
  setChangedValue: PropTypes.func,
  route: PropTypes.string,
  changedValue: PropTypes.bool
}

export default ListOfTitle
