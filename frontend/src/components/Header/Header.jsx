import {AppBar, Box, IconButton, Toolbar} from "@mui/material";
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';
import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {FetchFunction} from "../FetchFunction";

const Header = () => {

    const navigate = useNavigate();
    const [loggedIn, setLoggedIn] = useState(false)

    const handleLogout = () => {
        FetchFunction('POST', 'auth/logout', null, null)
            .then(res => {
                console.log(res)
                setLoggedIn(false)
                navigate('/login')
            })
            .catch(res => console.log(res))
    }

    const handleLogin = () => {
        navigate('/login')
    }

    const findUser = () => {
        FetchFunction('GET', 'auth/which_user', null, null)
            .then(() => {
                setLoggedIn(true)
            })
            .catch(()=> {
                setLoggedIn(false)
            })
    }

    useEffect(()=> {
        findUser()
    }, [loggedIn])

    return (<>
        <Box>
            <AppBar position="static">
                <Toolbar sx={{justifyContent: "space-between"}}>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{mr: 2}}
                    >
                        <MenuIcon/>
                    </IconButton>

                    <div onClick={() => navigate('/')}>
                        <IconButton>
                            Money maker
                        </IconButton>
                    </div>

                    <div>
                        { (loggedIn === false) ? (<Button color="inherit" onClick={handleLogin}>Login / Register</Button>) :
                            (<Button color="inherit" onClick={handleLogout}>Logout</Button>)
                        }
                    </div>
                </Toolbar>
            </AppBar>
        </Box>
    </>)
}

export default Header;