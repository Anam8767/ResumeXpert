# HireLens Auto-Start PowerShell Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    HireLens Auto-Start System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set project path
$projectPath = "d:\Windsurf\Hire lens FYP\hire_lens-dev"
Set-Location $projectPath

# Function to check if backend is running
function Test-BackendRunning {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# Check and start backend
Write-Host "🔍 Checking backend status..." -ForegroundColor Yellow
if (Test-BackendRunning) {
    Write-Host "✅ Backend is already running!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend not running, starting it..." -ForegroundColor Red
    Start-Process -FilePath "python" -ArgumentList "-m uvicorn app:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Minimized
    
    # Wait for backend to start
    Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
    $timeout = 30
    $timer = 0
    while ($timer -lt $timeout) {
        if (Test-BackendRunning) {
            Write-Host "✅ Backend started successfully!" -ForegroundColor Green
            break
        }
        Start-Sleep -Seconds 1
        $timer++
    }
    
    if ($timer -ge $timeout) {
        Write-Host "❌ Backend failed to start within timeout" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit
    }
}

# Start frontend
Write-Host ""
Write-Host "🚀 Starting frontend..." -ForegroundColor Cyan
Set-Location "$projectPath\frontend"
Start-Process -FilePath "npm" -ArgumentList "run dev" -WindowStyle Normal

Write-Host ""
Write-Host "✅ HireLens is now running!" -ForegroundColor Green
Write-Host "🔗 Backend: http://localhost:8000" -ForegroundColor Blue
Write-Host "🔗 Frontend: http://localhost:5173" -ForegroundColor Blue
Write-Host ""
Write-Host "📝 Keep this window open to maintain backend connection" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Red

# Keep script running
try {
    while ($true) {
        if (-not (Test-BackendRunning)) {
            Write-Host "❌ Backend stopped, restarting..." -ForegroundColor Red
            Start-Process -FilePath "python" -ArgumentList "-m uvicorn app:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Minimized
        }
        Start-Sleep -Seconds 10
    }
} catch {
    Write-Host "👋 Shutting down HireLens..." -ForegroundColor Yellow
}
