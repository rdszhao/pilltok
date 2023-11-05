'use client'

import {
  Box,
  Button,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import {useEffect, useState} from 'react'
import {useAuth} from '@clerk/nextjs'

const mockData = [
  {
    name: 'ATENOLOL',
    dosage: '100 mg',
    time_period: 'TAKE 1 TABLET BY MOUTH BEFORE BEDTIME',
    interactions: ['ALPRAZOLAM', 'AMOXICILLIN'],
  },
  {
    name: 'AMOXICILLIN',
    dosage: '500 MG',
    time_period: 'TAKE 4 CAPSULE MOUTH 1 HOUR',
    interactions: ['WARFARIN'],
  },
]

export default function Medications() {
  const {userId} = useAuth()
  const [medications, setMedications] = useState(mockData)
  const [modified, setModified] = useState(false)

  useEffect(() => {
    // Fetch the user's medications from the database
    // and update the medications state variable
    fetch(`localhost:8000/medications/${userId}`)
      .then((res) => res.json())
      .then((data) => setMedications(data))
  }, [])

  const handleDelete = (medicationId) => {
    setMedications(
      medications.filter((medication) => medication.id !== medicationId),
    )
    setModified(true)
  }

  const handleSave = () => {
    // Save the user's medications to the database
    fetch(`localhost:8000/medications/${userId}`, {
      method: 'POST',
      body: JSON.stringify({
        medications,
        userId,
      }),
    }).then((res) => {
      if (res.ok) {
        setModified(false)
        alert('Medications saved!')
      } else {
        alert('Error saving medications')
      }
    })
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
        Medication List
      </Typography>
      <TableContainer component={Paper} sx={{maxWidth: 800, mb: 4}}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell align="right">Dosage</TableCell>
              <TableCell align="right">Time Period</TableCell>
              <TableCell align="right">Interactions</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {medications.map((medication) => (
              <TableRow
                key={medication.id}
                sx={{'&:last-child td, &:last-child th': {border: 0}}}
              >
                <TableCell component="th" scope="row">
                  {medication.name}
                </TableCell>
                <TableCell align="right">{medication.dosage}</TableCell>
                <TableCell align="right">{medication.time_period}</TableCell>
                <TableCell align="right">
                  {medication.interactions.join(', ')}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    onClick={() => handleDelete(medication.id)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}
