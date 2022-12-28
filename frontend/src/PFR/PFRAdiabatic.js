import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import axios from "axios";

import ReactorStack from '../Components/ReactorStack/ReactorStack';

class PFRAdiabatic extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                lowerTemp: 300,
                upperTemp: 1000,
                cA: 0,
                hfA: 0,
                cB: 0,
                hfB: 0,
                hfC: 0,
            },
            errors: {
                lowerTemp: true,
                upperTemp: true,
                cA: true,
                hfA: true,
                cB: true,
                hfB: true,
                hfC: true,
            },
            errorMessages: {
                lowerTemp: '',
                upperTemp: '',
                cA: '',
                hfA: '',
                cB: '',
                hfB: '',
                hfC: '',
            },
            error: false,
            image: '',
            posted: false,
            loading: false
        }
        /***************************************
         * Static fields, to be changed by dev *
         ***************************************/

        this.bounds = {
            lowerTemp: 300,
            upperTemp: 1000,
            cA: {
                min: 10,
                max: 100
            },
            hfA: {
                min: -50000,
                max: 50000
            },
            cB: {
                min: 10,
                max: 100
            },
            hfB: {
                min: -50000,
                max: 50000
            },
            cC: {
                min: 10,
                max: 100
            },
            hfC: {
                min: -50000,
                max: 50000
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
                shorthand2: 'upperTemp',
            },
            {
                numVals: 1,
                title: "Specific Heat of A",
                onChange: this.changeCA.bind(this),
                adorn: "cal/mol.K",
                shorthand: 'cA',
            },
            {
                numVals: 1,
                title: 'Heat of Formation of A',
                onChange: this.changeHfA.bind(this),
                adorn: 'cal/mol',
                shorthand: 'hfA',
            },
            {
                numVals: 1,
                title: "Specific Heat of B",
                onChange: this.changeCB.bind(this),
                adorn: "cal/mol.K",
                shorthand: 'cB',
            },
            {
                numVals: 1,
                title: 'Heat of Formation of B',
                onChange: this.changeHfB.bind(this),
                adorn: 'cal/mol',
                shorthand: 'hfB',
            },
            {
                numVals: 1,
                title: 'Heat of Formation of C',
                onChange: this.changeHfC.bind(this),
                adorn: 'cal/mol',
                shorthand: 'hfC',
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

    changeCA(event) {
        var obj = this.validateValue(event, this.bounds.cA.min, this.bounds.cA.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    cA: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    cA: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    cA: obj.value
                },
                errors: {
                    ...prevState.errors,
                    cA: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    cA: obj.errorMessage
                }
            }));
        }
    }

    changeHfA(event) {
        var obj = this.validateValue(event, this.bounds.hfA.min, this.bounds.hfA.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    hfA: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    hfA: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    hfA: obj.value
                },
                errors: {
                    ...prevState.errors,
                    hfA: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    hfA: obj.errorMessage
                }
            }));
        }
    }

    changeCB(event) {
        var obj = this.validateValue(event, this.bounds.cB.min, this.bounds.cB.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    cB: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    cB: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    cB: obj.value
                },
                errors: {
                    ...prevState.errors,
                    cB: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    cB: obj.errorMessage
                }
            }));
        }
    }

    changeHfB(event) {
        var obj = this.validateValue(event, this.bounds.hfB.min, this.bounds.hfB.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    hfB: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    hfB: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    hfB: obj.value
                },
                errors: {
                    ...prevState.errors,
                    hfB: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    hfB: obj.errorMessage
                }
            }));
        }
    }

    changeHfC(event) {
        var obj = this.validateValue(event, this.bounds.hfC.min, this.bounds.hfC.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    hfC: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    hfC: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    hfC: obj.value
                },
                errors: {
                    ...prevState.errors,
                    hfC: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    hfC: obj.errorMessage
                }
            }));
        }
    }

    handleCalculate() {
        let openSnackbar = false
        for (const bool in this.state.errors) {
            openSnackbar = openSnackbar || this.state.errors[bool]
        }

        if (this.state.values.hfC - this.state.values.hfA - this.state.values.hfB >= 0) {
            openSnackbar = true
        }

        if (!openSnackbar) {
            let lowerTemp = '' + this.state.values.lowerTemp
            let upperTemp = '' + this.state.values.upperTemp
            let cA = '' + this.state.values.cA
            let hfA = '' + this.state.values.hfA
            let cB = '' + this.state.values.cB
            let hfB=  '' + this.state.values.hfB
            let hfC = '' + this.state.values.hfC

            axios
                .get('http://localhost:5000/pfr/adiabatic',
                {
                    params: {
                        lowerTemp: lowerTemp,
                        upperTemp: upperTemp,
                        cA: cA,
                        hfA: hfA,
                        cB: cB,
                        hfB: hfB,
                        hfC: hfC
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
                <h1>PFR - Adiabatic Operation</h1>
                <p>
                    This page is for simulating the reaction
                    A + B &#10230; C
                    in an Adiabatic PFR.
                </p>

                {!this.state.posted ? 
                    (<React.Fragment>
                        <ReactorStack 
                            fields={this.fields}
                            values={this.state.values}
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
                    </React.Fragment>)
                    :
                    (<React.Fragment>
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
                    </React.Fragment>)
                }
            </div>
        );
    }
}

export default PFRAdiabatic;