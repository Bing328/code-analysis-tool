#!/usr/bin/env bash
set -euo pipefail

# ===== 配置参数 =====
# 监控组件配置
GRAFANA_ADMIN_PASSWORD="${GRAFANA_ADMIN_PASSWORD:-SecurePass123!}"
NODE_EXPORTER_VERSION="${NODE_EXPORTER_VERSION:-1.8.2}"

# 远程部署配置
IPS_FILE="${IPS_FILE:-ips.txt}"
SSH_USER="${SSH_USER:-root}"        # 默认SSH用户，可修改为普通用户 (如 ubuntu)
SSH_PORT="${SSH_PORT:-22}"          # SSH端口

# ===== 0) 运行环境检查 =====
if [[ $EUID -ne 0 ]]; then
   echo "❌ 本脚本需要 root 权限运行 (用于配置本地Docker和防火墙)" 
   echo "请使用: sudo $0"
   exit 1
fi

check_dependencies() {
    local deps=("docker" "curl" "ssh" "scp" "jq")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing+=("$dep")
        fi
    done
    
    # 检查 docker compose (兼容 v1 和 v2)
    if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
        missing+=("docker compose")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "❌ 缺少必要依赖: ${missing[*]}"
        echo "请先安装这些工具: apt-get install docker.io curl openssh-client jq"
        exit 1
    fi
}
check_dependencies

# ===== 1) 准备目录与备份 =====
BASE_DIR="monitor-stack"

if [[ -d "$BASE_DIR" ]]; then
    BACKUP_NAME="${BASE_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "📦 检测到旧配置，备份至: $BACKUP_NAME"
    cp -r "$BASE_DIR" "$BACKUP_NAME"
fi

echo "📁 创建目录结构..."
mkdir -p "$BASE_DIR"/{prometheus/{rules,targets},alertmanager,grafana/provisioning/{datasources,dashboards}}

# !!! 关键改进：修复 Prometheus 容器(UID 65534)的写入权限问题 !!!
# Prometheus 和 Alertmanager 容器默认以 nobody 用户运行
echo "🔒 修正数据目录权限..."
chown -R 65534:65534 "$BASE_DIR/prometheus"
chown -R 65534:65534 "$BASE_DIR/alertmanager"

cd "$BASE_DIR"

# ===== 2) 生成 docker-compose.yml =====
cat > docker-compose.yml <<EOF
version: "3.8"
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    user: "65534:65534"
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus:/etc/prometheus
      - prometheus-data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.enable-admin-api"
      - "--web.enable-lifecycle"
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    user: "65534:65534"
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager:/etc/alertmanager
      - alertmanager-data:/alertmanager
    command:
      - "--config.file=/etc/alertmanager/alertmanager.yml"
      - "--storage.path=/alertmanager"
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:9093/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    user: "472:472"
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  prometheus-data:
  alertmanager-data:
  grafana-data:
EOF

# ===== 3) 生成配置文件 =====
# Prometheus 配置
cat > prometheus/prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'node_exporter'
    file_sd_configs:
      - files:
          - /etc/prometheus/targets/node_exporter.json
        refresh_interval: 1m
EOF

# 告警规则
cat > prometheus/rules/node_rules.yml <<EOF
groups:
- name: node.rules
  rules:
  - alert: HostHighCPU
    expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage on {{ \$labels.instance }}"
  
  - alert: HostDown
    expr: up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Host {{ \$labels.instance }} is down"
EOF

# Alertmanager 配置
cat > alertmanager/alertmanager.yml <<EOF
global:
  resolve_timeout: 5m
route:
  receiver: 'default'
receivers:
- name: 'default'
EOF

# Grafana Datasource (自动配置)
cat > grafana/provisioning/datasources/datasource.yml <<EOF
apiVersion: 1
datasources:
- name: Prometheus
  type: prometheus
  access: proxy
  url: http://prometheus:9090
  isDefault: true
EOF

# ===== 4) 启动监控栈 =====
configure_firewall() {
    echo "🔥 配置防火墙规则 (3000, 9090, 9093)..."
    if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
        ufw allow 3000/tcp comment 'Grafana'
        ufw allow 9090/tcp comment 'Prometheus'
        ufw allow 9093/tcp comment 'Alertmanager'
    elif command -v firewall-cmd >/dev/null 2>&1 && systemctl is-active --quiet firewalld; then
        firewall-cmd --permanent --add-port=3000/tcp
        firewall-cmd --permanent --add-port=9090/tcp
        firewall-cmd --permanent --add-port=9093/tcp
        firewall-cmd --reload
    fi
}
configure_firewall

echo "🐳 启动容器..."
docker compose up -d

echo "⏳ 等待服务就绪..."
sleep 15

# ===== 5) 目标管理 (IP列表) =====
if [[ ! -f "../${IPS_FILE}" ]]; then
    cat > "../${IPS_FILE}" <<EOF
# 格式: IP地址 [可选注释]
# 192.168.1.100
# 192.168.1.101
EOF
    echo "ℹ️  已创建示例IP文件: ../${IPS_FILE}"
    IPS_FILE="../${IPS_FILE}"
else
    IPS_FILE="../${IPS_FILE}"
fi

