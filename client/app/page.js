'use client'

import Image from 'next/image'
import LandingHero from './landingHero'
import Services from './services'
import Process from './process'
import {motion} from 'framer-motion'

export default function Home() {
  return (
    <motion.div
      initial={{opacity: 0}}
      animate={{opacity: 1}}
      exit={{opacity: 0}}
    >
      <LandingHero />
      <Services />
      <Process />
    </motion.div>
  )
}
