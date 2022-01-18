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

                        <div onClick={()=> console.log("ASDSA")}>
                            <IconButton>
                                Money maker
                            </IconButton>
                        </div>

                        <Button color="inherit">Login</Button>
                    </Toolbar>
                </AppBar>
            </Box>
        </>)
}

export default Header;