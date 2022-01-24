import {Container, Grid, TextField, Typography} from "@mui/material";
import Button from "@mui/material/Button";
import {useContext, useState} from "react";
import {FetchFunction} from "../components/FetchFunction";
import {ClientContext} from "../store/StoreCredentials";
import {useNavigate} from "react-router-dom";

const LoginPage = () => {

    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    let {jwt, setJWT} = useContext(ClientContext)

    const handleLogIn = async () => {
        const body = {
            email: email,
            password: password,
        }


        try {
            const response = await FetchFunction('POST', 'auth/login', null, body)
            setJWT(response["access_token"])
        } catch (error) {
            console.log(error)
        }
    }

    const handleProtectedRoute = async () => {
        console.log(jwt)

        try {
            const response = await FetchFunction('GET', 'auth/protected', jwt, null)
            navigate('/')
            console.log(response)
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <>
            <Grid item>
                <Grid
                    container
                    spacing={1}
                    direction={"column"}
                    alignItems={"center"}
                    justifyContent={"center"}
                >
                    <Grid item>
                        <Typography variant={"h4"}>Sign in</Typography>
                    </Grid>

                    <Grid item>
                        <TextField
                            variant={"outlined"}
                            placeholder={"Email address"}
                            autoFocus={true}
                            fullWidth={true}
                            sx={{width: "350px"}}
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </Grid>

                    <Grid item>
                        <TextField
                            variant={"outlined"}
                            placeholder={"Password"}
                            fullWidth={true}
                            sx={{width: "350px"}}
                            type={"password"}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </Grid>

                    <Grid item>
                        <Button variant={"contained"} onClick={handleLogIn}>
                            Sign in
                        </Button>

                        <Button variant={"contained"} onClick={handleProtectedRoute}>
                            Protected
                        </Button>
                    </Grid>
                </Grid>
            </Grid>
        </>
    )
}

export default LoginPage;