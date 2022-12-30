import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import axios from 'axios'

import ReactorStack from '../Components/ReactorStack/ReactorStack';

class PFRVarCo extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                coefficient: 2,
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
                min: 0.25,
                max: 2
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

        if (!openSnackbar) {
            let coefficient = this.state.values.coefficient

            axios
                .get('http://localhost:5000/pfr/varco',
                {
                    params: {
                        coefficient: coefficient
                    },
                    responseType: 'blob'
                })
                .then(response => {
                    this.setState((prevState) => ({
                        ...prevState,
                        error: false,
                        image: response.data,
                        loading: true,
                        posted: true
                    }),
                        () => {
                            this.setState({loading: false})
                        }
                    )
                })
                .catch(error => {
                    console.log(error)
                })
        }
        else {
            this.setState((prevState) => ({
                ...prevState,
                error: openSnackbar
            }))
        }
    }

    handleCloseSnackbar = () => this.setState({error: false})

    handleCloseImage = () => this.setState({
        image: '',
        loading: false,
        posted: false
    })

    render() {
        return (
            <div>
                <h1>PFR - Variable Coefficients of B</h1>
                <p>
                    This page is for simulating the reaction
                    A + B &#10230; C
                    in a PFR with varying coefficients of B.
                </p>
                {!this.state.posted ? 
                    (<React.Fragment>
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
                            values={this.state.values}
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
                    </React.Fragment>)
                    :
                    (
                    <React.Fragment>
                        <IconButton
                                size="small"
                                aria-label="close"
                                color="inherit"
                                onClick={this.handleCloseImage}
                            >
                                <CloseIcon fontSize="small" />
                        </IconButton>
                        {
                            this.state.loading ? 
                            (
                                <h1>Loading...</h1>
                            )
                            :
                            (<img 
                                src={URL.createObjectURL(this.state.image)}
                                alt="plot.png"
                            />)
                        }
                    </React.Fragment> 
                    )
                }
            </div>
        );
    }
}

export default PFRVarCo;