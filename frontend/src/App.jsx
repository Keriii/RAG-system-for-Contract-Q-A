import React from 'react'
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom'
import { logo } from "./assets"
import { Home, CreatePost } from "./pages"

const App = () => {
  return (
    <BrowserRouter>
      <div className="app-container">
        <header className="w-full fixed flex justify-between items-center bg-dark sm:px-8 px-4 py-4 border-b border-b-black">
          <Link to="/">
            <h2 className='text-white font-bold'>Lizzy</h2>
          </Link>
          <Link to="/" className="font-inter font-medium text-white px-2 ml-auto">Queries</Link>
          <Link to="/create" className="font-inter font-bold bg-accent text-black px-2 py-1 rounded-md">Ask</Link>
        </header>
        <main className="py-8 w-full bg-hero  min-h-[calc(100vh)]">
          <Routes>
            <Route path="/create" element={<CreatePost />} />
            <Route path="/" element={<Home />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
