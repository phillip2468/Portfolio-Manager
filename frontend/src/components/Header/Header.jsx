import {AppBar, Box, IconButton, Toolbar} from "@mui/material";
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';
import {useNavigate} from "react-router-dom";
import {useContext, useEffect, useState} from "react";
import {ClientContext} from "../../store/StoreCredentials";
import {FetchFunction} from "../FetchFunction";

const Header = () => {

    const navigate = useNavigate();
    const [user, setUser] = useState(true)

    const handleLogout = () => {
        setUser(false)
    }

    const handleLogin = () => {
        setUser(true)
    }

    useEffect(()=> {

    }, [user])

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
                        { (user === false) ? (<Button color="inherit" onClick={handleLogin}>Login / Register</Button>) :
                            (<Button color="inherit" onClick={handleLogout}>Logout</Button>)
                        }
                    </div>
                </Toolbar>
            </AppBar>
        </Box>
    </>)
}

export default Header;