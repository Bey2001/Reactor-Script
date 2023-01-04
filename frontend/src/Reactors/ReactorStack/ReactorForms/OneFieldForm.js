import React from "react";

import FormControl from "@mui/material/FormControl";
import FormHelperText from "@mui/material/FormHelperText";
import InputAdornment from "@mui/material/InputAdornment";
import InputLabel from "@mui/material/InputLabel";
import OutlinedInput from "@mui/material/OutlinedInput";

import "./OneFieldForm.css";

function OneFieldForm(props) {
  return (
    <FormControl required fullwidth sx={{ m: 1 }}>
      <InputLabel sx={{ color: "inherit" }}>{props.title}</InputLabel>
      <OutlinedInput
        endAdornment={<InputAdornment>{props.adorn}</InputAdornment>}
        label={props.label}
        error={props.error}
        onChange={props.onChange}
        placeholder={props.value}
        sx={{ color: "inherit" }}
      />
      <FormHelperText sx={{ color: "inherit" }}>
        {props.errorMessage}
      </FormHelperText>
    </FormControl>
  );
}

export default OneFieldForm;
