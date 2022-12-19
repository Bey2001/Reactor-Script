import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import ReactorStack from '../Components/ReactorStack/ReactorStack';

// Have each CSTR* be a stateful component with the specific fields necessary being stored.  This should allow editing using the old data as a basis


class PFRVarCo extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                coefficient: 4,
            },
            errors: {
                coefficient: true
            },
            errorMessages: {
                coefficient: '',
            },
            error: false
        }
        /***************************************
         * Static fields, to be changed by dev *
         ***************************************/

        this.bounds = {
            coefficient: {
                min: 0.5,
                max: 4
            }
        }
       
        // Constant fields for customizing the form fields on the web app
        this.fields = [
            {
                numVals: 1,
                title: "Coefficient of Reactant B",
                onChange: this.changeCoefficient.bind(this),
                adorn: "",
                shorthand: 'coefficient'
            }
        ]
    }

    validateValue(event, lowerBound, upperBound) {
        // Get the event.target's value as a number
        let value = + event.target.value
        // Default error setting
        let newError = false
        // Default error message setting
        let newErrorMessage = ''
        // Check if the value translated properly
        if (isNaN(value)) {
            newError = true
            newErrorMessage = 'Value passed in is not numeric'
        }
        // If the value is not within the appropriate bounds
        else if (value < lowerBound
                || value > upperBound) {
            newError = true
            newErrorMessage = 'Limit value to between ' + lowerBound + ' and ' + upperBound
        }
        // Return the evaluation of criteria
        return {
            value: value,
            error: newError,
            errorMessage: newErrorMessage
        }
    }

    changeCoefficient(event) {
        var obj = this.validateValue(event, this.bounds.coefficient.min, this.bounds.coefficient.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    coefficient: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    coefficient: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    coefficient: obj.value
                },
                errors: {
                    ...prevState.errors,
                    coefficient: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    coefficient: obj.errorMessage
                }
            }));
        }
    }

    handleCalculate() {
        let openSnackbar = false
        for (const bool in this.state.errors) {
            openSnackbar = openSnackbar || this.state.errors[bool]
            console.log(this.state.errors[bool])
        }

        this.setState((prevState) => ({
            ...prevState,
            error: openSnackbar
        }))

        // If no error exists, send the fields to the backend
        //      Need to also retrieve the URL and store it,
        //          then use it to render the appropriate graph
        if (!openSnackbar) {

        }
    }

    handleCloseSnackbar = () => this.setState({error: false})

    render() {
        return (
            <div>
                <h1>PFR - Coefficient Exploration</h1>
                <ReactorStack 
                    fields={this.fields}
                    errors={this.state.errors}
                    errorMessages={this.state.errorMessages}
                    handleCalculate={this.handleCalculate.bind(this)}
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100vh'
                    }}
                />
                {/* Snackbar to warn the user of existing errors */}
                <Snackbar
                    open={this.state.error}
                    message="Input errors exist"
                    onClose={this.handleCloseSnackbar}
                    action={(
                    <IconButton
                        size="small"
                        aria-label="close"
                        color="inherit"
                        onClick={this.handleCloseSnackbar}
                      >
                        <CloseIcon fontSize="small" />
                      </IconButton>
                    )}
                />
            </div>
        );
    }
}

export default PFRVarCo;