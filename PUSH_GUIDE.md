# 推送到 GitHub 指南

## 方法一：使用 GitHub CLI（推荐）

### 1. 安装 GitHub CLI
```bash
# Windows (使用 winget)
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh
```

### 2. 登录 GitHub
```bash
gh auth login
```

### 3. 创建仓库并推送
```bash
# 在项目目录下
cd customer-service-extractor

# 创建仓库（公开）
gh repo create customer-service-extractor --public --source=. --push

# 或创建私有仓库
gh repo create customer-service-extractor --private --source=. --push
```

## 方法二：手动推送

### 1. 在 GitHub 上创建仓库
1. 访问 https://github.com/new
2. 填写仓库名称：`customer-service-extractor`
3. 选择公开或私有
4. 不要勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

### 2. 本地推送
```bash
cd customer-service-extractor

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/customer-service-extractor.git

# 推送
git push -u origin main
```

### 3. 如果使用 Personal Access Token
```bash
# 添加远程仓库（使用token）
git remote add origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/customer-service-extractor.git

# 推送
git push -u origin main
```

## 方法三：使用 VS Code

1. 打开项目文件夹
2. 点击左侧 "源代码管理" 图标
3. 点击 "发布到 GitHub"
4. 按照提示完成

## 验证推送

推送完成后，访问：
```
https://github.com/YOUR_USERNAME/customer-service-extractor
```

## 生成 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择有效期和权限（至少需要 `repo` 权限）
4. 生成后复制token

## 项目文件清单

推送前确保包含以下文件：
- ✅ README.md
- ✅ schema.json
- ✅ extractor.py
- ✅ validator.py
- ✅ conversations.json
- ✅ results.json
- ✅ requirements.txt
- ✅ .gitignore
- ✅ .github/workflows/python.yml
- ✅ screenshots/ (目录)
