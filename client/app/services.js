import React from 'react'
import {Box, Card, CardContent, Typography, Icon} from '@mui/material'
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh'
import ScheduleIcon from '@mui/icons-material/Schedule'
import MedicationIcon from '@mui/icons-material/Medication'
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive'
const services = [
  {
    title: 'Automated Recognition',
    description: 'Automatically parses your prescription',
    icon: <AutoFixHighIcon fontSize="inherit" />,
  },
  {
    title: 'Adaptive Scheduling',
    description: 'Schedules your medication routine, adapts to your needs',
    icon: <ScheduleIcon fontSize="inherit" />,
  },
  {
    title: 'Interaction Resolution',
    description: 'Checks and resolves drug interactions between medications',
    icon: <MedicationIcon fontSize="inherit" />,
  },
  {
    title: 'Smart Reminders',
    description: 'Sends you reminders when it is time to take your medication',
    icon: <NotificationsActiveIcon fontSize="inherit" />,
  },
]

const ServiceCard = ({title, description, icon}) => (
  <Card
    sx={{
      maxWidth: 200,
      height: 'auto',
      m: 2,
      boxShadow: 3,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      alignItems: 'center',
      padding: 2,
      backgroundColor: 'background.paper',
    }}
  >
    <CardContent
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Icon
        sx={{
          fontSize: 48,
          mb: 2,
        }}
      >
        {icon}
      </Icon>
      <Typography gutterBottom variant="h5" component="div" textAlign="center">
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary" textAlign="center">
        {description}
      </Typography>
    </CardContent>
  </Card>
)

export default function Services() {
  return (
    <Box width="100vw" height="100vh" padding={4}>
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{
          mb: 4,
        }}
      >
        OUR SERVICES
      </Typography>
      <Typography variant="h2" fontWeight="bold" my={2}>
        We Provide
      </Typography>
      <Typography variant="body1" mb={4}>
        All in one medication management solution.
      </Typography>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          flexWrap: 'wrap',
          mt: 10,
        }}
      >
        {services.map((service, index) => (
          <ServiceCard key={index} {...service} />
        ))}
      </Box>
    </Box>
  )
}
