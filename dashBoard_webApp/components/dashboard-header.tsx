export default function DashboardHeader() {
  return (
    <header className="border-b border-border bg-card">
      <div className="px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-lg">DG</span>
            </div>
            <h1 className="text-2xl font-bold text-text-pretty">DriveGuard AI</h1>
          </div>
          <p className="text-muted-foreground text-sm">Insurance Dashboard</p>
        </div>
      </div>
    </header>
  )
}
