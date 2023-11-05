import {Box, Typography, Button} from '@mui/material'

export default function LandingHero() {
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
      <Box
        sx={{
          position: 'relative',
          zIndex: 2,
          textShadow: '1px 1px 5px rgba(0, 0, 0, 0.2)',
          textAlign: 'center',
        }}
      >
        <Typography variant="h1" color="text.main" gutterBottom>
          PillTok
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Manage your medications effortlessly.
        </Typography>
        <Typography variant="body1" color="text.secondary" mb={4}>
          PillTok simplifies your medication routine with smart reminders and
          health tracking.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          sx={{
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)',
            textTransform: 'none',
            fontSize: '1rem',
            padding: '10px 20px',
            borderRadius: '25px',
            background: 'linear-gradient(to right, #12c2e9, #c471ed, #f64f59)',
            backgroundSize: '300% 100%', // increase the size of the gradient
            transition: 'all 0.5s ease-in-out', // animate all properties
            '&:hover': {
              backgroundPosition: '100% 0', // change the position of the gradient
            },
          }}
        >
          Get Started
        </Button>
      </Box>
    </Box>
  )
}
