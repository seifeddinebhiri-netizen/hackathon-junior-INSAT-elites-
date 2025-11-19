import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { useTheme } from '@/contexts/ThemeContext'
import { useSettings } from '@/contexts/SettingsContext'
import { 
  Moon, 
  Sun, 
  Languages, 
  Zap, 
  RotateCcw, 
  User, 
  Mail, 
  Image as ImageIcon,
  Lock,
  Type,
  ArrowLeft,
  Save
} from 'lucide-react'

const languages = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'zh', name: '中文' },
  { code: 'ja', name: '日本語' },
]

export default function Settings() {
  const navigate = useNavigate()
  const { theme, toggleTheme } = useTheme()
  const { settings, updateSettings, resetSettings, updateProfile } = useSettings()
  
  const [profileData, setProfileData] = useState(settings.profile)
  const [passwordData, setPasswordData] = useState({
    current: '',
    new: '',
    confirm: ''
  })
  const [showPasswordChange, setShowPasswordChange] = useState(false)

  const handleProfileUpdate = () => {
    updateProfile(profileData)
    alert('Profile updated successfully!')
  }

  const handlePasswordChange = () => {
    if (passwordData.new !== passwordData.confirm) {
      alert('New passwords do not match!')
      return
    }
    if (passwordData.new.length < 8) {
      alert('Password must be at least 8 characters long!')
      return
    }
    // In a real app, this would make an API call
    alert('Password changed successfully!')
    setPasswordData({ current: '', new: '', confirm: '' })
    setShowPasswordChange(false)
  }

  const handleReset = () => {
    if (confirm('Are you sure you want to reset all settings to default values?')) {
      resetSettings()
      setProfileData(settings.profile)
      alert('Settings reset to default values!')
    }
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setProfileData({ ...profileData, picture: reader.result as string })
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="max-w-4xl mx-auto p-6 lg:p-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate('/')}
            className="hover:bg-accent"
          >
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-[#0f2048] dark:text-[#e10010]">Settings</h1>
            <p className="text-sm text-muted-foreground mt-1">Manage your preferences and account</p>
          </div>
        </div>

        <div className="space-y-6">
          {/* Appearance Section */}
          <Card className="bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] p-6">
            <div className="flex items-center gap-3 mb-6">
              {theme === 'dark' ? (
                <Moon className="w-5 h-5 text-[#0f2048] dark:text-white" />
              ) : (
                <Sun className="w-5 h-5 text-[#0f2048] dark:text-white" />
              )}
              <h2 className="text-xl font-bold text-[#0f2048] dark:text-white">Appearance</h2>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b border-[#e5e7eb] dark:border-[#2d3f6b]">
                <div>
                  <p className="font-semibold text-[#0f2048] dark:text-white">Theme</p>
                  <p className="text-sm text-muted-foreground">Switch between light and dark mode</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-muted-foreground">{theme === 'dark' ? 'Dark' : 'Light'}</span>
                  <Switch
                    checked={theme === 'dark'}
                    onCheckedChange={() => toggleTheme()}
                    className="data-[state=checked]:bg-white data-[state=unchecked]:bg-white shadow-[0_0_4px_#e10010] focus:ring-[#e10010]"
                  />
                </div>
              </div>
            </div>
          </Card>

          {/* Language Section */}
          <Card className="bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] p-6">
            <div className="flex items-center gap-3 mb-6">
              <Languages className="w-5 h-5 text-[#0f2048] dark:text-white" />
              <h2 className="text-xl font-bold text-[#0f2048] dark:text-white">Language</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                  Select Language
                </label>
                <select
                  value={settings.language}
                  onChange={(e) => updateSettings({ language: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-md bg-[#f9fafb] dark:bg-[#0f2048] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white font-semibold focus:outline-none focus:ring-2 focus:ring-[#0f2048] dark:focus:ring-white focus:border-[#0f2048] dark:focus:border-white"
                >
                  {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </Card>

          {/* Accessibility Section */}
          <Card className="bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] p-6">
            <div className="flex items-center gap-3 mb-6">
              <Zap className="w-5 h-5 text-[#0f2048] dark:text-white" />
              <h2 className="text-xl font-bold text-[#0f2048] dark:text-white">Accessibility</h2>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b border-[#e5e7eb] dark:border-[#2d3f6b]">
                <div>
                  <p className="font-semibold text-[#0f2048] dark:text-white">Animations</p>
                  <p className="text-sm text-muted-foreground">Disable animations for motion-sensitive users</p>
                </div>
                <Switch
                  checked={settings.animationsEnabled}
                  onCheckedChange={(checked: boolean) => updateSettings({ animationsEnabled: checked })}
                  className="data-[state=checked]:bg-white data-[state=unchecked]:bg-white shadow-[0_0_4px_#e10010] focus:ring-[#e10010]"
                />
              </div>

              <div className="pt-3">
                <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                  Font Size
                </label>
                <div className="flex gap-2">
                  {(['small', 'medium', 'large'] as const).map((size) => (
                    <Button
                      key={size}
                      variant={settings.fontSize === size ? 'default' : 'outline'}
                      onClick={() => updateSettings({ fontSize: size })}
                      className={`flex-1 ${
                        settings.fontSize === size
                          ? 'bg-[#0f2048] dark:bg-white text-white dark:text-[#0f2048]'
                          : 'border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white'
                      }`}
                    >
                      <Type className="w-4 h-4 mr-2" />
                      {size.charAt(0).toUpperCase() + size.slice(1)}
                    </Button>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          {/* Profile Management Section */}
          <Card className="bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] p-6">
            <div className="flex items-center gap-3 mb-6">
              <User className="w-5 h-5 text-[#0f2048] dark:text-white" />
              <h2 className="text-xl font-bold text-[#0f2048] dark:text-white">Profile Management</h2>
            </div>
            
            <div className="space-y-6">
              {/* Profile Picture */}
              <div>
                <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                  Profile Picture
                </label>
                <div className="flex items-center gap-4">
                  <div className="w-20 h-20 rounded-full bg-[#0f2048] dark:bg-white flex items-center justify-center overflow-hidden">
                    {profileData.picture ? (
                      <img src={profileData.picture} alt="Profile" className="w-full h-full object-cover" />
                    ) : (
                      <User className="w-10 h-10 text-white dark:text-[#0f2048]" />
                    )}
                  </div>
                  <label className="cursor-pointer">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                    <Button
                      variant="outline"
                      className="border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white"
                    >
                      <ImageIcon className="w-4 h-4 mr-2" />
                      Upload Image
                    </Button>
                  </label>
                </div>
              </div>

              {/* Name */}
              <div>
                <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={profileData.name}
                  onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-md bg-[#f9fafb] dark:bg-[#0f2048] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0f2048] dark:focus:ring-white focus:border-[#0f2048] dark:focus:border-white"
                  placeholder="Enter your name"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={profileData.email}
                  onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-md bg-[#f9fafb] dark:bg-[#0f2048] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0f2048] dark:focus:ring-white focus:border-[#0f2048] dark:focus:border-white"
                  placeholder="Enter your email"
                />
              </div>

              <Button
                onClick={handleProfileUpdate}
                className="w-full bg-[#0f2048] dark:bg-white text-white dark:text-[#0f2048] hover:bg-[#0f2048]/90 dark:hover:bg-white/90"
              >
                <Save className="w-4 h-4 mr-2" />
                Save Profile Changes
              </Button>
            </div>
          </Card>

          {/* Password Change Section */}
          <Card className="bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Lock className="w-5 h-5 text-[#0f2048] dark:text-white" />
                <h2 className="text-xl font-bold text-[#0f2048] dark:text-white">Password Change</h2>
              </div>
              <Button
                variant="outline"
                onClick={() => setShowPasswordChange(!showPasswordChange)}
                className="border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white"
              >
                {showPasswordChange ? 'Cancel' : 'Change Password'}
              </Button>
            </div>
            
            {showPasswordChange && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                    Current Password
                  </label>
                  <input
                    type="password"
                    value={passwordData.current}
                    onChange={(e) => setPasswordData({ ...passwordData, current: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-md bg-[#f9fafb] dark:bg-[#0f2048] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0f2048] dark:focus:ring-white focus:border-[#0f2048] dark:focus:border-white"
                    placeholder="Enter current password"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                    New Password
                  </label>
                  <input
                    type="password"
                    value={passwordData.new}
                    onChange={(e) => setPasswordData({ ...passwordData, new: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-md bg-[#f9fafb] dark:bg-[#0f2048] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0f2048] dark:focus:ring-white focus:border-[#0f2048] dark:focus:border-white"
                    placeholder="Enter new password (min. 8 characters)"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-[#0f2048] dark:text-white mb-2">
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    value={passwordData.confirm}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-md bg-[#f9fafb] dark:bg-[#0f2048] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] text-[#0f2048] dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0f2048] dark:focus:ring-white focus:border-[#0f2048] dark:focus:border-white"
                    placeholder="Confirm new password"
                  />
                </div>

                <Button
                  onClick={handlePasswordChange}
                  className="w-full bg-[#e10010] text-white hover:bg-[#e10010]/90"
                >
                  <Lock className="w-4 h-4 mr-2" />
                  Update Password
                </Button>
              </div>
            )}
          </Card>

          {/* Reset Settings Section */}
          <Card className="bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] p-6">
            <div className="flex items-center gap-3 mb-6">
              <RotateCcw className="w-5 h-5 text-[#e10010]" />
              <h2 className="text-xl font-bold text-[#0f2048] dark:text-white">Reset Settings</h2>
            </div>
            
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Reset all settings to their default values. This action cannot be undone.
              </p>
              <Button
                variant="outline"
                onClick={handleReset}
                className="border-2 border-[#e10010] text-[#e10010] hover:bg-[#e10010] hover:text-white"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Reset All Settings
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
