import React, { useContext } from 'react'
import PropTypes from 'prop-types'
import Button from '@mui/material/Button'
import { FetchFunction } from '../FetchFunction'
import { ClientContext } from '../../store/StoreCredentials'

const DeleteList = props => {
  const { userId } = useContext(ClientContext)

  const deleteList = () => {
    FetchFunction('DELETE', `${props.route}/${userId}/${props.selectedItem}`)
      .then(() => props.setSelectedItem(''))
      .catch(error => console.log(error))
  }

  return (
    <>
      <Button
        onClick={() => deleteList()}
        sx={{ background: 'red' }}
        variant={'outlined'}
      >
        {props.text}
      </Button>
    </>
  )
}

DeleteList.propTypes = {
  text: PropTypes.string,
  route: PropTypes.string,
  selectedItem: PropTypes.string,
  setSelectedItem: PropTypes.func
}

export default DeleteList
