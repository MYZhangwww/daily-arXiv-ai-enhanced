# Windows PowerShell 版本的运行脚本
# run.ps1 - Windows PowerShell version of run.sh

# 设置错误处理
$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   daily-arXiv-ai-enhanced - Windows PowerShell 版本        ║" -ForegroundColor Cyan
Write-Host "║   Windows PowerShell Version                              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# 环境变量检查
Write-Host "`n=== 环境变量检查 / Environment Check ===" -ForegroundColor Yellow

# 检查 OPENAI_API_KEY
if ([string]::IsNullOrEmpty($env:OPENAI_API_KEY)) {
    Write-Host "⚠️  未设置 OPENAI_API_KEY / OPENAI_API_KEY not set" -ForegroundColor Yellow
    Write-Host "📝 可选的环境变量 / Optional variables:" -ForegroundColor Cyan
    Write-Host "   `$env:OPENAI_API_KEY = 'your-api-key'"
    Write-Host "   `$env:OPENAI_BASE_URL = 'https://api.openai.com/v1'"
    Write-Host "   `$env:LANGUAGE = 'Chinese'"
    Write-Host "   `$env:CATEGORIES = 'cs.CV, cs.CL'"
    Write-Host "   `$env:MODEL_NAME = 'gpt-4o-mini'"
    Write-Host ""
    Write-Host "📢 飞书通知配置 / Feishu Notification (Optional):" -ForegroundColor Cyan
    Write-Host "   `$env:FEISHU_WEBHOOK_URL = 'https://open.feishu.cn/open-apis/bot/v2/hook/...'"
    Write-Host "   `$env:FEISHU_SECRET = 'your-secret-here'"
    Write-Host ""
    
    $response = Read-Host "继续运行部分流程 (仅爬取+去重+通知)? Continue with partial workflow? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "退出 / Exiting"
        exit 0
    }
    $PARTIAL_MODE = $true
} else {
    Write-Host "✅ OPENAI_API_KEY 已设置" -ForegroundColor Green
    $PARTIAL_MODE = $false
    
    # 设置默认值
    if ([string]::IsNullOrEmpty($env:LANGUAGE)) { $env:LANGUAGE = "Chinese" }
    if ([string]::IsNullOrEmpty($env:CATEGORIES)) { $env:CATEGORIES = "cs.CV, cs.CL" }
    if ([string]::IsNullOrEmpty($env:MODEL_NAME)) { $env:MODEL_NAME = "gpt-4o-mini" }
    if ([string]::IsNullOrEmpty($env:OPENAI_BASE_URL)) { $env:OPENAI_BASE_URL = "https://api.openai.com/v1" }
    
    Write-Host "🔧 当前配置 / Current configuration:" -ForegroundColor Green
    Write-Host "   LANGUAGE: $($env:LANGUAGE)"
    Write-Host "   CATEGORIES: $($env:CATEGORIES)"
    Write-Host "   MODEL_NAME: $($env:MODEL_NAME)"
    Write-Host "   OPENAI_BASE_URL: $($env:OPENAI_BASE_URL)"
}

# 获取当前日期
$today = Get-Date -Format "yyyy-MM-dd" -AsUTC

Write-Host "`n=== 开始工作流程 / Starting Workflow ===" -ForegroundColor Yellow
Write-Host "爬取日期: $today" -ForegroundColor Cyan

# 步骤 1: 爬取数据
Write-Host "`n步骤 1: 开始爬取 / Step 1: Starting crawl..." -ForegroundColor Green

$dataFile = "data/$today.jsonl"
if (Test-Path $dataFile) {
    Write-Host "🗑️  发现今日文件已存在，正在删除 / Found existing file, deleting..." -ForegroundColor Yellow
    Remove-Item $dataFile -Force
    Write-Host "✅ 文件已删除 / File deleted" -ForegroundColor Green
} else {
    Write-Host "📝 今日文件不存在，准备新建 / File doesn't exist, creating new one..." -ForegroundColor Cyan
}

