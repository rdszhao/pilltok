import {Inter} from 'next/font/google'
import CustomTheme from './theme'
import {ClerkProvider} from '@clerk/nextjs'
import './globals.css'

const inter = Inter({subsets: ['latin']})

export const metadata = {
  title: 'PilTok',
  description: 'Manage your medications effortlessly.',
}

export default function RootLayout({children}) {
  return (
    <ClerkProvider>
      <CustomTheme>
        <html lang="en">
          <body className={inter.className}>{children}</body>
        </html>
      </CustomTheme>
    </ClerkProvider>
  )
}
