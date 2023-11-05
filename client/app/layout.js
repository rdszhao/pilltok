import {Inter} from 'next/font/google'
import CustomTheme from './theme'
import {ClerkProvider} from '@clerk/nextjs'
import TopBar from './topbar'
import './globals.css'

const inter = Inter({subsets: ['latin']})

export const metadata = {
  title: 'PilTok',
  description: 'Manage your medications effortlessly.',
}

export default function RootLayout({children}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <CustomTheme>
          <body className={inter.className}>
            {' '}
            {children}
            <TopBar />
          </body>
        </CustomTheme>
      </html>
    </ClerkProvider>
  )
}
