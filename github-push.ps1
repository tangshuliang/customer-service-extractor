# GitHub 推送脚本 - 交互式
# 运行方式: PowerShell -ExecutionPolicy Bypass -File github-push.ps1

param(
    [string]$Username = "",
    [string]$Token = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub 仓库推送工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 如果没有提供参数，则交互式输入
if (-not $Username) {
    $Username = Read-Host "请输入您的 GitHub 用户名"
}

if (-not $Token) {
    $Token = Read-Host "请输入您的 GitHub Personal Access Token" -AsSecureString
    $Token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Token))
}

if (-not $Username -or -not $Token) {
    Write-Host "❌ 用户名和Token不能为空" -ForegroundColor Red
    exit 1
}

$RepoName = "customer-service-extractor"

Write-Host ""
Write-Host "正在推送到 GitHub..." -ForegroundColor Yellow
Write-Host "仓库: $RepoName" -ForegroundColor Gray
Write-Host "用户: $Username" -ForegroundColor Gray
Write-Host ""

# 检查远程仓库是否已存在
git remote remove origin 2>$null

# 添加远程仓库
git remote add origin "https://${Username}:${Token}@github.com/${Username}/${RepoName}.git"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 添加远程仓库失败" -ForegroundColor Red
    exit 1
}

# 推送
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✅ 推送成功！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "仓库地址: https://github.com/${Username}/${RepoName}" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ 推送失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因:" -ForegroundColor Yellow
    Write-Host "  1. Token 没有 repo 权限" -ForegroundColor Yellow
    Write-Host "  2. 仓库不存在，需要先创建" -ForegroundColor Yellow
    Write-Host "  3. 网络连接问题" -ForegroundColor Yellow
    Write-Host ""
    
    # 尝试创建仓库
    Write-Host "是否尝试自动创建仓库? (y/n)" -ForegroundColor Cyan
    $create = Read-Host
    if ($create -eq "y") {
        Write-Host "正在创建仓库..." -ForegroundColor Yellow
        
        $body = @{
            name = $RepoName
            description = "客服对话结构化信息提取工具 - AI测评任务"
            private = $false
            auto_init = $false
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method POST -Headers @{
                "Authorization" = "token $Token"
                "Accept" = "application/vnd.github.v3+json"
            } -Body $body -ContentType "application/json"
            
            Write-Host "✅ 仓库创建成功，重新推送..." -ForegroundColor Green
            git push -u origin main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "========================================" -ForegroundColor Green
                Write-Host "  ✅ 推送成功！" -ForegroundColor Green
                Write-Host "========================================" -ForegroundColor Green
                Write-Host ""
                Write-Host "仓库地址: https://github.com/${Username}/${RepoName}" -ForegroundColor Cyan
            }
        } catch {
            Write-Host "❌ 创建仓库失败: $_" -ForegroundColor Red
        }
    }
}

# 清除token
$Token = $null
