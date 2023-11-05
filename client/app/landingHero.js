import {Box, Typography, Button} from '@mui/material'
import {useAuth} from '@clerk/nextjs'
import {useRouter} from 'next/navigation'
import {motion} from 'framer-motion'

// Define the animation variants
const containerVariants = {
  hidden: {opacity: 0},
  visible: {
    opacity: 1,
    transition: {duration: 0.5, when: 'beforeChildren', staggerChildren: 0.3},
  },
}

const itemVariants = {
  hidden: {opacity: 0, y: -20},
  visible: {opacity: 1, y: 0, transition: {duration: 0.5}},
}

const MotionTypography = motion(Typography)
const MotionButton = motion(Button)

export default function LandingHero() {
  const {isLoaded, userId} = useAuth()
  const router = useRouter()
  return (
    <Box
      sx={{
        width: '100vw',
        height: '100vh',
        bgcolor: 'background.default',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        p: 4, // padding
        backgroundImage:
          'linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(7, 177, 77, 0.3) 100%)',
        boxShadow: 'inset 0 0 20px rgba(0, 0, 0, 0.1)',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundImage: `url(hero.png)`,
          backgroundSize: 'cover',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center center',
          zIndex: 1,
          opacity: 0.2,
        },
        '&::after': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background:
            'linear-gradient(to bottom, rgba(255,255,255,0.8) 0%,rgba(255,255,255,0) 100%)',
        },
      }}
    >
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        style={{position: 'relative', zIndex: 2, textAlign: 'center'}}
      >
        <MotionTypography
          variant="h1"
          color="text.main"
          gutterBottom
          variants={itemVariants}
        >
          PillTok
        </MotionTypography>
        <MotionTypography
          variant="h5"
          color="text.secondary"
          paragraph
          variants={itemVariants}
        >
          Manage your medications effortlessly.
        </MotionTypography>
        <MotionTypography
          variant="body1"
          color="text.secondary"
          mb={4}
          variants={itemVariants}
        >
          PillTok simplifies your medication routine with smart reminders and
          health tracking.
        </MotionTypography>
        <MotionButton
          variant="contained"
          color="primary"
          size="large"
          onClick={() => {
            if (userId) {
              router.push('/dashboard')
            } else {
              router.push('/signup')
            }
          }}
          variants={itemVariants}
          sx={{
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)',
            textTransform: 'none',
            fontSize: '1rem',
            padding: '10px 20px',
            borderRadius: '25px',
            background: 'linear-gradient(to right, #12c2e9, #c471ed, #f64f59)',
            backgroundSize: '300% 100%', // increase the size of the gradient
            transition: 'background-position 0.5s ease-in-out',
            '&:hover': {
              backgroundPosition: '100% 0', // change the position of the gradient
            },
          }}
        >
          Get Started
        </MotionButton>
      </motion.div>
    </Box>
  )
}
