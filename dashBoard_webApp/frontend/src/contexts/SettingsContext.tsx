import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface Settings {
  language: string
  animationsEnabled: boolean
  fontSize: 'small' | 'medium' | 'large'
  profile: {
    name: string
    email: string
    picture: string
  }
}

const defaultSettings: Settings = {
  language: 'en',
  animationsEnabled: true,
  fontSize: 'medium',
  profile: {
    name: 'John Smith',
    email: 'john.smith@example.com',
    picture: ''
  }
}

interface SettingsContextType {
  settings: Settings
  updateSettings: (updates: Partial<Settings>) => void
  resetSettings: () => void
  updateProfile: (updates: Partial<Settings['profile']>) => void
}

const SettingsContext = createContext<SettingsContextType | undefined>(undefined)

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<Settings>(() => {
    const saved = localStorage.getItem('appSettings')
    if (saved) {
      try {
        return { ...defaultSettings, ...JSON.parse(saved) }
      } catch {
        return defaultSettings
      }
    }
    return defaultSettings
  })

  useEffect(() => {
    localStorage.setItem('appSettings', JSON.stringify(settings))
    
    // Apply font size
    const root = document.documentElement
    root.style.fontSize = 
      settings.fontSize === 'small' ? '14px' :
      settings.fontSize === 'large' ? '18px' : '16px'
    
    // Apply animations
    if (!settings.animationsEnabled) {
      root.classList.add('no-animations')
    } else {
      root.classList.remove('no-animations')
    }
  }, [settings])

  const updateSettings = (updates: Partial<Settings>) => {
    setSettings(prev => ({ ...prev, ...updates }))
  }

  const updateProfile = (updates: Partial<Settings['profile']>) => {
    setSettings(prev => ({
      ...prev,
      profile: { ...prev.profile, ...updates }
    }))
  }

  const resetSettings = () => {
    setSettings(defaultSettings)
  }

  return (
    <SettingsContext.Provider value={{ settings, updateSettings, resetSettings, updateProfile }}>
      {children}
    </SettingsContext.Provider>
  )
}

export function useSettings() {
  const context = useContext(SettingsContext)
  if (context === undefined) {
    throw new Error('useSettings must be used within a SettingsProvider')
  }
  return context
}

