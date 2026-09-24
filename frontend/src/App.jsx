import { useState } from 'react'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import PopularDestinations from './components/DestinationCard/PopularDestinations.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Header />
      <Hero />
    </>
  )
}

export default App
