import {AppBar, Box, IconButton, Toolbar} from "@mui/material";
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';
import {useNavigate} from "react-router-dom";
import {useContext, useEffect, useState} from "react";
import {ClientContext} from "../../store/StoreCredentials";
import {FetchFunction} from "../FetchFunction";

const Header = () => {

    const navigate = useNavigate();

    const [user, setUser] = useState([])

    const whichUser = () => {
        FetchFunction('GET', 'auth/which_user', null, null)
            .then(res => {
                alert(res)
                setUser(res)
            })
            .catch(error => alert(error))
    }

    let {logoutUser} = useContext(ClientContext);

    const handleLogout = () => {
        setUser([])
        logoutUser();
    }

    console.log(user)
    useEffect(()=> {
        whichUser();
    }, [])

    if (!user) {
        navigate('/login')
    }


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
                        {user !== [] ?
                            <Button color="inherit" onClick={handleLogout}>Logout</Button> :
                            <Button color="inherit" onClick={() => navigate('/login')}>Login / Register</Button>
                        }
                    </div>
                </Toolbar>
            </AppBar>
        </Box>
    </>)
}

export default Header;