try {
    Write-Host "正在爬取... / Crawling..." -ForegroundColor Cyan
    Push-Location daily_arxiv
    python -m scrapy crawl arxiv -o ../data/$today.jsonl
    Pop-Location
    
    if (-not (Test-Path $dataFile)) {
        Write-Host "❌ 爬取失败，未生成数据文件 / Crawling failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ 爬取完成 / Crawling completed" -ForegroundColor Green
} catch {
    Write-Host "❌ 爬取出错 / Crawling error: $_" -ForegroundColor Red
    exit 1
}

# 步骤 2: 去重检查
Write-Host "`n步骤 2: 执行去重检查 / Step 2: Deduplication check..." -ForegroundColor Green

try {
    Push-Location daily_arxiv
    python daily_arxiv/check_stats.py
    $dedupExitCode = $LASTEXITCODE
    Pop-Location
    
    switch ($dedupExitCode) {
        0 {
            Write-Host "✅ 去重检查通过 / Deduplication check passed" -ForegroundColor Green
        }
        1 {
            Write-Host "⏹️  无新内容，停止处理 / No new content, stopping" -ForegroundColor Yellow
            exit 1
        }
        2 {
            Write-Host "❌ 去重检查出错 / Deduplication check error" -ForegroundColor Red
            exit 2
        }
        default {
            Write-Host "❌ 未知错误 / Unknown error: $dedupExitCode" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ 去重检查失败 / Deduplication check failed: $_" -ForegroundColor Red
    exit 1
}

# 步骤 3: 发送飞书通知
if (-not [string]::IsNullOrEmpty($env:FEISHU_WEBHOOK_URL)) {
    Write-Host "`n步骤 3 (可选): 发送飞书通知 / Step 3 (Optional): Sending Feishu notification..." -ForegroundColor Green
    
    try {
        # 使用精选文章模式（默认）/ Use featured papers mode (default)
        python utils/feishu.py --data $dataFile --date $today --mode featured
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ 飞书通知已发送 / Feishu notification sent" -ForegroundColor Green
        } else {
            Write-Host "⚠️  飞书通知发送失败，但继续处理 / Feishu notification failed, continuing..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  飞书通知发送异常，但继续处理 / Feishu notification exception, continuing..." -ForegroundColor Yellow
    }
} else {
    Write-Host "`n步骤 3 (可选): ⏭️  未设置 FEISHU_WEBHOOK_URL，跳过飞书通知 / Skipping Feishu notification" -ForegroundColor Cyan
}

# 步骤 4: AI 增强处理
if ($PARTIAL_MODE -eq $false) {
    Write-Host "`n步骤 4: AI 增强处理 / Step 4: AI enhancement..." -ForegroundColor Green
    
    try {
        Push-Location ai
        python enhance.py --data ../data/$today.jsonl
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ AI 处理失败 / AI processing failed" -ForegroundColor Red
            exit 1
        }
        Pop-Location
        Write-Host "✅ AI 增强处理完成 / AI enhancement completed" -ForegroundColor Green
    } catch {
        Write-Host "❌ AI 处理异常 / AI processing exception: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n步骤 4: ⏭️  跳过 AI 处理 (部分模式) / Skipping AI processing (partial mode)" -ForegroundColor Cyan
}

# 步骤 5: Markdown 转换
Write-Host "`n步骤 5: Markdown 转换 / Step 5: Markdown conversion..." -ForegroundColor Green

$aiEnhancedFile = "data/${today}_AI_enhanced_$($env:LANGUAGE).jsonl"

if ($PARTIAL_MODE -eq $false -and (Test-Path $aiEnhancedFile)) {
    try {
        Push-Location to_md
        python convert.py --data ../data/$today"_AI_enhanced_$($env:LANGUAGE).jsonl"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Markdown 转换失败 / Markdown conversion failed" -ForegroundColor Red
            exit 1
        }
        Pop-Location
        Write-Host "✅ Markdown 转换完成 / Markdown conversion completed" -ForegroundColor Green
    } catch {
        Write-Host "❌ Markdown 转换异常 / Markdown conversion exception: $_" -ForegroundColor Red
        exit 1
    }
} elseif ($PARTIAL_MODE -eq $true) {
    Write-Host "⏭️  跳过 Markdown 转换 (部分模式) / Skipping Markdown conversion (partial mode)" -ForegroundColor Cyan
} else {
    Write-Host "❌ AI 增强文件不存在 / AI enhanced file not found: $aiEnhancedFile" -ForegroundColor Red
    exit 1
}

# 步骤 6: 更新文件列表
Write-Host "`n步骤 6: 更新文件列表 / Step 6: Updating file list..." -ForegroundColor Green

try {
    $files = Get-ChildItem "data/*.jsonl" -File | Select-Object -ExpandProperty Name | ForEach-Object { $_ -replace '^', '' }
    $files | Out-File -FilePath "assets/file-list.txt" -Encoding UTF8 -Force
    Write-Host "✅ 文件列表更新完成 / File list updated" -ForegroundColor Green
} catch {
    Write-Host "⚠️  文件列表更新失败 / File list update failed: $_" -ForegroundColor Yellow
}

# 完成总结
Write-Host "`n=== 工作流程完成 / Workflow Completed ===" -ForegroundColor Green

if ($PARTIAL_MODE -eq $false) {
    Write-Host "🎉 完整流程已完成 / Complete workflow finished:" -ForegroundColor Cyan
    Write-Host "   ✅ 数据爬取 / Data crawling"
    Write-Host "   ✅ 去重检查 / Smart duplicate check"
    Write-Host "   ✅ 飞书通知 / Feishu notification"
    Write-Host "   ✅ AI 增强处理 / AI enhancement"
    Write-Host "   ✅ Markdown 转换 / Markdown conversion"
    Write-Host "   ✅ 文件列表更新 / File list update"
} else {
    Write-Host "🔄 部分流程已完成 / Partial workflow finished:" -ForegroundColor Cyan
    Write-Host "   ✅ 数据爬取 / Data crawling"
    Write-Host "   ✅ 去重检查 / Smart duplicate check"
    Write-Host "   ✅ 飞书通知 / Feishu notification"
    Write-Host "   ⏭️  跳过 AI 增强和 Markdown 转换"
    Write-Host "   ✅ 文件列表更新 / File list update"
    Write-Host ""
    Write-Host "💡 提示: 设置 OPENAI_API_KEY 可启用完整功能" -ForegroundColor Yellow
}

Write-Host "`n✨ 脚本执行完成！/ Script execution completed!" -ForegroundColor Green
