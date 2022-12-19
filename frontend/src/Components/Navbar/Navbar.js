import React, { useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import IconButton from '@mui/material/IconButton';

import LargeMenu from './LargeMenu';
import SmallMenu from './SmallMenu';
import logo from '../../logo.svg';


// List of CSTR page names
const cstrPages = [
  {
    "page": "Adiabatic",
    "path": "/cstr/adiabatic"
  },
  {
    "page": "Heat Exchanger",
    "path": "/cstr/exchanger"
  },
  {
    "page": "Spacetime",
    "path": "/cstr/spacetime"
  },
  {
    "page": "Temperature",
    "path": "/cstr/temperature"
  },
  {
    "page": "Var. Coefficient",
    "path": "/cstr/varco"
  }
];

// List of PFR page names
const pfrPages = [
  {
    "page": "Adiabatic",
    "path": "/pfr/adiabatic"
  },
  {
    "page": "Spacetime",
    "path": "/pfr/spacetime"
  },
  {
    "page": "Temperature",
    "path": "/pfr/temperature"
  },
  {
    "page": "Var. Coefficient",
    "path": "/pfr/varco"
  }
];

function Navbar() {
  const [anchorElCSTR, setAnchorElCSTR] = useState(null);
  const [anchorElPFR, setAnchorElPFR] = useState(null);
  const [anchorBigCSTR, setAnchorBigCSTR] = useState(null);
  const [anchorBigPFR, setAnchorBigPFR] = useState(null);


  const handleOpenCSTRMenu = (event) => {
    setAnchorElCSTR(event.currentTarget);
  };
  const handleOpenPFRMenu = (event) => {
    setAnchorElPFR(event.currentTarget);
  };
  const handleOpenBigCSTR = (event) => {
    setAnchorBigCSTR(event.currentTarget);
  };
  const handleOpenBigPFR = (event) => {
    setAnchorBigPFR(event.currentTarget);
  };

  const handleCloseCSTRMenu = () => {
    setAnchorElCSTR(null);
  };
  const handleClosePFRMenu = () => {
    setAnchorElPFR(null);
  };
  const handleCloseBigCSTR = () => {
    setAnchorBigCSTR(null);
  };
  const handleCloseBigPFR = () => {
    setAnchorBigPFR(null);
  };

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>

          {/* Full screen logo */}
          <IconButton 
            href="/"
            sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }}
          >
            <img 
              src={logo} 
              className="App-logo" 
              alt="logo" 
            />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            ChE-Suite
          </Typography>

          {/* Large screen menu */}
          {/* <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {cstrPages.map((item) => (
              <Button
                key={item.page}
                onClick={handleCloseCSTRMenu}
                href={item.path}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {item.page}
              </Button>
            ))}
          </Box>  */}
          <LargeMenu
            title="CSTR"
            handleOpen={handleOpenBigCSTR}
            handleClose={handleCloseBigCSTR}
            anchorEl={anchorBigCSTR}
            pages={cstrPages}
          />
          <LargeMenu
            title="PFR"
            handleOpen={handleOpenBigPFR}
            handleClose={handleCloseBigPFR}
            anchorEl={anchorBigPFR}
            pages={pfrPages}
          />
          {/* End of full screen typography */}
          
          {/* Small screen menu */}
          <SmallMenu
            title="CSTR"
            handleOpen={handleOpenCSTRMenu}
            handleClose={handleCloseCSTRMenu}
            anchorEl={anchorElCSTR}
            pages={cstrPages}
          />
          {/* End of small screen menu */}

          {/* Small screen typography */}
          <IconButton sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }}>
            <img 
              src={logo} 
              className="App-logo" 
              alt="logo" 
            />
          </IconButton>
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            ChE-Suite
          </Typography>
          {/* End of Small screen typography */}

          <SmallMenu
            title="PFR"
            handleOpen={handleOpenPFRMenu}
            handleClose={handleClosePFRMenu}
            anchorEl={anchorElPFR}
            pages={pfrPages}
          />

          <Box sx={{ flexGrow: 0 }}>
            <IconButton                 
              href={"/help"}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right'
              }}
              sx={{ 
                color: 'inherit', 
              }}
            >
              HELP
            </IconButton>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default Navbar;