import React from 'react'
import {Box, Card, CardContent, Typography, Icon} from '@mui/material'
import PersonAddIcon from '@mui/icons-material/PersonAdd'
import CameraAltIcon from '@mui/icons-material/CameraAlt'
import FactCheckIcon from '@mui/icons-material/FactCheck'
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive'

const steps = [
  {
    title: 'Register',
    icon: <PersonAddIcon fontSize="inherit" />,
  },
  {
    title: 'Snap',
    icon: <CameraAltIcon fontSize="inherit" />,
  },
  {
    title: 'Review',
    icon: <FactCheckIcon fontSize="inherit" />,
  },
  {
    title: 'Smart Reminders',
    icon: <NotificationsActiveIcon fontSize="inherit" />,
  },
]

const ProcessCard = ({index, title, icon}) => {
  const inverseMarginTop = (steps.length - 1 - index) * 5
  return (
    <Card
      sx={{
        width: 250,
        height: 150,
        mt: inverseMarginTop,
        mx: 2,
        boxShadow: 3,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'center',
        padding: 2,
        backgroundColor: 'background.paper',
        position: 'relative', // Ensure position relative is set here
      }}
    >
      <Icon
        sx={{
          fontSize: 52,
          mb: 2,
          position: 'absolute',
          top: 0,
          left: 0,
          m: 2,
        }}
      >
        {icon}
      </Icon>
      <Typography
        sx={{
          position: 'absolute',
          bottom: 0,
          right: 0,
          textAlign: 'center',
          mr: 1,
          padding: 1, // Add some padding if needed
        }}
        variant="h6"
        component="div"
      >
        {title}
      </Typography>
    </Card>
  )
}

export default function Process() {
  return (
    <Box width="100vw" height="100vh" padding={4}>
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{
          mb: 4,
        }}
      >
        WORK FLOW
      </Typography>
      <Typography variant="h2" fontWeight="bold" my={2}>
        Working Process
      </Typography>
      <Typography variant="body1" mb={4}>
        Easy steps to get started
      </Typography>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          mt: 10,
        }}
      >
        {steps.map((step, index) => (
          <ProcessCard key={index} index={index} {...step} />
        ))}
      </Box>
    </Box>
  )
}
