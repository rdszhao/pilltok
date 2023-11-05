'use client'
import {motion, useScroll, useTransform} from 'framer-motion'
import {useRouter} from 'next/navigation'
import {Box, Stack, Typography, Button} from '@mui/material'
import {SignedIn, SignedOut, UserButton} from '@clerk/nextjs'

const MotionBox = motion(Box)

export default function TopBar() {
  const router = useRouter()
  const {scrollYProgress} = useScroll()

  // Adjust the range of the scrollYProgress to alpha values
  const backgroundColorAlpha = useTransform(scrollYProgress, [0, 0.3], [0, 0.3])
  // Make sure alpha doesn't exceed 0.3
  const clampedAlpha = useTransform(backgroundColorAlpha, (alpha) =>
    Math.min(alpha, 0.3),
  )
  // Use the animated alpha value to set the background color
  const backgroundColor = useTransform(
    clampedAlpha,
    (alpha) => `rgba(27, 26, 46, ${alpha})`,
  )

  // Handle the backdropFilter and boxShadow similarly, ensuring they reset to 'none' smoothly
  const backdropFilter = useTransform(
    scrollYProgress,
    [0, 0.3],
    ['none', 'blur(10px)'],
  )

  return (
    <MotionBox
      position="fixed"
      width="100vw"
      height="10vh"
      display="flex"
      flexDirection="row"
      justifyContent="space-between"
      alignItems="center"
      top={0}
      left={0}
      zIndex={1000}
      paddingX={5}
      style={{
        backgroundColor,
        backdropFilter,
      }}
      initial={{
        backgroundColor: 'rgba(27, 26, 46, 0)',
        backdropFilter: 'none',
        boxShadow: 'none',
      }}
      // No need for 'animate' or 'transition' here since we're using useTransform
    >
      <Typography variant="h4" color="primary" onClick={() => router.push('/')}>
        PillTok
      </Typography>
      <SignedIn>
        <Stack direction="row" spacing={2}>
          <Button
            variant="text"
            color="primary"
            onClick={() => router.push('/dashboard')}
          >
            Dashboard
          </Button>
          <Button
            variant="text"
            color="primary"
            onClick={() => router.push('/upload')}
          >
            Picture
          </Button>
          <UserButton />
        </Stack>
      </SignedIn>
      <SignedOut>
        <Stack direction="row" spacing={2}>
          <Button
            variant="text"
            color="primary"
            onClick={() => router.push('/signin')}
          >
            Login
          </Button>
          <Button
            variant="text"
            color="primary"
            onClick={() => router.push('/signup')}
          >
            Signup
          </Button>
        </Stack>
      </SignedOut>
    </MotionBox>
  )
}
