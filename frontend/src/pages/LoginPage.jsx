import { Divider, Grid, Link, TextField, Typography } from '@mui/material'
import Button from '@mui/material/Button'
import { useContext, useState } from 'react'
import { ClientContext } from '../store/StoreCredentials'
import { useNavigate } from 'react-router-dom'

const LoginPage = () => {
  const navigate = useNavigate()

  const [email, setEmail] = useState('testemail1234@email.com')
  const [password, setPassword] = useState('Password12345')

  const { loginUser } = useContext(ClientContext)

  const handleLogIn = () => {
    loginUser(email, password)
  }

  return (
        <>
            <Grid item>
                <Grid
                    alignItems={'center'}
                    container
                    direction={'column'}
                    justifyContent={'center'}
                    spacing={2}
                >
                    <Grid item>
                        <Typography variant={'h4'}>Sign in</Typography>
                    </Grid>

                    <Grid item>
                        <TextField
                            autoFocus={true}
                            fullWidth={true}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder={'Email address'}
                            sx={{ width: '350px' }}
                            value={email}
                            variant={'outlined'}
                        />
                    </Grid>

                    <Grid item>
                        <TextField
                            fullWidth={true}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder={'Password'}
                            sx={{ width: '350px' }}
                            type={'password'}
                            value={password}
                            variant={'outlined'}
                        />
                    </Grid>

                    <Grid item>
                        <Button onClick={handleLogIn} variant={'contained'}>
                            Sign in
                        </Button>
                    </Grid>

                    <Grid item>
                        <Link href={'#'}>Forgot your password?</Link>
                    </Grid>

                    <Divider flexItem light={true} style={{ marginTop: '10px' }}/>

                    <Grid item>
                        <Button onClick={() => navigate('/register')} style={{ backgroundColor: 'green' }}
                                variant={'contained'}>
                            Create a new account
                        </Button>
                    </Grid>

                </Grid>
            </Grid>
        </>
  )
}

export default LoginPage
