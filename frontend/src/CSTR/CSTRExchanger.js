import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import axios from 'axios'

import ReactorStack from '../Components/ReactorStack/ReactorStack';

import './CSTR.css';

// Have each CSTR* be a stateful component with the specific fields necessary being stored.  This should allow editing using the old data as a basis


class CSTRExchanger extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                lowerTemp: 300,
                upperTemp: 1000,
                u: 630,
                a: 0.00033,
                tSurface: 330,
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
            u: {
                min: 100,
                max: 1000
            },
            a: {
                min: 0,
                max: 1
            },
            tSurface: {
                min: this.state.values.lowerTemp,
                max: this.state.values.upperTemp
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
        }

        if (!openSnackbar) {
            let lowerTemp = '' + this.state.values.lowerTemp
            let upperTemp = '' + this.state.values.upperTemp
            let u = '' + this.state.values.u
            let a = '' + this.state.values.a
            let tSurface = '' + this.state.values.tSurface

            axios
                .get('http://localhost:5000/cstr/exchanger',
                {
                    params: {
                        lowerTemp: lowerTemp,
                        upperTemp: upperTemp,
                        u: u,
                        a: a,
                        tSurface: tSurface
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
            <header className="CSTR-header">
                <h1>CSTR - Heat Exchanger</h1>
                <p className='CSTR-flavor'>
                    This page is for simulating the reaction
                    A + B &#10230; C
                    in a CSTR with a heat exchanger.
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
                        <Button 
                            onClick={this.handleCloseImage} 
                            color='inherit' 
                            id="go-back"
                        >
                            Go Back (Saves Settings)
                        </Button>
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
            </header>
        );
    }
}

export default CSTRExchanger;