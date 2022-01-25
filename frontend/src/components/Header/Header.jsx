import {AppBar, Box, IconButton, Toolbar} from "@mui/material";
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';
import {useNavigate} from "react-router-dom";
import {useContext} from "react";
import {ClientContext} from "../../store/StoreCredentials";

const Header = () => {

    const navigate = useNavigate();
    let {token, logoutUser} = useContext(ClientContext);

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
                        {token ?
                            <Button color="inherit" onClick={() => {logoutUser()}}>Logout</Button> :
                            <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
                        }
                    </div>
                </Toolbar>
            </AppBar>
        </Box>
    </>)
}

export default Header;