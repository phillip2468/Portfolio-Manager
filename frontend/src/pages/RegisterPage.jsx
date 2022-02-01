import {Grid, Typography} from "@mui/material";
import EmailAddress from "../components/EmailAddress";
import {useState} from "react";
import PasswordField from "../components/Password";

const RegisterPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')

    const handleEmail = (event) => {
        const typedEmail = event.target.value;
        setEmail(typedEmail);
    }
    
    const handlePassword = (event) => {
        const typedPassword = event.target.value;
        setPassword(typedPassword);
    }

    const handleConfirmPassword = (event) => {
        const typedPassword = event.target.value;
        setConfirmPassword(typedPassword);
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
                            email={email}
                            setValue={handleEmail}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            placeholder={'Type in a password'}
                            password={password}
                            setPassword={handlePassword}
                        />
                    </Grid>

                    <Grid item>
                        <PasswordField
                            placeholder={'Type in a password'}
                            password={confirmPassword}
                            setPassword={handleConfirmPassword}
                        />
                    </Grid>
                </Grid>
            </Grid>
        </>
    )
}

export default RegisterPage;