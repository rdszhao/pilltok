'use client'

import {
  Box,
  Button,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material'
import {useState} from 'react'

// Helper function to create an array of options for hours (0-23)
const generateHourOptions = () => {
  const hoursArray = []
  for (let i = 0; i < 24; i++) {
    hoursArray.push({
      label: `${i}:00`, // display label
      value: i * 60, // value in minutes after midnight
    })
  }
  return hoursArray
}

const hoursOptions = generateHourOptions()

export default function Routine() {
  const [routines, setRoutines] = useState({
    wakeup_time: 0,
    bedtime: 0,
    meals: {
      breakfast: 0,
      lunch: 0,
      dinner: 0,
    },
  })

  const handleSelectChange = (event) => {
    const {name, value} = event.target
    if (name.startsWith('meal')) {
      const mealType = name.split('_')[1]
      setRoutines((prevRoutines) => ({
        ...prevRoutines,
        meals: {
          ...prevRoutines.meals,
          [mealType]: value,
        },
      }))
    } else {
      setRoutines((prevRoutines) => ({
        ...prevRoutines,
        [name]: value,
      }))
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    // Handle the form submission logic here
    console.log(routines)
  }

  return (
    <Box
      width="100vw"
      height="100vh"
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      p={4}
    >
      <Typography variant="h4" gutterBottom>
        Daily Routine
      </Typography>
      <Box
        component="form"
        noValidate
        autoComplete="off"
        onSubmit={handleSubmit}
        sx={{display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 500}}
      >
        <Grid container spacing={2}>
          {/* Wake-up time and Bedtime */}
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Wake-up Time</InputLabel>
              <Select
                name="wakeup_time"
                value={routines.wakeup_time}
                label="Wake-up Time"
                onChange={handleSelectChange}
              >
                {hoursOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Bedtime</InputLabel>
              <Select
                name="bedtime"
                value={routines.bedtime}
                label="Bedtime"
                onChange={handleSelectChange}
              >
                {hoursOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          {/* Meal times */}
          {Object.entries(routines.meals).map(([mealType, value], index) => (
            <Grid
              item
              xs={12}
              sm={index === Object.entries(routines.meals).length - 1 ? 12 : 6}
              key={mealType}
            >
              <FormControl fullWidth>
                <InputLabel>
                  {mealType.charAt(0).toUpperCase() + mealType.slice(1)}
                </InputLabel>
                <Select
                  name={`meal_${mealType}`}
                  value={value}
                  label={mealType.charAt(0).toUpperCase() + mealType.slice(1)}
                  onChange={handleSelectChange}
                >
                  {hoursOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          ))}
        </Grid>

        <Button type="submit" variant="contained" color="primary" sx={{mt: 2}}>
          Save Routine
        </Button>
      </Box>
    </Box>
  )
}
