#!/bin/bash
echo "🧹 项目清理工具"
echo "=============="

# 1. 删除Python缓存
echo "清理Python缓存..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null

# 2. 删除生成的报告
echo "删除生成的HTML报告..."
rm -f Code_Audit_Report_*.html

# 3. 删除构建文件
echo "删除构建文件..."
rm -rf build/ dist/ *.spec

# 4. 显示清理结果
echo ""
echo "清理完成！剩余文件："
ls -la
