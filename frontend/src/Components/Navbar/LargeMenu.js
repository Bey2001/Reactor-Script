import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';

function LargeMenu(props) {

    return (
        <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            
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
                    horizontal: 'left',
                }}
                keepMounted
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                }}
                open={Boolean(props.anchorEl)}
                onClose={props.handleClose}
                sx={{
                    display: { xs: 'none', md: 'block' },
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

export default LargeMenu