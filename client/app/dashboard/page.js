'use client'
import React, {useEffect, useState} from 'react'
import {
  Box,
  Typography,
  FormControl,
  Select,
  Button,
  MenuItem,
  Snackbar,
  Alert,
  Modal,
} from '@mui/material'
import {Warning} from '@mui/icons-material'
import {useAuth} from '@clerk/nextjs'

const data = {
  schedule: {
    ATENOLOL: [450, 930, 1410],
    AMOXICILLIN: [450, 770, 1090, 1410],
  },
  warning_keys: [
    {
      ATENOLOL: 'AMOXICILLIN',
    },
    {
      ATENOLOL: 'AMOXICILLIN',
    },
  ],
  warnings_dict: {
    ATENOLOL: {
      ALPRAZOLAM:
        'Alprazolam may decrease the excretion rate of Amoxicillin which could result in a higher serum level.',
      AMOXICILLIN:
        'Amoxicillin may decrease the excretion rate of Warfarin which could result in a higher serum level.',
    },
    AMOXICILLIN: {
      WARFARIN:
        'Amoxicillin may decrease the excretion rate of Warfarin which could result in a higher serum level.',
    },
  },
}
// Convert minutes since midnight to a percentage of the day
const minutesToPercentOfDay = (minutes) => (minutes / 1440) * 100

// Convert minutes since midnight to a time string
const minutesToTimeString = (minutes) => {
  const date = new Date()
  date.setHours(0, minutes, 0)
  return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
}

