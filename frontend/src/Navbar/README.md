# Comments on the General Structure of the Navbar

The components with their source code in this folder account for the functional components used as part of the Navbar. This includes the Navbar and the LargeMenu components.

## The Navbar

The Navbar itself is a simple four-button interface with the first three being on the top-left of the screen and the fourth being on the top-right of the screen. The first is the home button that displays "ChE-Suite", the second is the button to open the menu for CSTR analysis, the third is the button to open the menu for PFR analysis, and the fourth is the button to navigate to the Info page.

When either the second or third button is clicked, a menu pops up leveraging the pages listed in the Navbar components for CSTR and PFR respectively. These use LargeMenu functional components to render link options for the user to select.

## The LargeMenu Functional Component

In addition to the Navbar, the LargeMenu functional component is defined here, which is a pretty straightforward menu that is generated from a button click. Actual detailed implementation details can be seen from the source code file `LargeMenu.js`.

## Further Investigation

If you want, more information about this Navbar construction can be seen at https://javascript.works-hub.com/learn/how-to-create-a-responsive-navbar-using-material-ui-and-react-router-f9a01.
