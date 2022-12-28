import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import axios from 'axios'

import ReactorStack from '../Components/ReactorStack/ReactorStack';

class PFRSpacetime extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                volume: 0.350,
                lowerFlowrate: 0.00001,
                upperFlowrate: 10
            },
            errors: {
                volume: true,
                lowerFlowrate: true,
                upperFlowrate: true
            },
            errorMessages: {
                volume: '',
                lowerFlowrate: '',
                upperFlowrate: ''
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
            volume: {
                min: 0,
                max: 10
            },
            lowerFlowrate: 1,
            upperFlowrate: 10000
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
                numVals: 2,
                title1: 'Lower Vol. Flowrate',
                title2: 'Upper Vol. Flowrate',
                onChange1: this.changeLowerFlowrate.bind(this),
                onChange2: this.changeUpperFlowrate.bind(this),
                adorn: 'm^3/s',
                shorthand1: 'lowerFlowrate',
                shorthand2: 'upperFlowrate'
            }
        ]
    }

    validateValue(event, lowerBound, upperBound) {
        // Get the event.target's value as lowerFlowrate number
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

    changeLowerFlowrate(event) {
        var obj = this.validateValue(event, this.bounds.lowerFlowrate.min, this.state.values.upperFlowrate)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    lowerFlowrate: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    lowerFlowrate: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    lowerFlowrate: obj.value
                },
                errors: {
                    ...prevState.errors,
                    lowerFlowrate: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    lowerFlowrate: obj.errorMessage
                }
            }));
        }
    }

    changeUpperFlowrate(event) {
        var obj = this.validateValue(event, this.state.values.lowerFlowrate, this.bounds.upperFlowrate)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    upperFlowrate: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    upperFlowrate: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    upperFlowrate: obj.value
                },
                errors: {
                    ...prevState.errors,
                    upperFlowrate: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    upperFlowrate: obj.errorMessage
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
            let volume = this.state.values.volume
            let lowerFlowrate = this.state.values.lowerFlowrate
            let upperFlowrate = this.state.values.upperFlowrate

            axios
                .get('http://localhost:5000/pfr/spacetime',
                {
                    params: {
                        volume: volume,
                        lowerFlowrate: lowerFlowrate,
                        upperFlowrate: upperFlowrate
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
                <h1>PFR - Spacetime Manipulation</h1>
                <p>
                    This page is for simulating the reaction
                    A + B &#10230; C
                    in a PFR with varying spacetime.
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

export default PFRSpacetime;