import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import ReactorStack from '../Components/ReactorStack/ReactorStack';

// Have each CSTR* be a stateful component with the specific fields necessary being stored.  This should allow editing using the old data as a basis


class CSTRExchanger extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                lowerTemp: 300,
                upperTemp: 500,
                u: 30,
                a: -35000,
                tSurface: 30,
            },
            errors: {
                lowerTemp: true,
                upperTemp: true,
                u: true,
                a: true,
                tSurface: true,
            },
            errorMessages: {
                lowerTemp: '',
                upperTemp: '',
                u: '',
                a: '',
                tSurface: '',
            },
            error: false
        }
        /***************************************
         * Static fields, to be changed by dev *
         ***************************************/

        this.bounds = {
            lowerTemp: 300,
            upperTemp: 1000,
            u: {
                min: 10,
                max: 100
            },
            a: {
                min: -50000,
                max: 50000
            },
            tSurface: {
                min: 10,
                max: 100
            }
        }
       
        // Constant fields for customizing the form fields on the web app
        this.fields = [
            {
                numVals: 2,
                title1: 'Lower Temp. Bound',
                title2: 'Upper Temp. Bound',
                onChange1: this.changeLowerTemp.bind(this),
                onChange2: this.changeUpperTemp.bind(this),
                adorn: "K",
                shorthand1: 'lowerTemp',
                shorthand2: 'upperTemp'
            },
            {
                numVals: 1,
                title: "Heat Transfer Coefficient",
                onChange: this.changeU.bind(this),
                adorn: "W/m^2.K",
                shorthand: 'u'
            },
            {
                numVals: 1,
                title: 'Area of Heat Transfer',
                onChange: this.changeA.bind(this),
                adorn: 'm^2',
                shorthand: 'a'
            },
            {
                numVals: 1,
                title: "Surface Temperature",
                onChange: this.changeTS.bind(this),
                adorn: "K",
                shorthand: 'tSurface'
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

    changeLowerTemp(event) {
        var obj = this.validateValue(event, this.bounds.lowerTemp, this.state.values.upperTemp)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    lowerTemp: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    lowerTemp: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    lowerTemp: obj.value
                },
                errors: {
                    ...prevState.errors,
                    lowerTemp: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    lowerTemp: obj.errorMessage
                }
            }));
        }
    }

    changeUpperTemp(event) {
        var obj = this.validateValue(event, this.state.values.lowerTemp, this.bounds.upperTemp)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    upperTemp: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    upperTemp: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    upperTemp: obj.value
                },
                errors: {
                    ...prevState.errors,
                    upperTemp: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    upperTemp: obj.errorMessage
                }
            }));
        }
    }

    changeU(event) {
        var obj = this.validateValue(event, this.bounds.u.min, this.bounds.u.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    u: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    u: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    u: obj.value
                },
                errors: {
                    ...prevState.errors,
                    u: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    u: obj.errorMessage
                }
            }));
        }
    }

    changeA(event) {
        var obj = this.validateValue(event, this.bounds.a.min, this.bounds.a.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    a: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    a: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    a: obj.value
                },
                errors: {
                    ...prevState.errors,
                    a: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    a: obj.errorMessage
                }
            }));
        }
    }

    changeTS(event) {
        var obj = this.validateValue(event, this.bounds.tSurface.min, this.bounds.tSurface.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    tSurface: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    tSurface: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    tSurface: obj.value
                },
                errors: {
                    ...prevState.errors,
                    tSurface: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    tSurface: obj.errorMessage
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
                <h1>CSTR - Heat Exchanger</h1>
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

export default CSTRExchanger;