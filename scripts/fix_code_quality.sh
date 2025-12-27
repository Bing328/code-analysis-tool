#!/bin/bash

echo "🔧 开始修复代码质量问题..."
echo "=" * 60

# 1. 删除未使用的导入和变量
echo "1. 清理未使用的导入和变量..."
autoflake --in-place --remove-unused-variables --remove-all-unused-imports .

# 2. 格式化代码
echo "2. 使用black格式化代码..."
black . --line-length=127

# 3. 排序imports
echo "3. 排序imports..."
isort .

# 4. 检查结果
echo -e "\n4. 检查修复结果..."
flake8 . --count

echo -e "\n" "=" * 60
echo "✅ 代码质量修复完成！"