const ScheduleTimeline = () => {
  const {userId} = useAuth()
  const [status, setStatus] = useState({})
  const [openSnackbar, setOpenSnackbar] = useState(false)
  // Add the following state variable for the interactions modal
  const [interactionsModalOpen, setInteractionsModalOpen] = useState(false)

  useEffect(() => {
    // Fetch the user's schedule from the database
    // and update the status state variable

    fetch(`localhost:8000/schedule/${userId}`)
      .then((res) => res.json())
      .then((data) => setStatus(data))
  }, [])

  // Function to handle opening the modal
  const handleOpenInteractionsModal = () => {
    setInteractionsModalOpen(true)
  }

  // Function to handle closing the modal
  const handleCloseInteractionsModal = () => {
    setInteractionsModalOpen(false)
  }

  const combinedSchedule = Object.keys(data.schedule).reduce((acc, drug) => {
    data.schedule[drug].forEach((time) => {
      if (!acc[time]) {
        acc[time] = [drug]
      } else {
        acc[time].push(drug)
      }
    })
    return acc
  }, {})

  const extractInteractions = (warningKeys, warningsDict) => {
    const interactions = {}

    // Go through each key-value pair in warning_keys
    warningKeys.forEach((pair) => {
      const key = Object.keys(pair)[0] // Assuming each pair only has one key
      const value = pair[key]

      // Access the warning from warnings_dict using the key and value
      if (warningsDict[key] && warningsDict[key][value]) {
        if (!interactions[key]) {
          interactions[key] = {}
        }

        interactions[key][value] = warningsDict[key][value]
      }
    })

    return interactions
  }

  const interactions = extractInteractions(
    data.warning_keys,
    data.warnings_dict,
  )

  // Updated to work with new data structure
  const handleStatusChange = (time, event) => {
    const newValue = event.target.value
    combinedSchedule[time].forEach((drug) => {
      const key = `${drug}-${time}`
      setStatus((prevStatus) => ({...prevStatus, [key]: newValue}))
    })
  }

  const submitSchedule = () => {
    const hasMissingValues =
      Object.values(status).some((value) => value === '') ||
      Object.keys(status).length === 0
    if (hasMissingValues) {
      setOpenSnackbar(true) // Show Snackbar
      return
    }

    // Convert the status object to the desired format before submission
    const submissionStatus = Object.keys(status).reduce((acc, key) => {
      const time = key.split('-')[1]
      // Save as int
      acc[time] = parseInt(status[key])
      return acc
    }, {})
    console.log('Submission status:', submissionStatus)
    // Add your submit logic here

    fetch('localhost:8000/reschedule', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({...submissionStatus, userId}),
    }).then((response) => {
      if (response.ok) {
        // Handle success
        alert('Schedule saved!')
      } else {
        // Handle error
        alert('Something went wrong!')
      }
    })
  }

  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return
    }
    setOpenSnackbar(false)
  }

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      p={4}
      height="100vh"
      width="100vw"
    >
      <Box sx={{position: 'absolute', top: '13vh', right: 8, zIndex: 10}}>
        <Button color="warning" onClick={handleOpenInteractionsModal}>
          <Warning />
        </Button>
      </Box>
      <InteractionModal
        open={interactionsModalOpen}
        onClose={handleCloseInteractionsModal}
        interactions={interactions}
      />
      <Snackbar
        open={openSnackbar}
        autoHideDuration={2000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity="error"
          sx={{width: '100%'}}
        >
          You must fill all the values before submitting.
        </Alert>
      </Snackbar>
      <Box
        sx={{
          position: 'relative',
          width: '90%',
          height: '100px',
          border: '1px solid',
          borderRadius: '4px',
          mt: '16px',
          backgroundColor: '#f0f0f0',
        }}
      >
        {/* Hour indicators */}
        {Array.from({length: 24}).map((_, index) => (
          <Box
            key={index}
            sx={{
              position: 'absolute',
              left: `${(index / 24) * 100}%`,
              top: 0,
              bottom: 0,
              borderLeft: '1px solid #ddd',
              '&:after': {
                content: `"${index}"`,
                position: 'absolute',
                top: '100%',
                left: '-50%',
                whiteSpace: 'nowrap',
              },
            }}
          />
        ))}
        {/* Drug schedule */}
        {Object.entries(combinedSchedule).map(([time, drugs]) => {
          const left = minutesToPercentOfDay(time)
          const drugNames = drugs.join(', ') // Join drug names into a single string'

          return (
            <Box
              key={time}
              sx={{
                position: 'absolute',
                left: `${left}%`,
                top: '50%',
                transform: 'translate(-50%, -50%)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Box
                sx={{
                  position: 'relative', // Container for the drug names
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                }}
              >
                <Typography
                  variant="caption"
                  sx={{
                    position: 'absolute',
                    whiteSpace: 'nowrap',
                    top: '-40px',
                  }}
                >
                  {drugNames}
                </Typography>
              </Box>
              <FormControl
                size="small"
                sx={{position: 'absolute', bottom: '-30px'}}
              >
                {' '}
                {/* Position the select below */}
                <Select
                  value={status[`${drugs[0]}-${time}`] || ''}
                  onChange={(e) => handleStatusChange(time, e)}
                  displayEmpty
                  sx={{m: 1, minWidth: 80}}
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  <MenuItem value="-1">Behind</MenuItem>
                  <MenuItem value="0">On Time</MenuItem>
                  <MenuItem value="1">Ahead</MenuItem>
                </Select>
              </FormControl>
              <Typography
                variant="caption"
                sx={{
                  position: 'absolute',
                  bottom: '-45px',
                  whiteSpace: 'nowrap',
                }}
              >
                {minutesToTimeString(time)}
              </Typography>
            </Box>
          )
        })}
      </Box>
      <Button
        variant="contained"
        color="primary"
        onClick={() => {
          submitSchedule()
        }}
        sx={{
          position: 'absolute',
          bottom: '16px',
          right: '16px',
        }}
      >
        Submit Schedule
      </Button>
    </Box>
  )
}

export default ScheduleTimeline

const InteractionModal = ({open, onClose, interactions}) => {
  // Flatten the interactions to a list
  const interactionList = Object.entries(interactions).flatMap(
    ([med, warnings]) =>
      Object.entries(warnings).map(([interactionMed, desc]) => ({
        med,
        interactionMed,
        desc,
      })),
  )

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="interaction-modal-title"
      aria-describedby="interaction-modal-description"
    >
      <Box
        // Style the modal here with Material-UI sx prop or create a style object
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
        }}
      >
        <Typography id="interaction-modal-title" variant="h6" component="h2">
          Medication Interactions
        </Typography>
        <Box id="interaction-modal-description" sx={{mt: 2}}>
          {interactionList.map((interaction, index) => (
            <Typography key={index} sx={{mt: 1}}>
              <strong>{interaction.med}:</strong> {interaction.desc}
            </Typography>
          ))}
        </Box>
      </Box>
    </Modal>
  )
}
