import React, { Component } from "react";

import CloseIcon from "@mui/icons-material/Close";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Snackbar from "@mui/material/Snackbar";
import axios from "axios";

import ReactorStack from "../../ReactorStack/ReactorStack";
import { backend } from "../../../Globals/config"


import "./CSTR.css";

// Have each CSTR* be a stateful component with the specific fields necessary being stored.  This should allow editing using the old data as a basis

class CSTRTemp extends Component {
  constructor() {
    super();

    // Dynamic fields (subject to change, hence being in state)
    this.state = {
      values: {
        lowerTemp: 300,
        upperTemp: 1000,
        eA: 10000,
        k: 0.01,
        tRef: 300,
      },
      errors: {
        lowerTemp: true,
        upperTemp: true,
        eA: true,
        k: true,
        tRef: true,
      },
      errorMessages: {
        lowerTemp: "",
        upperTemp: "",
        eA: "",
        k: "",
        tRef: "",
      },
      error: false,
      image: "",
      posted: false,
      loading: false,
    };
    /***************************************
     * Static fields, to be changed by dev *
     ***************************************/

    this.bounds = {
      lowerTemp: 300,
      upperTemp: 1000,
      eA: {
        min: 1,
        max: 100000,
      },
      k: {
        min: 0.00001,
        max: 1,
      },
      tRef: {
        min: 300,
        max: 1000,
      },
    };

    // Constant fields for customizing the form fields on the web app
    this.fields = [
      {
        numVals: 2,
        title1: "Lower Temp. Bound",
        title2: "Upper Temp. Bound",
        onChange1: this.changeLowerTemp.bind(this),
        onChange2: this.changeUpperTemp.bind(this),
        adorn: "K",
        shorthand1: "lowerTemp",
        shorthand2: "upperTemp",
      },
      {
        numVals: 1,
        title: "Activation Energy",
        onChange: this.changeEA.bind(this),
        adorn: "cal/mol",
        shorthand: "eA",
      },
      {
        numVals: 1,
        title: "Measured Rate Constant",
        onChange: this.changeK.bind(this),
        adorn: "m^3/mol.s",
        shorthand: "k",
      },
      {
        numVals: 1,
        title: "Reference Temperature for Rate Constant",
        onChange: this.changeTRef.bind(this),
        adorn: "K",
        shorthand: "tRef",
      },
    ];
  }

  validateValue(event, lowerBound, upperBound) {
    // Get the event.target's value as a number
    let value = +event.target.value;
    // Default error setting
    let newError = false;
    // Default error message setting
    let newErrorMessage = "";
    // Check if the value translated properly
    if (isNaN(value)) {
      newError = true;
      newErrorMessage = "Value passed in is not numeric";
    }
    // If the value is not within the appropriate bounds
    else if (value < lowerBound || value > upperBound) {
      newError = true;
      newErrorMessage =
        "Limit value to between " + lowerBound + " and " + upperBound;
    }
    // Return the evaluation of criteria
    return {
      value: value,
      error: newError,
      errorMessage: newErrorMessage,
    };
  }

  changeLowerTemp(event) {
    var obj = this.validateValue(
      event,
      this.bounds.lowerTemp,
      this.state.values.upperTemp
    );
    if (obj.error) {
      this.setState((prevState) => ({
        ...prevState,
        errors: {
          ...prevState.errors,
          lowerTemp: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          lowerTemp: obj.errorMessage,
        },
      }));
    } else {
      this.setState((prevState) => ({
        ...prevState,
        values: {
          ...prevState.values,
          lowerTemp: obj.value,
        },
        errors: {
          ...prevState.errors,
          lowerTemp: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          lowerTemp: obj.errorMessage,
        },
      }));
    }
  }

  changeUpperTemp(event) {
    var obj = this.validateValue(
      event,
      this.state.values.lowerTemp,
      this.bounds.upperTemp
    );
    if (obj.error) {
      this.setState((prevState) => ({
        ...prevState,
        errors: {
          ...prevState.errors,
          upperTemp: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          upperTemp: obj.errorMessage,
        },
      }));
    } else {
      this.setState((prevState) => ({
        ...prevState,
        values: {
          ...prevState.values,
          upperTemp: obj.value,
        },
        errors: {
          ...prevState.errors,
          upperTemp: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          upperTemp: obj.errorMessage,
        },
      }));
    }
  }

