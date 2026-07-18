# Clash Verge 配置

## 问题现象
- 断内网（局域网 192.168.x.x 无法访问）
- 劫持端口
- Google 等外网打不开

## 最终解决方案

### 1. 关闭 TUN 模式
在 Clash Verge GUI 中关闭 TUN 模式，或检查 `clash-verge.yaml`：
```yaml
tun:
  enable: false
```

### 2. 开启系统代理
```bash
sudo networksetup -setwebproxy Wi-Fi 127.0.0.1 7897
sudo networksetup -setsecurewebproxy Wi-Fi 127.0.0.1 7897
sudo networksetup -setwebproxystate Wi-Fi on
sudo networksetup -setsecurewebproxystate Wi-Fi on
```

### 3. 内网直连规则（防断网）
在 Merge.yaml / clash-verge.yaml 的 prepend-rules 中添加：
```yaml
prepend-rules:
  - IP-CIDR,192.168.0.0/16,DIRECT
  - IP-CIDR,10.0.0.0/8,DIRECT
  - IP-CIDR,172.16.0.0/12,DIRECT
  - DOMAIN-SUFFIX,local,DIRECT
```

### 4. DNS fake-ip-filter 添加 .local
```yaml
dns:
  fake-ip-filter:
    - '+.local'
```

## 关键文件路径
- 配置文件: `~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml`
- 合并模板: `.../profiles/Merge.yaml`
- 日志: `.../logs/latest.log`
- Unix Socket: `/tmp/verge/verge-mihomo.sock`

## 常用命令
```bash
# 检查代理状态
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/proxies | python3 -m json.tool

# 检查当前模式
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/configs

# 测试代理是否通
curl -s -o /dev/null -w "%{http_code}" -x http://127.0.0.1:7897 https://www.google.com

# 查看系统代理
networksetup -getwebproxy Wi-Fi
```
