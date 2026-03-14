@echo off
echo ========================================
echo  Student Placement Prediction Portal
echo ========================================
echo.
echo Starting application...
echo.

if exist ".venv\Scripts\python.exe" (
	echo Using project virtual environment...
	.venv\Scripts\python.exe app.py
) else (
	echo Virtual environment not found. Trying Python launcher...
	py -3.12 app.py
)

pause
