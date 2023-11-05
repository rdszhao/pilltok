'use client'
import {ThemeProvider} from '@mui/material/styles'
import {createTheme} from '@mui/material/styles'

const themeOptions = (isDarkMode) =>
  createTheme({
    palette: {
      mode: isDarkMode ? 'dark' : 'light', // 'type' is replaced with 'mode' in MUI v5
      primary: {
        // This will be the blue color used throughout your application
        main: isDarkMode ? '#003c71' : '#1f78b4', // Dark blue for dark mode, lighter blue for light mode
      },
      secondary: {
        // This will be the green color used for secondary actions and highlights
        main: isDarkMode ? '#357a38' : '#4caf50', // Darker green for dark mode, brighter green for light mode
      },
      background: {
        // The background colors for your application
        default: isDarkMode ? '#121212' : '#ffffff', // Dark background for dark mode, white for light mode
        paper: isDarkMode ? '#1e272e' : '#bbdefb', // Slightly lighter dark background for surfaces in dark mode, light blue for light mode
      },
      text: {
        // Text colors for your application
        primary: isDarkMode ? '#ffffff' : '#000000', // White text for dark mode, black for light mode
        secondary: isDarkMode ? '#a0a0a0' : '#303030', // Light grey for secondary text in dark mode, dark grey for light mode
      },
    },
    typography: {
      // Define the font to be used across the application
      fontFamily: "'Roboto', sans-serif",
    },
  })

export default function CustomTheme({children}) {
  // Set 'isDarkMode' to 'false' for light theme by default
  return <ThemeProvider theme={themeOptions(false)}>{children}</ThemeProvider>
}
