# Comments on the General Structure of the Reactor Pages

Each Reactor page has a type of the reactor being analyzed, along with the type of analysis available on that page. For example, CSTRAdiabatic deals with Adiabatic Operation analysis of a CSTR. Every page, save for CSTRVarCo works with the generic reaction A + B --> C for simplicity.

## React Structure

Every page is written in JavaScript as a class component, and leverages several functional components to actually present the data. The use of both of these is to split the data to be stored where it needs to be stored through the concept of stateful components. This basically means that the class component, that of the reactor page, is the component that stores the data, which dynamically changes, in it, versus it being stored at the form level. This follows good React conventions, especially with abstracting data collected/utilized in the children components (i.e. the form elements/fillable fields) into the larger parent (the reactor page) as far as necessary for distinction between pages/sibling components.

This does not mean that the class components are without function, most notably the functions used as "onChange" functions for the fillable fields. For the most part, these function verify that the information passed into one of the fields is numeric first, then that the data passed in is within the bounds programmed into the overall reactor page component. This frontend verification greatly reduces the time for a graph to be generated, as well as allowing the user to understand exactly what and where the issue is when entering data into the form.

## Connecting to the Backend Server

ChE-Suite leverages a React frontend with a Flask backend. This is a particularly rudimentary structure, honestly no more complex than a calculator app that happens to do specialized integrations for its calculations. There is plenty of documentation to see Flask connecting to React, but there are some confusing aspects to how the connection is made.

ChE-Suite uses axios to connect the frontend React app to the backend Flask app. The connection is simple to make using Flask's API and Resources, and allows the frontend to access different URLs that contain parameters, while spitting out usable graph images that can be rendered by the frontend React app. This is great, as it minimizes the data that needs to be stored for both the frontend and backend. All React needs is to take the data sent back, store it in an accessible form via URL, then use that URL to source an image in an img object to display to the user.

If you're only working on the frontend React app, you need not concern yourself with how the Flask app works; this is discussed in the backend's API README.md file.

## Further Investigation

I recommend looking into several functions that are at the core of React programming, namely setState, as well as the general concept of a State to further understand the Reactor Pages. Once you have mastered class/stateful components, you should easily be able to navigate through any of the pages, since a majority of them are reliant only on the idea of a state of a parent component.
