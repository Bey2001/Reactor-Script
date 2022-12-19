import React from "react";

import ReactorForm from "../ReactorForms/ReactorForm";

function ReactorStack(props) {

    return (
        <ReactorForm 
            fields={props.fields}
            errors={props.errors}
            errorMessages={props.errorMessages}
            handleCalculate={props.handleCalculate}
        />
    );
}

export default ReactorStack;