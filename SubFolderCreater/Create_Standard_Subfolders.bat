@echo off
setlocal enabledelayedexpansion

REM =============================================================================
REM Create_Standard_Subfolders.bat
REM Version: 1.2
REM Author: Divyansh Jaiswal
REM Last Updated: 2025-06-12
REM Changelog: Replaced individual folder creation calls with a loop for cleaner logic
REM Purpose: Create standardized folder structure in immediate subfolders only
REM =============================================================================

REM Get the current directory where the script is located
set "SCRIPT_DIR=%~dp0"
set "LOG_FILE=%SCRIPT_DIR%created_folders_log.txt"

REM Define the folders to be created in each subfolder
set "FOLDER1=Maya-Blender files"
set "FOLDER2=MD files"
set "FOLDER3=Output format files"
set "FOLDER4=Materials"

REM Function to get formatted timestamp
call :GetTimestamp TIMESTAMP

echo Starting folder structure creation...
echo [%TIMESTAMP%] Script started >> "%LOG_FILE%"

REM Counter for created and existing folders
set /a CREATED_COUNT=0
set /a EXISTING_COUNT=0

REM Loop through immediate subfolders only (1-level deep)
for /d %%D in ("%SCRIPT_DIR%*") do (
    REM Get the folder name without path
    set "SUBFOLDER=%%~nxD"
    set "SUBFOLDER_PATH=%%D"
    
    echo Processing subfolder: !SUBFOLDER!
    
    REM Create each required folder if it doesn't exist using loop optimization
    for %%F in ("%FOLDER1%" "%FOLDER2%" "%FOLDER3%" "%FOLDER4%") do (
        call :CreateFolderIfNeeded "!SUBFOLDER_PATH!" "%%~F"
    )
)

REM Final summary
call :GetTimestamp TIMESTAMP
echo [%TIMESTAMP%] Script completed. Created: %CREATED_COUNT%, Already existed: %EXISTING_COUNT% >> "%LOG_FILE%"
echo.
echo Script completed successfully!
echo Created folders: %CREATED_COUNT%
echo Already existing folders: %EXISTING_COUNT%
echo Check '%LOG_FILE%' for detailed log.

pause
goto :eof

REM =============================================================================
REM Function: CreateFolderIfNeeded
REM Parameters: %1 = Parent folder path, %2 = Folder name to create
REM =============================================================================
:CreateFolderIfNeeded
set "PARENT_PATH=%~1"
set "FOLDER_NAME=%~2"
set "FULL_PATH=%PARENT_PATH%\%FOLDER_NAME%"

if exist "%FULL_PATH%" (
    call :GetTimestamp TIMESTAMP
    echo [!TIMESTAMP!] ⚠️ Already exists: !FULL_PATH! >> "%LOG_FILE%"
    set /a EXISTING_COUNT+=1
) else (
    mkdir "%FULL_PATH%" 2>nul
    if !errorlevel! equ 0 (
        call :GetTimestamp TIMESTAMP
        echo [!TIMESTAMP!] ✅ Created: !FULL_PATH! >> "%LOG_FILE%"
        set /a CREATED_COUNT+=1
    ) else (
        call :GetTimestamp TIMESTAMP
        echo [!TIMESTAMP!] ❌ Failed to create: !FULL_PATH! >> "%LOG_FILE%"
    )
)
goto :eof

REM =============================================================================
REM Function: GetTimestamp
REM Returns formatted timestamp in YYYY-MM-DD HH:MM:SS format
REM Parameter: %1 = Variable name to store timestamp
REM =============================================================================
:GetTimestamp
REM Parse date (format may vary by system locale)
for /f "tokens=1-3 delims=/.- " %%a in ('date /t') do (
    set "DATE_PART=%%c-%%a-%%b"
)

REM Parse time and remove milliseconds
for /f "tokens=1-3 delims=:. " %%a in ('time /t') do (
    set "TIME_PART=%%a:%%b:%%c"
)

REM Handle time format variations (12-hour vs 24-hour)
set "TIME_PART=%TIME_PART: =%"
if "%TIME_PART:~2,1%"==":" (
    set "TIME_PART=0%TIME_PART%"
)

REM Set the timestamp variable
set "%1=%DATE_PART% %TIME_PART%"
goto :eof 