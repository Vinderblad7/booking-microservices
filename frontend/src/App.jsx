import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <main>
      <h1>Travel Booking</h1>
      <p>Find your perfect trip with our easy-to-use booking platform.</p>
    </main>
  )
}

export default App
