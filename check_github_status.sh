#!/bin/bash
echo "🔍 检查GitHub项目状态"
echo "====================="

# 显示项目信息
echo "1. 本地项目信息："
echo "   大小：" $(du -sh . | cut -f1)
echo "   文件数：" $(find . -type f | wc -l)
echo "   提交数：" $(git log --oneline | wc -l)

echo ""
echo "2. Git状态："
git status --short

echo ""
echo "3. 远程仓库："
git remote -v

echo ""
echo "4. 最后5次提交："
git log --oneline -5

echo ""
echo "🎯 下一步："
echo "1. 访问 https://github.com/Bing328/code-analysis-tool 查看项目"
echo "2. 查看Actions：https://github.com/Bing328/code-analysis-tool/actions"
echo "3. 检查README.md是否显示正确"
echo "4. 如果有需要，可以配置GitHub Pages或设置项目描述"
