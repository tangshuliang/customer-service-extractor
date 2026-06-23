# PowerShell 推送脚本
# 使用方法：
# 1. 修改 $GitHubUsername 和 $GitHubToken
# 2. 运行：.\push.ps1

$GitHubUsername = "YOUR_GITHUB_USERNAME"  # 替换为您的GitHub用户名
$GitHubToken = "YOUR_GITHUB_TOKEN"         # 替换为您的GitHub Token
$RepoName = "customer-service-extractor"

# 检查是否已配置远程仓库
$remote = git remote -v 2>$null
if ($remote -match "origin") {
    Write-Host "远程仓库已存在，直接推送..." -ForegroundColor Yellow
    git push -u origin main
} else {
    Write-Host "添加远程仓库..." -ForegroundColor Green
    git remote add origin "https://${GitHubUsername}:${GitHubToken}@github.com/${GitHubUsername}/${RepoName}.git"
    
    Write-Host "推送到 GitHub..." -ForegroundColor Green
    git push -u origin main
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 已成功推送到 GitHub!" -ForegroundColor Green
    Write-Host "仓库地址: https://github.com/${GitHubUsername}/${RepoName}"
} else {
    Write-Host "❌ 推送失败，请检查用户名和Token" -ForegroundColor Red
}
