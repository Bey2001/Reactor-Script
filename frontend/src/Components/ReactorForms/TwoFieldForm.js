import React from "react";

import Box from "@mui/material/Box";

import OneFieldForm from "./OneFieldForm";
import './TwoFieldForm.css';

function TwoFieldForm(props) {


    return (
        <Box
            component="form"
            className="two-field-form"
        >
            <OneFieldForm
                title={props.title1}
                onChange={props.onChange1}
                adorn={props.adorn}
                label={props.title1}
                error={props.error1}
                errorMessage={props.errorMessage1}
            />
            <OneFieldForm
                title={props.title2}
                onChange={props.onChange2}
                adorn={props.adorn}
                label={props.title2}
                error={props.error2}
                errorMessage={props.errorMessage2}
            />
        </Box>
    );
}

export default TwoFieldForm;