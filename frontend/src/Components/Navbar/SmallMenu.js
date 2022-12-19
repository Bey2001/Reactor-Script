import React from 'react';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';

function SmallMenu(props) {

    return (
        <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>

            {/* Icon/Name */}
            <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={props.handleOpen}
                color="inherit"
            >
                {props.title}
            </IconButton>
            {/* End of Icon/Name */}

            <Menu
                id="menu-appbar"
                anchorEl={props.anchorEl}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                open={Boolean(props.anchorEl)}
                onClose={props.handleClose}
                sx={{
                    display: { xs: 'block', md: 'none' },
                }}
            >
                {props.pages.map((page) => (
                    <MenuItem 
                        key={page.page} 
                        onClick={props.handleClose}
                    >
                        <Typography 
                            component="a"
                            href={page.path}
                            style={{ 
                                textDecoration: 'none',
                                color: 'inherit'
                            }}
                        >
                            {page.page}
                        </Typography>
                    </MenuItem>
                ))}
            </Menu>
        </Box> 
    )
}

export default SmallMenu