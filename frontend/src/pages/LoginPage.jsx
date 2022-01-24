import {Grid, TextField, Typography} from "@mui/material";
import Button from "@mui/material/Button";
import {useState} from "react";
import {FetchFunction} from "../components/FetchFunction";
import {useNavigate} from "react-router-dom";
import jwt_decode from "jwt-decode";


const LoginPage = () => {

    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogIn = async () => {
        const body = {
            email: email,
            password: password,
        }
        try {
            const response = await FetchFunction('POST', 'auth/login', null, body)
            const jwt_token = jwt_decode(response['access_token']).toString()
            localStorage.setItem('token_jwt', jwt_token)
            navigate('/')
        } catch (error) {
            alert(error)
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
                    </Grid>
                </Grid>
            </Grid>
        </>
    )
}

export default LoginPage;