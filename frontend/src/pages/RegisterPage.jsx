import {Grid, Typography} from "@mui/material";
import EmailAddress from "../components/EmailAddress";
import {useState} from "react";
import PasswordField from "../components/Password";
import Button from "@mui/material/Button";
import {useNavigate} from "react-router-dom";

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

    const [error, setError] = useState(false)

    const handleInputChanges = (prop) => (event) => {
        setInputs({...inputs, [prop]: event.target.value });
    }

    const registerAccount = () => {
        if (inputs.password !== inputs.confirmPassword) {
            setError(true);
        }
    }

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
                            error={errorInInputs.email}
                            setError={setErrorInInputs}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            placeholder={'Type in a password'}
                            password={inputs.password}
                            setPassword={handleInputChanges('password')}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            placeholder={'Confirm your password'}
                            password={inputs.confirmPassword}
                            setPassword={handleInputChanges('confirmPassword')}
                        />
                    </Grid>

                    {error && (
                        <Grid item>
                            <Typography variant={'subtitle1'}>Passwords do not match</Typography>
                        </Grid>
                    )}


                    <Grid item>
                        <Button
                            variant={"contained"}
                            onClick={registerAccount}
                            disabled={error}
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