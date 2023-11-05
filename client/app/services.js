import React, {useRef} from 'react'
import {Box, Card, CardContent, Typography, Icon} from '@mui/material'
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh'
import ScheduleIcon from '@mui/icons-material/Schedule'
import MedicationIcon from '@mui/icons-material/Medication'
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive'
import {useInView, motion} from 'framer-motion'

const stepVariants = {
  visible: (i) => ({
    opacity: 1,
    translateY: 0,
    transition: {
      delay: i * 0.4 + 1,
    },
  }),
  hidden: {opacity: 0, translateY: -100},
}

const titleVariants = {
  visible: {opacity: 1, transition: {duration: 0.5, delay: 0.5}},
  hidden: {opacity: 0},
}

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

const ServiceCard = ({title, description, index, icon, isInView}) => (
  <motion.div
    variants={stepVariants}
    initial="hidden"
    animate={isInView ? 'visible' : 'hidden'}
    custom={index}
  >
    <Card
      sx={{
        maxWidth: 200,
        height: 300,
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
        <Typography
          gutterBottom
          variant="h5"
          component="div"
          textAlign="center"
        >
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" textAlign="center">
          {description}
        </Typography>
      </CardContent>
    </Card>
  </motion.div>
)

export default function Services() {
  const ref = useRef()
  const isInView = useInView(ref, {once: true, amount: 0.5})
  return (
    <Box ref={ref} width="100vw" height="100vh" padding={4}>
      <motion.div
        variants={titleVariants}
        initial="hidden"
        animate={isInView ? 'visible' : 'hidden'}
      >
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
      </motion.div>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          flexWrap: 'wrap',
          mt: 10,
        }}
      >
        {services.map((service, index) => (
          <ServiceCard
            key={index}
            index={index}
            isInView={isInView}
            {...service}
          />
        ))}
      </Box>
    </Box>
  )
}
