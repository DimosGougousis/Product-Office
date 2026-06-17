#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Register a scheduled YUUP run in Windows Task Scheduler.

.DESCRIPTION
  Creates a scheduled task that invokes YUUP via Claude Code CLI on a cadence.
  Respects budget caps by wrapping in a timeout gate. Logs to governance/runs/.

.PARAMETER TaskName
  Friendly name for the scheduled task.

.PARAMETER Objective
  The YUUP objective to run (same as /yuup argument).

.PARAMETER Schedule
  Task Scheduler trigger string: "Daily", "Hourly", "At 09:00", etc.

.PARAMETER MaxMinutes
  Budget cap in minutes (default 15). Kills the process if exceeded.

.EXAMPLE
  .\scripts\yuup-schedule.ps1 -TaskName "Daily PRD Review" `
    -Objective "Review active PRDs for completeness and flag gaps" `
    -Schedule "Daily at 08:00"

.NOTES
  Requires running as Administrator to register scheduled tasks.
  Uses the current user's Claude Code installation.
#>

param(
    [Parameter(Mandatory)]
    [string]$TaskName,

    [Parameter(Mandatory)]
    [string]$Objective,

    [Parameter(Mandatory)]
    [string]$Schedule,

    [int]$MaxMinutes = 15
)

$ErrorActionPreference = "Stop"

# Resolve paths
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$RunSlug = ($Objective -replace '[^a-zA-Z0-9-]', '-').TrimStart('-').TrimEnd('-')
if ($RunSlug.Length -gt 40) { $RunSlug = $RunSlug.Substring(0, 40) }
$RunId = "yuup-" + (Get-Date -Format "yyyy-MM-dd") + "-" + $RunSlug
$LogDir = Join-Path $RepoRoot "governance" "runs"
$ScriptPath = Join-Path $RepoRoot "scripts" "yuup-run-scheduled.ps1"

# Ensure log directory exists
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# Build the action: run a wrapper PowerShell script
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" -Objective `"$Objective`" -RunId `"$RunId`" -RepoRoot `"$RepoRoot`" -MaxMinutes $MaxMinutes"

# Parse the schedule trigger
$Trigger = switch -Wildcard ($Schedule) {
    "Daily*" {
        $time = if ($Schedule -match '\d{2}:\d{2}') { $matches[0] } else { "08:00" }
        New-ScheduledTaskTrigger -Daily -At $time
    }
    "Hourly*" {
        New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) `
            -RepetitionInterval (New-TimeSpan -Hours 1) `
            -RepetitionDuration ([TimeSpan]::MaxValue)
    }
    "Weekly*" {
        $time = if ($Schedule -match '\d{2}:\d{2}') { $matches[0] } else { "08:00" }
        $day = if ($Schedule -match 'Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday') { $matches[0] } else { "Monday" }
        New-ScheduledTaskTrigger -Weekly -DaysOfWeek $day -At $time
    }
    default {
        Write-Error "Unsupported schedule: $Schedule. Use 'Daily at HH:MM', 'Hourly', or 'Weekly Day at HH:MM'"
        exit 1
    }
}

# Task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes ($MaxMinutes + 5))

# Register the task
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "YUUP unattended run: $Objective" `
    -Force

Write-Host ""
Write-Host "===== Scheduled YUUP Run Registered =====" -ForegroundColor Green
Write-Host "Task:        $TaskName"
Write-Host "Objective:   $Objective"
Write-Host "Schedule:    $Schedule"
Write-Host "Max runtime: $MaxMinutes min"
Write-Host "Run ID:      $RunId"
Write-Host ""
Write-Host "To view:     taskschd.msc"
Write-Host "To remove:   Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
Write-Host "To run now:  Start-ScheduledTask -TaskName '$TaskName'"
