#!/bin/bash
echo "🚀 推送代码到GitHub"

# 检查远程地址
echo "当前远程地址："
git remote -v

echo ""
echo "提示：如果推送失败，可能需要使用GitHub PAT"
echo "获取PAT：https://github.com/settings/tokens"
echo ""
echo "正在推送..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
    echo "🌐 访问：https://github.com/Bing328/code-analysis-tool"
else
    echo "❌ 推送失败，尝试备用方案..."
    echo ""
    echo "请运行以下命令使用PAT推送："
    echo "  git push https://bing328:你的PAT@github.com/Bing328/code-analysis-tool.git main"
fi
