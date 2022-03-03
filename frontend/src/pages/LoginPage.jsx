import { Divider, Grid, Link } from '@mui/material'
import Button from '@mui/material/Button'
import { useContext, useState } from 'react'
import { ClientContext } from '../store/StoreCredentials'
import { useNavigate } from 'react-router-dom'
import Password from '../components/Password/Password'
import EmailAddress from '../components/EmailAddress/EmailAddress'
import Title from '../components/Title/Title'

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
                      <Title
                        title={'Sign in'}
                      />
                    </Grid>

                    <Grid item>
                      <EmailAddress
                        email={email}
                        placeholder={'Enter an email address here'}
                        setEmail={setEmail}
                      />
                    </Grid>

                    <Grid item>
                        <Password
                        password={password}
                        placeholder={'Enter a password here'}
                        setPassword={setPassword}
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
