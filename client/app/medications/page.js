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


export default function Medications() {
  const {userId} = useAuth()
  const [medications, setMedications] = useState([])
  const [modified, setModified] = useState(false)

  useEffect(() => {
    // Fetch the user's medications from the database
    // and update the medications state variable
    fetch(`http://localhost:8000/medications/${userId}`)
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
    const obj = {
      "data": medications,
      "user_id": userId
    }
    console.log(obj)
    // Save the user's medications to the database
    fetch(`http://localhost:8000/medications`, {
      method: 'POST',
      body: JSON.stringify(obj),
      headers: {
        'Content-Type': 'application/json',
      },
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
            {medications.map((medication, index) => (
              <TableRow
                key={index}
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
      {modified && (
        <Button variant="contained" color="primary" onClick={()=>{
          handleSave()
        }}>
          Save
        </Button>
      )}
    </Box>
  )
}
