import React from 'react';
import { AppBar, CssBaseline, Drawer, Hidden, IconButton,Typography, Toolbar, Divider,
    List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import { Menu,  Home, CalendarToday, People } from '@material-ui/icons';
import { NavLink, Link } from "react-router-dom";
import '../App.css';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: drawerWidth,
      flexShrink: 0,
    },
  },
  appBar: {
    [theme.breakpoints.up('sm')]: {
      width: `calc(100% - ${drawerWidth}px)`,
      marginLeft: drawerWidth,
    },
  },
  menuButton: {
    marginRight: theme.spacing(2),
    [theme.breakpoints.up('sm')]: {
      display: 'none',
    },
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  nested: {
    paddingLeft: theme.spacing(10),
  },
}));

function Layout(props) {
    const { window, children } = props;
    const classes = useStyles();
    const theme = useTheme();
    const [mobileOpen, setMobileOpen] = React.useState(false);
  
    const handleDrawerToggle = () => {
      setMobileOpen(!mobileOpen);
    };
  
    const drawer = (
      <div>
        <div className={classes.toolbar} />
        <Divider />
        <List>
            <ListItem button key="Home" component={NavLink} to="/">
              <ListItemIcon><Home /></ListItemIcon>
              <ListItemText primary="Home" />
            </ListItem>
        </List>
        <Divider />
        <List>
          {['Fantasy Standings', 'MLB Standings'].map((text, index) => (
            <ListItem button key={text} 
                component={NavLink} 
                to={index === 0 ? "/fantasystandings" : "/mlbstandings"}>
              <ListItemIcon><CalendarToday /></ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        <ListItem button key="Fantasy Teams"
            component={NavLink}
            to="/fantasyteams">
                <ListItemIcon><People /></ListItemIcon>
                <ListItemText primary="Fantasy Teams" />
            </ListItem>
        </List>
        <List>
        {["Team Collins", "Team Donofrio", "Team Ludwig", "Team Luvin", "Team McGowan", "Team Schmidt", "Team Shannon"].map ((text, index) => (
              // <a className="stubbornLink" href={`/fantasyteams#${text}`}>
              <Link 
                className="stubbornLink"
                to={{ 
                pathname: "/fantasyteams",
                hash: "#" + text              
              }}>
                <ListItem button key={text} 
                    className={classes.nested}
                    >
                      {/*^this link just doesn't work...if i change it to a normal anchor, then it does, but otherwise no. */}
                    <ListItemText primary={text} />
                </ListItem>
                </Link>
              // </a>
        ))}
        </List>
      </div>
    );
  
    const container = window !== undefined ? () => window().document.body : undefined;

    
    return (
     <div className={classes.root}>
      <CssBaseline />
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            className={classes.menuButton}
          >
            <Menu />
          </IconButton>
          <Typography variant="h6" noWrap>
            COVID-19 MLB Fantasy League
          </Typography>
        </Toolbar>
      </AppBar>
      <nav className={classes.drawer} aria-label="mailbox folders">
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Hidden smUp implementation="css">
          <Drawer
            container={container}
            variant="temporary"
            anchor={theme.direction === 'rtl' ? 'right' : 'left'}
            open={mobileOpen}
            onClose={handleDrawerToggle}
            classes={{
              paper: classes.drawerPaper,
            }}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
          >
            {drawer}
          </Drawer>
        </Hidden>
        <Hidden xsDown implementation="css">
          <Drawer
            classes={{
              paper: classes.drawerPaper,
            }}
            variant="permanent"
            open
          >
            {drawer}
          </Drawer>
        </Hidden>
      </nav>
      <main className={classes.content}>
      <div className={classes.toolbar} />
      {/* the children are what is passed bw the Layout tags in the App.js file*/}
        {children}
      </main>
    </div>
    );
}

export default Layout;
