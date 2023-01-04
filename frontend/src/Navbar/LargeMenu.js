import React from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Typography from "@mui/material/Typography";

function LargeMenu(props) {
  return (
    <Box>
      {/* Icon/Name */}
      <Button size="large" onClick={props.handleOpen} color="inherit">
        {props.title}
      </Button>
      {/* End of Icon/Name */}

      <Menu
        id="menu-appbar"
        anchorEl={props.anchorEl}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        keepMounted
        transformOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
        open={Boolean(props.anchorEl)}
        onClose={props.handleClose}
      >
        {props.pages.map((page) => (
          <MenuItem key={page.page} onClick={props.handleClose}>
            <Typography
              component="a"
              href={page.path}
              style={{
                textDecoration: "none",
                color: "inherit",
              }}
            >
              {page.page}
            </Typography>
          </MenuItem>
        ))}
      </Menu>
    </Box>
  );
}

export default LargeMenu;
