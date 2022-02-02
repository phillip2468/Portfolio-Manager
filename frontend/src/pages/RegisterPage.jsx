import {Grid, Typography} from "@mui/material";
import EmailAddress from "../components/EmailAddress";
import {useEffect, useState} from "react";
import PasswordField from "../components/Password";
import Button from "@mui/material/Button";
import {useNavigate} from "react-router-dom";
import {FetchFunction} from "../components/FetchFunction";

const RegisterPage = () => {

    const navigate = useNavigate();

    const [inputs, setInputs] = useState({
        email: '',
        password: '',
        confirmPassword: '',
    })

    const [errorInInputs, setErrorInInputs] = useState({
        email: false,
        password: false,
        confirmPassword: false,
    })

    const [error, setError] = useState({
        validInputs: true,
        matchingPasswords: true,
    });

    const handleInputChanges = (prop) => (event) => {
        setInputs({...inputs, [prop]: event.target.value });
    }

    const registerAccount = () => {
        const body = {
            email: inputs.email,
            password: inputs.password,
        }
        FetchFunction('POST', 'auth/register', body)
            .then(()=> navigate('/'))
            .catch(error => console.log(error))
    }

    useEffect(()=> {
        if (Object.values(errorInInputs).every((value) => value === false)) {
            setError({...error, validInputs: false})
        }
        if (inputs.password !== inputs.confirmPassword) {
            setError({...error, matchingPasswords: false})
        } else {
            setError({...error, validInputs: true, matchingPasswords: true})
        }
    }, [errorInInputs])


    return (
        <>
            <Grid item>
                <Grid container
                      spacing={2}
                      direction={"column"}
                      alignItems={"center"}
                      justifyContent={"center"}
                >
                    <Grid item>
                        <Typography variant={"h4"}>Register</Typography>
                    </Grid>

                    <Grid item>
                        <EmailAddress
                            placeholder={'Type in an email address'}
                            email={inputs.email}
                            setValue={handleInputChanges('email')}
                            errorInInputs={errorInInputs}
                            setErrorInInputs={setErrorInInputs}
                            errorKey={'email'}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            placeholder={'Type in a password'}
                            password={inputs.password}
                            setPassword={handleInputChanges('password')}
                            errorInInputs={errorInInputs}
                            setErrorInInputs={setErrorInInputs}
                            errorKey={'password'}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            placeholder={'Confirm your password'}
                            password={inputs.confirmPassword}
                            setPassword={handleInputChanges('confirmPassword')}
                            errorInInputs={errorInInputs}
                            setErrorInInputs={setErrorInInputs}
                            errorKey={'confirmPassword'}
                        />
                    </Grid>

                    {(error.matchingPasswords === false) && (
                        <Grid item>
                            <Typography variant={'subtitle1'}>Passwords do not match</Typography>
                        </Grid>
                    )}


                    <Grid item>
                        <Button
                            variant={"contained"}
                            onClick={registerAccount}
                            disabled={(!Object.values(errorInInputs).every((value) => value === false))}
                        >
                            Register a new account
                        </Button>
                    </Grid>

                </Grid>
            </Grid>
        </>
    )
}

export default RegisterPage;