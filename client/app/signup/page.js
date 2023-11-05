'use client'
import {SignUp} from '@clerk/nextjs'
import {Box, CircularProgress} from '@mui/material'
import Image from 'next/image'
import {motion} from 'framer-motion'
import {useAuth} from '@clerk/nextjs'

const MotionBox = motion(Box)

export default function Page() {
  const {isLoaded} = useAuth()
  const imageAnimation = {
    y: [-10, 10], // Image moves up to -20px, back to 0, down to 20px, and back to 0
    transition: {
      duration: 4, // The duration for a complete cycle of the animation
      ease: 'easeInOut',
      repeat: Infinity, // Loop the animation indefinitely
      repeatType: 'reverse', // The animation will reverse after each iteration
      repeatDelay: 0, // No delay between repetitions
    },
  }
  return (
    <MotionBox
      key="signup"
      width="100vw"
      height="100vh"
      display="flex"
      flexDirection="row"
      initial={{
        opacity: 0,
        background:
          'linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(158,214,182,1) 50%, rgba(255,255,255,1) 100%)', // White to middle color to white
      }}
      animate={{
        opacity: 1,
        background:
          'linear-gradient(90deg, rgba(144,238,144,1) 0%, rgba(255,255,255,1) 100%)', // Green to white
      }}
      exit={{
        opacity: 0,
        background:
          'linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(158,214,182,1) 50%, rgba(255,255,255,1) 100%)', // White to middle color to white
      }}
      transition={{duration: 1}}
      justifyContent="center"
      alignItems="center"
      sx={{
        background:
          'linear-gradient(90deg, rgba(144,238,144,1) 0%, rgba(255,255,255,1) 100%)',
      }}
    >
      {!isLoaded ? (
        <CircularProgress />
      ) : (
        <MotionBox
          initial={{opacity: 0}}
          animate={{opacity: 1}}
          exit={{opacity: 0}}
          transition={{duration: 0.5}}
          width="70%"
          height="80%"
          padding={4}
          backgroundColor="white"
          display="flex"
          flexDirection="row"
          justifyContent="center"
          alignItems="center"
        >
          <Box height="80%" width="50%">
            <motion.div animate={imageAnimation}>
              <Image src="/joy.png" width={400} height={400} alt="Joy" />
            </motion.div>
          </Box>
          <SignUp />
        </MotionBox>
      )}
    </MotionBox>
  )
}
