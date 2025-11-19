import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import { SettingsProvider } from './contexts/SettingsContext'
import Dashboard from './components/Dashboard'
import Settings from './components/Settings'

function App() {
  return (
    <ThemeProvider>
      <SettingsProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Router>
      </SettingsProvider>
    </ThemeProvider>
  )
}

export default App

