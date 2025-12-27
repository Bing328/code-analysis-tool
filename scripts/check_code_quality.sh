#!/bin/bash

echo "🔍 运行代码质量检查..."
echo "=" * 60

# 1. 检查flake8
echo "1. 运行flake8代码检查..."
flake8 . --count

# 2. 检查black格式
echo -e "\n2. 检查black代码格式..."
black --check . --diff

# 3. 检查import排序
echo -e "\n3. 检查import排序..."
isort --check-only .

# 4. 清理未使用的导入
echo -e "\n4. 清理未使用的导入..."
autoflake --check .

echo -e "\n" "=" * 60
echo "✅ 代码质量检查完成！"
