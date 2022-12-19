import React from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import OneFieldForm from "./OneFieldForm";
import TwoFieldForm from "./TwoFieldForm";

import './ReactorForm.css';

function ReactorForm(props) {
    return (
        <Box
            component="form"
            className="stack"
        >
            {props.fields.map((row, index) => (
                row.numVals === 1 ?
                (
                    <OneFieldForm
                        title={row.title}
                        onChange={row.onChange}
                        adorn={row.adorn}
                        label={row.title}
                        error={props.errors[row.shorthand]}
                        errorMessage={props.errorMessages[row.shorthand]}
                    />
                ) 
                :
                (
                    <TwoFieldForm
                        className="two-field-form"
                        title1={row.title1}
                        title2={row.title2}
                        onChange1={row.onChange1}
                        onChange2={row.onChange2}
                        adorn={row.adorn}
                        error1={props.errors[row.shorthand1]}
                        error2={props.errors[row.shorthand2]}
                        errorMessage1={props.errorMessages[row.shorthand1]}
                        errorMessage2={props.errorMessages[row.shorthand2]}
                    />
                    // <OneFieldForm
                    //     title={row.title}
                    //     onChange={row.onChange1}
                    //     adorn={row.adorn}
                    //     label={row.title}
                    //     error={props.errors[row.shorthand1]}
                    //     errorMessage={props.errorMessages[row.shorthand1]}
                    // />
                )
            ))}
            <Button onClick={props.handleCalculate}>
                Calculate
            </Button>
        </Box>
    );
}

export default ReactorForm;