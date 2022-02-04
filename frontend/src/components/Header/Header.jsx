import { AppBar, Box, Drawer, IconButton, List, ListItem, ListItemText, Toolbar } from '@mui/material'
import Button from '@mui/material/Button'
import MenuIcon from '@mui/icons-material/Menu'
import { useNavigate } from 'react-router-dom'
import { useContext, useState } from 'react'
import { ClientContext } from '../../store/StoreCredentials'

const anchor = 'left'

const Header = () => {
  const navigate = useNavigate()

  const { logoutUser, loggedIn } = useContext(ClientContext)

  const goToLoginPage = () => {
    navigate('/login')
  }

  const [drawerOpen, setDrawerOpen] = useState(false)

  const toggleDrawer = (anchor, open) => (event) => {
    // This is so you can scroll through the list of items with the keyboard
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return
    }

    setDrawerOpen(open)
  }

  const protectedPage = (pageName) => {
    if (loggedIn) {
      navigate(`/${pageName}`)
    } else {
      navigate('/login')
    }
  }

  const listOfItems = (anchor) => (
    <Box
      onClick={toggleDrawer(anchor, false)}
      onKeyDown={toggleDrawer(anchor, false)}
      role="presentation"
      sx={{ width: 250 }}>
      <List>
        <ListItem button key={'Home'}>
          <ListItemText onClick={() => navigate('/')} primary={'Home'}/>
        </ListItem>

        <ListItem button key={'Market trends'}>
          <ListItemText onClick={() => navigate('/trends')} primary={'Trends'}/>
        </ListItem>

        <ListItem button key={'Portfolio'}>
          <ListItemText onClick={() => protectedPage('portfolio')} primary={'Portfolio'}/>
        </ListItem>

        <ListItem button key={'Watchlist'}>
          <ListItemText onClick={() => protectedPage('watchlist')} primary={'Watchlist'}/>
        </ListItem>
      </List>
    </Box>
  )

  return (<>
        <Box>
            <AppBar position="static">
                <Toolbar sx={{ justifyContent: 'space-between' }}>
                    <IconButton
                        aria-label="menu"
                        color="inherit"
                        edge="start"
                        onClick={toggleDrawer(anchor, true)}
                        size="large"
                        sx={{ mr: 2 }}
                    >
                        <MenuIcon/>
                    </IconButton>

                  <Drawer anchor={anchor} onClose={toggleDrawer(anchor, false)} open={drawerOpen}>
                    {listOfItems(anchor)}
                  </Drawer>

                    <div onClick={() => navigate('/')}>
                        <IconButton>
                            Money maker
                        </IconButton>
                    </div>

                    <div>
                        {
                            (loggedIn === false)
                              ? (<Button color="inherit" onClick={goToLoginPage}>Login / Register</Button>)
                              : (<Button color="inherit" onClick={logoutUser}>Logout</Button>)
                        }
                    </div>
                </Toolbar>
            </AppBar>
        </Box>
    </>)
}

export default Header
