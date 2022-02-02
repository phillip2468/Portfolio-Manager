import { IconButton, InputAdornment, TextField } from '@mui/material'
import { useState } from 'react'
import { Visibility, VisibilityOff } from '@material-ui/icons'
import * as PropTypes from 'prop-types'

const errorText = 'Passwords must contain a lowercase and uppercase letter, a digit and be greater than 8 characters.'
const defaultText = 'You can enter numbers and letters (no special characters)'

// https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
const validatePassword = (password) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
  return regex.test(password)
}

const PasswordField = ({ placeholder, password, setPassword, errorInInputs, setErrorInInputs, errorKey }) => {
  const [helperText, setHelperText] = useState(defaultText)
  const [showPassword, setShowPassword] = useState(false)

  const checkPassword = (event) => {
    const password = event.target.value
    if (!validatePassword(password)) {
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
                InputProps={{
                  endAdornment: (
                        <InputAdornment position="end">
                            <IconButton
                                aria-label="toggle password visibility"
                                onClick={() => setShowPassword(!showPassword)}
                                onMouseDown={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? <Visibility/> : <VisibilityOff/>}
                            </IconButton>
                        </InputAdornment>
                  )
                }}
                error={errorInInputs[errorKey]}
                fullWidth={true}
                helperText={helperText}
                onBlur={checkPassword}
                onChange={setPassword}
                placeholder={placeholder}
                sx={{ width: '350px' }}
                type={showPassword ? 'text' : 'password'}
                value={password}
                variant={'outlined'}
            />
        </>
  )
}

PasswordField.propTypes = {
  placeholder: PropTypes.string,
  password: PropTypes.string,
  setPassword: PropTypes.func,
  errorInInputs: PropTypes.arrayOf(PropTypes.object),
  setErrorInInputs: PropTypes.arrayOf(PropTypes.object),
  errorKey: PropTypes.string
}

export default PasswordField
