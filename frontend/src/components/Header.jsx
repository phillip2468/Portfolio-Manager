import {AppBar, Box, IconButton, Toolbar, Typography} from "@mui/material";
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';

const Header = () => {
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
                        <Typography variant="h5" component="div" sx={{flexGrow: 1}}>
                            Money maker
                        </Typography>
                        <Button color="inherit">Login</Button>
                    </Toolbar>
                </AppBar>
            </Box>
        </>)
}

export default Header;