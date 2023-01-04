import React, { useState } from "react";

import { Box } from "@mui/material";
import AppBar from "@mui/material/AppBar";
import Container from "@mui/material/Container";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

import LargeMenu from "./LargeMenu";

// List of CSTR page names
const cstrPages = [
  {
    page: "Adiabatic",
    path: "/cstr/adiabatic",
  },
  {
    page: "Heat Exchanger",
    path: "/cstr/exchanger",
  },
  {
    page: "Spacetime",
    path: "/cstr/spacetime",
  },
  {
    page: "Temperature",
    path: "/cstr/temperature",
  },
  {
    page: "Var. Coefficient",
    path: "/cstr/varco",
  },
];

// List of PFR page names
const pfrPages = [
  {
    page: "Adiabatic",
    path: "/pfr/adiabatic",
  },
  {
    page: "Spacetime",
    path: "/pfr/spacetime",
  },
  {
    page: "Temperature",
    path: "/pfr/temperature",
  },
  {
    page: "Var. Coefficient",
    path: "/pfr/varco",
  },
];

function Navbar() {
  const [anchorBigCSTR, setAnchorBigCSTR] = useState(null);
  const [anchorBigPFR, setAnchorBigPFR] = useState(null);

  const handleOpenBigCSTR = (event) => {
    setAnchorBigCSTR(event.currentTarget);
  };
  const handleOpenBigPFR = (event) => {
    setAnchorBigPFR(event.currentTarget);
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
        <Toolbar>
          {/* Home Name */}
          <Typography
            variant="h4"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              fontFamily: "arial",
              fontWeight: 600,
              color: "inherit",
              textDecoration: "none",
            }}
          >
            ChE-Suite
          </Typography>

          <Box
            sx={{
              width: 3,
              height: 50,
              backgroundColor: "white",
            }}
          />

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

          <Typography
            variant="h4"
            noWrap
            component="a"
            href="/info"
            sx={{
              mr: 2,
              fontFamily: "arial",
              fontWeight: 600,
              color: "inherit",
              textDecoration: "none",
              marginLeft: "auto",
            }}
          >
            Info
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default Navbar;
