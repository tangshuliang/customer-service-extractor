#!/bin/bash
# GitHub推送脚本
# 使用方法：
# 1. 修改下面的GITHUB_USERNAME和GITHUB_TOKEN
# 2. 运行：bash push_to_github.sh

GITHUB_USERNAME="YOUR_GITHUB_USERNAME"
GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
REPO_NAME="customer-service-extractor"

# 添加远程仓库
git remote add origin "https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# 推送到GitHub
git push -u origin main

echo "✅ 已成功推送到 GitHub: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
