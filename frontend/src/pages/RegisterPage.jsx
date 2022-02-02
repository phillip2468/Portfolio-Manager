import { Grid, Typography } from '@mui/material'
import EmailAddress from '../components/EmailAddress'
import { useEffect, useState } from 'react'
import PasswordField from '../components/Password'
import Button from '@mui/material/Button'
import { useNavigate } from 'react-router-dom'
import { FetchFunction } from '../components/FetchFunction'

const RegisterPage = () => {
  const navigate = useNavigate()

  const [inputs, setInputs] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  })

  const [errorInInputs, setErrorInInputs] = useState({
    email: false,
    password: false,
    confirmPassword: false
  })

  const [error, setError] = useState({
    emptyInputs: true,
    invalidInputs: true
  })

  const handleInputChanges = (prop) => (event) => {
    setInputs({ ...inputs, [prop]: event.target.value })
  }

  const registerAccount = () => {
    const body = {
      email: inputs.email,
      password: inputs.password
    }
    FetchFunction('POST', 'auth/register', body)
      .then(() => navigate('/'))
      .catch(error => console.log(error))
  }

  useEffect(() => {
    if (Object.values(errorInInputs).some(value => value === true)) {
      setError(prevState => ({
        ...prevState,
        invalidInputs: true
      }))
    } else {
      setError(prevState => ({
        ...prevState,
        invalidInputs: false
      }))
    }

    if (Object.values(inputs).some(value => value.length === 0)) {
      setError(prevState => ({
        ...prevState,
        emptyInputs: true
      }))
    } else {
      setError(prevState => ({
        ...prevState,
        emptyInputs: false
      }))
    }
  }, [errorInInputs, inputs])

  const enableRegisterButton = () => {
    return Object.values(error).some(value => value === true)
  }

  return (
        <>
            <Grid item>
                <Grid alignItems={'center'}
                      container
                      direction={'column'}
                      justifyContent={'center'}
                      spacing={2}
                >
                    <Grid item>
                        <Typography variant={'h4'}>Register</Typography>
                    </Grid>

                    <Grid item>
                        <EmailAddress
                            email={inputs.email}
                            errorInInputs={errorInInputs}
                            errorKey={'email'}
                            placeholder={'Type in an email address'}
                            setErrorInInputs={setErrorInInputs}
                            setValue={handleInputChanges('email')}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            errorInInputs={errorInInputs}
                            errorKey={'password'}
                            password={inputs.password}
                            placeholder={'Type in a password'}
                            setErrorInInputs={setErrorInInputs}
                            setPassword={handleInputChanges('password')}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            errorInInputs={errorInInputs}
                            errorKey={'confirmPassword'}
                            password={inputs.confirmPassword}
                            placeholder={'Confirm your password'}
                            setErrorInInputs={setErrorInInputs}
                            setPassword={handleInputChanges('confirmPassword')}
                        />
                    </Grid>

                    {inputs.password !== inputs.confirmPassword && (
                        <Grid item>
                            <Typography variant={'subtitle1'}>Passwords do not match</Typography>
                        </Grid>
                    )}

                    <Grid item>
                        <Button
                            disabled={enableRegisterButton()}
                            onClick={registerAccount}
                            variant={'contained'}
                        >
                            Register a new account
                        </Button>
                    </Grid>

                </Grid>
            </Grid>
        </>
  )
}

export default RegisterPage
