import {AppBar, Box, IconButton, Toolbar} from "@mui/material";
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';
import {useNavigate} from "react-router-dom";

const Header = () => {

    const navigate = useNavigate();

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

                    <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
                </Toolbar>
            </AppBar>
        </Box>
    </>)
}

export default Header;