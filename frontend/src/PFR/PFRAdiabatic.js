import React, { Component } from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import ReactorStack from '../Components/ReactorStack/ReactorStack';

// Have each CSTR* be a stateful component with the specific fields necessary being stored.  This should allow editing using the old data as a basis


class PFRAdiabatic extends Component {

    constructor() {
        super()

        // Dynamic fields (subject to change, hence being in state)
        this.state = {
            values: {
                lowerTemp: 300,
                upperTemp: 500,
                cA: 30,
                hfA: -35000,
                cB: 30,
                hfB: -35000,
                cC: 30,
                hfC: -41000,
                // eAF: 10000,
                // k300: 0.00001,
            },
            errors: {
                lowerTemp: true,
                upperTemp: true,
                cA: true,
                hfA: true,
                cB: true,
                hfB: true,
                cC: true,
                hfC: true,
                // eAF: true,
                // k300: true
            },
            errorMessages: {
                lowerTemp: '',
                upperTemp: '',
                cA: '',
                hfA: '',
                cB: '',
                hfB: '',
                cC: '',
                hfC: '',
                // eAF: '',
                // k300: ''
            },
            error: false
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
            },
            // eAF: {
            //     min: 10000,
            //     max: 100000
            // },
            // k300: {
            //     min: 0.00001,
            //     max: 100
            // }
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
                title: "Specific Heat of A",
                onChange: this.changeCA.bind(this),
                adorn: "cal/mol.K",
                shorthand: 'cA'
            },
            {
                numVals: 1,
                title: 'Heat of Formation of A',
                onChange: this.changeHfA.bind(this),
                adorn: 'cal/mol',
                shorthand: 'hfA'
            },
            {
                numVals: 1,
                title: "Specific Heat of B",
                onChange: this.changeCB.bind(this),
                adorn: "cal/mol.K",
                shorthand: 'cB'
            },
            {
                numVals: 1,
                title: 'Heat of Formation of B',
                onChange: this.changeHfB.bind(this),
                adorn: 'cal/mol',
                shorthand: 'hfB'
            },
            {
                numVals: 1,
                title: "Specific Heat of C",
                onChange: this.changeCC.bind(this),
                adorn: "cal/mol.K",
                shorthand: 'cC'
            },
            {
                numVals: 1,
                title: 'Heat of Formation of C',
                onChange: this.changeHfC.bind(this),
                adorn: 'cal/mol',
                shorthand: 'hfC'
            },
            // {
            //     numVals: 1,
            //     title: 'Activation Energy',
            //     onChange: this.changeEAF.bind(this),
            //     adorn: 'cal/mol',
            //     shorthand: 'eAF'
            // },
            // {
            //     numVals: 1,
            //     title: 'Rate Constant (at 300K)',
            //     onChange: this.changeK300.bind(this),
            //     adorn: 'm^3/mol.s',
            //     shorthand: 'k300'
            // }
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

    changeCC(event) {
        var obj = this.validateValue(event, this.bounds.cC.min, this.bounds.cC.max)
        if (obj.error) {
            this.setState((prevState) => 
            ({
                ...prevState,
                errors: {
                    ...prevState.errors,
                    cC: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    cC: obj.errorMessage
                }
            }));
        }
        else {
            this.setState((prevState) => 
            ({
                ...prevState,
                values: {
                    ...prevState.values,
                    cC: obj.value
                },
                errors: {
                    ...prevState.errors,
                    cC: obj.error
                },
                errorMessages: {
                    ...prevState.errors,
                    cC: obj.errorMessage
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

    // changeEAF(event) {
    //     var obj = this.validateValue(event, this.bounds.eAF.min, this.bounds.eAF.max)
    //     if (obj.error) {
    //         this.setState((prevState) => 
    //         ({
    //             ...prevState,
    //             errors: {
    //                 ...prevState.errors,
    //                 eAF: obj.error
    //             },
    //             errorMessages: {
    //                 ...prevState.errors,
    //                 eAF: obj.errorMessage
    //             }
    //         }));
    //     }
    //     else {
    //         this.setState((prevState) => 
    //         ({
    //             ...prevState,
    //             values: {
    //                 ...prevState.values,
    //                 eAF: obj.value
    //             },
    //             errors: {
    //                 ...prevState.errors,
    //                 eAF: obj.error
    //             },
    //             errorMessages: {
    //                 ...prevState.errors,
    //                 eAF: obj.errorMessage
    //             }
    //         }));
    //     }
    // }

    // changeK300(event) {
    //     var obj = this.validateValue(event, this.bounds.k300.min, this.bounds.k300.max)
    //     if (obj.error) {
    //         this.setState((prevState) => 
    //         ({
    //             ...prevState,
    //             errors: {
    //                 ...prevState.errors,
    //                 k300: obj.error
    //             },
    //             errorMessages: {
    //                 ...prevState.errors,
    //                 k300: obj.errorMessage
    //             }
    //         }));
    //     }
    //     else {
    //         this.setState((prevState) => 
    //         ({
    //             ...prevState,
    //             values: {
    //                 ...prevState.values,
    //                 k300: obj.value
    //             },
    //             errors: {
    //                 ...prevState.errors,
    //                 k300: obj.error
    //             },
    //             errorMessages: {
    //                 ...prevState.errors,
    //                 k300: obj.errorMessage
    //             }
    //         }));
    //     }
    // }

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
                <h1>PFR - Adiabatic</h1>
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

export default PFRAdiabatic;