import {Divider, Grid, Link, TextField, Typography} from "@mui/material";
import Button from "@mui/material/Button";
import {useContext, useState} from "react";
import {ClientContext} from "../store/StoreCredentials";


const LoginPage = () => {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    let {loginUser} = useContext(ClientContext);

    const handleLogIn = () => {
        loginUser(email, password);
    }

    return (
        <>
            <Grid item>
                <Grid
                    container
                    spacing={2}
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

                    <Grid item>
                        <Link href={"#"}>Forgot your password?</Link>
                    </Grid>

                    <Divider light={true} flexItem style={{marginTop: "10px"}}/>

                    <Grid item>
                        <Button variant={"contained"} onClick={handleLogIn} style={{backgroundColor: "green"}}>
                            Create a new account
                        </Button>
                    </Grid>

                </Grid>
            </Grid>
        </>
    )
}

export default LoginPage;