generate_targets() {
    local target_file="prometheus/targets/node_exporter.json"
    local json_content="["
    local first=1
    
    while IFS= read -r line; do
        # 去除注释和空行
        ip=$(echo "$line" | awk '{print $1}')
        [[ -z "$ip" ]] && continue
        [[ "$ip" =~ ^# ]] && continue
        
        if [[ $first -eq 0 ]]; then json_content+=","; fi
        json_content+="{\"targets\": [\"${ip}:9100\"], \"labels\": {\"instance\": \"${ip}\"}}"
        first=0
    done < "$IPS_FILE"
    
    json_content+="]"
    echo "$json_content" > "$target_file"
    echo "✅ 更新监控目标列表，Prometheus将自动重载"
}
generate_targets

# ===== 6) Node Exporter 远程安装逻辑 =====

# 生成安装脚本 (不依赖 sed，直接生成)
generate_remote_installer() {
    cat > /tmp/install_ne.sh <<EOF
#!/bin/bash
set -e

# 自动提升权限
if [ "\$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

VERSION="${NODE_EXPORTER_VERSION}"
ARCH=\$(uname -m)

# 架构映射
case "\$ARCH" in
    x86_64) FILE="node_exporter-\${VERSION}.linux-amd64.tar.gz" ;;
    aarch64) FILE="node_exporter-\${VERSION}.linux-arm64.tar.gz" ;;
    *) echo "不支持的架构: \$ARCH"; exit 1 ;;
esac

echo ">>> 下载 Node Exporter \$VERSION (\$ARCH)..."
cd /tmp
if ! curl -fsSL -O "https://github.com/prometheus/node_exporter/releases/download/v\${VERSION}/\${FILE}"; then
    echo "下载失败"
    exit 1
fi

tar -xzf "\${FILE}"
cd "node_exporter-\${VERSION}.linux-*"

echo ">>> 安装二进制文件..."
\$SUDO mv node_exporter /usr/local/bin/
\$SUDO chown root:root /usr/local/bin/node_exporter

echo ">>> 配置 Systemd 服务..."
cat <<SERVICE | \$SUDO tee /etc/systemd/system/node_exporter.service > /dev/null
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=nobody
ExecStart=/usr/local/bin/node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

echo ">>> 启动服务..."
\$SUDO systemctl daemon-reload
\$SUDO systemctl enable --now node_exporter

# 防火墙 (尽力而为)
if command -v ufw >/dev/null; then
    \$SUDO ufw allow 9100/tcp >/dev/null 2>&1 || true
elif command -v firewall-cmd >/dev/null; then
    \$SUDO firewall-cmd --permanent --add-port=9100/tcp >/dev/null 2>&1 || true
    \$SUDO firewall-cmd --reload >/dev/null 2>&1 || true
fi

echo ">>> 安装完成"
EOF
}

install_remote() {
    generate_remote_installer
    
    echo "🚀 开始远程安装 Node Exporter (SSH用户: $SSH_USER)..."
    
    while IFS= read -r line; do
        ip=$(echo "$line" | awk '{print $1}')
        [[ -z "$ip" ]] && continue
        [[ "$ip" =~ ^# ]] && continue
        
        echo -n "📡 节点 $ip: "
        
        # 1. 检测是否已安装
        if ssh -p "$SSH_PORT" -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$SSH_USER@$ip" "systemctl is-active node_exporter" &>/dev/null; then
            echo "✅ 已运行 (跳过)"
            continue
        fi
        
        # 2. 上传脚本
        if ! scp -P "$SSH_PORT" -o StrictHostKeyChecking=no /tmp/install_ne.sh "$SSH_USER@$ip:/tmp/" &>/dev/null; then
            echo "❌ 上传失败 (检查SSH连接/权限)"
            continue
        fi
        
        # 3. 执行安装 (这里不需要sudo，脚本内部会处理sudo)
        if ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no -t "$SSH_USER@$ip" "bash /tmp/install_ne.sh" &>/dev/null; then
            echo "✅ 安装成功"
        else
            echo "❌ 安装/启动失败 (请尝试手动执行查看报错)"
        fi
        
    done < "$IPS_FILE"
}

# 询问是否部署Agent
echo ""
read -p "是否向 ips.txt 中的节点安装 Node Exporter? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    install_remote
fi

# ===== 7) 结束信息 =====
# 改进的 IP 获取逻辑: 优先获取路由到外网的接口 IP，避开 Docker 网桥
HOST_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '{print $7; exit}') || HOST_IP=$(hostname -I | awk '{print $1}')

cat <<EOF

🎉🎉🎉 部署完成! 🎉🎉🎉

📊 访问面板:
   Grafana:      http://${HOST_IP}:3000  (账号: admin / 密码: ${GRAFANA_ADMIN_PASSWORD})
   Prometheus:   http://${HOST_IP}:9090
   Alertmanager: http://${HOST_IP}:9093

📝 后续操作:
   1. 登录 Grafana
   2. 左侧菜单 -> Dashboards -> New -> Import
   3. 输入 ID: 1860 (Node Exporter Full) -> Load
   4. Select a Prometheus data source -> 选择 "Prometheus" -> Import

🔧 运维命令:
   cd ${BASE_DIR}
   查看状态: docker compose ps
   查看日志: docker compose logs -f
   停止服务: docker compose down

EOF
