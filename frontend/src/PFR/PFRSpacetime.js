import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import ReactorStack from '../Components/ReactorStack/ReactorStack';

// Have each CSTR* be a stateful component with the specific fields necessary being stored.  This should allow editing using the old data as a basis


class PFRSpacetime extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                volume: 30,
                flowrate: -35000,
            },
            errors: {
                volume: true,
                flowrate: true,
            },
            errorMessages: {
                volume: '',
                flowrate: '',
            },
            error: false
        }
        /***************************************
         * Static fields, to be changed by dev *
         ***************************************/

        this.bounds = {
            volume: {
                min: 10,
                max: 100
            },
            flowrate: {
                min: -50000,
                max: 50000
            },
        }
       
        // Constant fields for customizing the form fields on the web app
        this.fields = [
            {
                numVals: 1,
                title: "Reactor Volume",
                onChange: this.changeVolume.bind(this),
                adorn: "m^3",
                shorthand: 'volume'
            },
            {
                numVals: 1,
                title: 'Volumetric Flowrate',
                onChange: this.changeFlowrate.bind(this),
                adorn: 'm^2',
                shorthand: 'flowrate'
            }
        ]
    }

    validateValue(event, lowerBound, upperBound) {
        // Get the event.target's value as flowrate number
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

    changeVolume(event) {
        var obj = this.validateValue(event, this.bounds.volume.min, this.bounds.volume.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    volume: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    volume: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    volume: obj.value
                },
                errors: {
                    ...prevState.errors,
                    volume: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    volume: obj.errorMessage
                }
            }));
        }
    }

    changeFlowrate(event) {
        var obj = this.validateValue(event, this.bounds.flowrate.min, this.bounds.flowrate.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    flowrate: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    flowrate: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    flowrate: obj.value
                },
                errors: {
                    ...prevState.errors,
                    flowrate: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    flowrate: obj.errorMessage
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
                <h1>PFR - Spacetime</h1>
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

export default PFRSpacetime;