  changeEA(event) {
    var obj = this.validateValue(event, this.bounds.eA.min, this.bounds.eA.max);
    if (obj.error) {
      this.setState((prevState) => ({
        ...prevState,
        errors: {
          ...prevState.errors,
          eA: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          eA: obj.errorMessage,
        },
      }));
    } else {
      this.setState((prevState) => ({
        ...prevState,
        values: {
          ...prevState.values,
          eA: obj.value,
        },
        errors: {
          ...prevState.errors,
          eA: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          eA: obj.errorMessage,
        },
      }));
    }
  }

  changeK(event) {
    var obj = this.validateValue(event, this.bounds.k.min, this.bounds.k.max);
    if (obj.error) {
      this.setState((prevState) => ({
        ...prevState,
        errors: {
          ...prevState.errors,
          k: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          k: obj.errorMessage,
        },
      }));
    } else {
      this.setState((prevState) => ({
        ...prevState,
        values: {
          ...prevState.values,
          k: obj.value,
        },
        errors: {
          ...prevState.errors,
          k: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          k: obj.errorMessage,
        },
      }));
    }
  }

  changeTRef(event) {
    var obj = this.validateValue(
      event,
      this.bounds.tRef.min,
      this.bounds.tRef.max
    );
    if (obj.error) {
      this.setState((prevState) => ({
        ...prevState,
        errors: {
          ...prevState.errors,
          tRef: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          tRef: obj.errorMessage,
        },
      }));
    } else {
      this.setState((prevState) => ({
        ...prevState,
        values: {
          ...prevState.values,
          tRef: obj.value,
        },
        errors: {
          ...prevState.errors,
          tRef: obj.error,
        },
        errorMessages: {
          ...prevState.errors,
          tRef: obj.errorMessage,
        },
      }));
    }
  }

  handleCalculate() {
    let openSnackbar = false;
    for (const bool in this.state.errors) {
      openSnackbar = openSnackbar || this.state.errors[bool];
    }

    // If no error exists, send the fields to the backend
    //      Need to also retrieve the URL and store it,
    //          then use it to render the appropriate graph
    if (!openSnackbar) {
      let lowerTemp = "" + this.state.values.lowerTemp;
      let upperTemp = "" + this.state.values.upperTemp;
      let eA = "" + this.state.values.eA;
      let k = "" + this.state.values.k;
      let tRef = "" + this.state.values.tRef;

      axios
        .get(backend + "/cstr/temp", {
          params: {
            lowerTemp: lowerTemp,
            upperTemp: upperTemp,
            eA: eA,
            k: k,
            tRef: tRef,
          },
          responseType: "blob",
        })
        .then((response) => {
          this.setState(
            (prevState) => ({
              ...prevState,
              error: false,
              image: response.data,
              loading: true,
              posted: true,
            }),
            () => {
              this.setState({ loading: false });
            }
          );
        })
        .catch((error) => {
          console.log(error);
        });
    } else {
      this.setState((prevState) => ({
        ...prevState,
        error: openSnackbar,
      }));
    }
  }

  handleCloseSnackbar = () => this.setState({ error: false });

  handleCloseImage = () =>
    this.setState({
      image: "",
      loading: false,
      posted: false,
    });

  render() {
    return (
      <header className="CSTR-header">
        <h1>CSTR - Temperature Manipulation</h1>
        <p className="CSTR-flavor">
          This page is for simulating the reaction A + B &#10230; C in an
          isothermal CSTR at various temperatures.
        </p>
        {!this.state.posted ? (
          <React.Fragment>
            <ReactorStack
              fields={this.fields}
              errors={this.state.errors}
              errorMessages={this.state.errorMessages}
              handleCalculate={this.handleCalculate.bind(this)}
              sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100vh",
              }}
              values={this.state.values}
            />
            {/* Snackbar to warn the user of existing errors */}
            <Snackbar
              open={this.state.error}
              message="Input errors exist"
              onClose={this.handleCloseSnackbar}
              action={
                <IconButton
                  size="small"
                  aria-label="close"
                  color="inherit"
                  onClick={this.handleCloseSnackbar}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              }
            />
          </React.Fragment>
        ) : (
          <React.Fragment>
            <Button
              onClick={this.handleCloseImage}
              color="inherit"
              id="go-back"
            >
              Go Back (Saves Settings)
            </Button>
            {this.state.loading ? (
              <h1>Loading...</h1>
            ) : (
              <img src={URL.createObjectURL(this.state.image)} alt="plot.png" />
            )}
          </React.Fragment>
        )}
      </header>
    );
  }
}

export default CSTRTemp;
