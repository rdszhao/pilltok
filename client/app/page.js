'use client'

import Image from 'next/image'
import LandingHero from './landingHero'
import Services from './services'
import Process from './process'

export default function Home() {
  return (
    <>
      <LandingHero />
      <Services />
      <Process />
    </>
  )
}
