param(
    [Parameter(Mandatory = $true)]
    [string]$RunTag,

    [string]$SuiteFile = "tools/multiagent/benchmark_suites/all_agents_harness_suite.json",

    [string]$Candidate = "auto-score",

    [string]$CompareRunTag = "",

    [string]$Hypothesis = ""
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repoRoot

$command = @(
    "python",
    "tools/multiagent/agent_harness_cycle.py",
    $RunTag,
    "--suite-file",
    $SuiteFile,
    "--candidate",
    $Candidate
)

if ($CompareRunTag -ne "") {
    $command += @("--compare-run-tag", $CompareRunTag)
}

if ($Hypothesis -ne "") {
    $command += @("--hypothesis", $Hypothesis)
}

& $command[0] $command[1..($command.Length - 1)]
