# Student Placement Prediction Portal - Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Student Placement Prediction Portal" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Yellow
Write-Host ""

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
	Write-Host "Using project virtual environment..." -ForegroundColor Green
	& $venvPython "app.py"
} else {
	Write-Host "Virtual environment not found. Trying Python launcher..." -ForegroundColor Yellow
	py -3.12 app.py
}
