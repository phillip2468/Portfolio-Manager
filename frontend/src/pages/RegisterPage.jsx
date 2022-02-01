import {Grid, Typography} from "@mui/material";
import EmailAddress from "../components/EmailAddress";
import {useState} from "react";

const RegisterPage = () => {
    const [email, setEmail] = useState('');

    const handleSearch = (event) => {
        const typedEmail = event.target.value;
        setEmail(typedEmail);
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
                        <Typography variant={"h4"}>Register account</Typography>
                    </Grid>

                    <Grid item>
                        <EmailAddress
                            placeholder={'Type in an email address'}
                            email={email}
                            setValue={handleSearch}
                        />
                    </Grid>
                </Grid>
            </Grid>
        </>
    )
}

export default RegisterPage;