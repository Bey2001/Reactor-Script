import React from "react";

import FormControl from "@mui/material/FormControl";
import InputAdornment from "@mui/material/InputAdornment";
import InputLabel from "@mui/material/InputLabel";
import OutlinedInput from "@mui/material/OutlinedInput";
import FormHelperText from "@mui/material/FormHelperText";

function OneFieldForm(props) {

    return (
        <FormControl required fullwidth sx={{ m: 1 }}>
            <InputLabel >{props.title}</InputLabel>
            <OutlinedInput
                endAdornment={
                    <InputAdornment>
                        {props.adorn}
                    </InputAdornment>
                }
                label={props.label}
                error={props.error}
                onChange={props.onChange}
            />
            <FormHelperText>{props.errorMessage}</FormHelperText>
        </FormControl>
    );
}

export default OneFieldForm;