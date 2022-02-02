import { TextField } from '@mui/material'
import { useState } from 'react'
import * as PropTypes from 'prop-types'

const errorText = 'Email addresses should be longer than 10 characters, contain an @ symbol and should contain a domain.'
const defaultText = 'You can enter numbers, letters and periods'

// https://stackoverflow.com/questions/52188192/what-is-the-simplest-and-shortest-way-for-validating-an-email-in-react
const validateEmail = (email) => {
  const regexp = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return regexp.test(email)
}

const EmailAddress = ({ placeholder, email, setValue, errorInInputs, setErrorInInputs, errorKey }) => {
  const [helperText, setHelperText] = useState(defaultText)

  const checkEmailAddress = (event) => {
    const emailAddress = event.target.value
    if (!validateEmail(emailAddress)) {
      setErrorInInputs({ ...errorInInputs, [errorKey]: true })
      setHelperText(errorText)
    } else {
      setErrorInInputs({ ...errorInInputs, [errorKey]: false })
      setHelperText(defaultText)
    }
  }

  return (
        <>
            <TextField
                error={errorInInputs[errorKey]}
                fullWidth={true}
                helperText={helperText}
                onBlur={checkEmailAddress}
                onChange={setValue}
                placeholder={placeholder}
                sx={{ width: '350px' }}
                value={email}
                variant={'outlined'}
            />
        </>
  )
}

EmailAddress.propTypes = {
  placeholder: PropTypes.string,
  email: PropTypes.string,
  setValue: PropTypes.func,
  errorInInputs: PropTypes.arrayOf(PropTypes.object),
  setErrorInInputs: PropTypes.arrayOf(PropTypes.object),
  errorKey: PropTypes.string
}

export default EmailAddress
