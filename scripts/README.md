# 脚本目录说明

本目录包含项目中的所有 Shell 脚本。

## 脚本列表

### 代码质量相关
- `check_code_quality.sh` - 检查代码质量
- `fix_code_quality.sh` - 修复代码质量问题

### 部署和构建相关
- `check_github_status.sh` - 检查 GitHub 状态
- `clean_project.sh` - 清理项目
- `push_github.sh` - 推送代码到 GitHub
- `setup_monitor_v2.sh` - 设置监控
- `test_builds.sh` - 测试构建

### 开发工具
- 其他辅助脚本

## 使用方法

### 从项目根目录运行脚本
```bash
# 直接运行脚本
./scripts/check_code_quality.sh

# 或者进入 scripts 目录运行
cd scripts
./check_code_quality.sh

设置 PATH 环境变量（可选）

如果你经常使用这些脚本，可以将 scripts 目录添加到 PATH：
export PATH="$PATH:$(pwd)/scripts"

注意事项

注意事项
所有脚本都有执行权限

脚本中使用相对路径时，请确保从项目根目录运行

添加新脚本时，请确保添加执行权限：chmod +x script_name.sh
