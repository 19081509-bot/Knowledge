# SSH 密钥配置（Windows 免密登录）

## 场景
Mac（192.168.2.67）→ Windows（192.168.2.166）免密 SSH

## 步骤

### 1. Windows 端（管理员 PowerShell）

```powershell
# 创建 .ssh 目录
mkdir $env:USERPROFILE\.ssh -Force

# 添加公钥
Add-Content $env:USERPROFILE\.ssh\authorized_keys "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILwpjTpFPEzsSfb68Z5Ys13D42IFaks5jnGqqw5oR8Ym w@192.168.2.67"
```

### 2. 开启 PubkeyAuthentication

```powershell
# 编辑 sshd_config
$config = Get-Content C:\ProgramData\ssh\sshd_config
$config = $config -replace '#PubkeyAuthentication yes', 'PubkeyAuthentication yes'
$config | Set-Content C:\ProgramData\ssh\sshd_config
Restart-Service sshd
```

### 3. 重要：因 administrator 属于 Administrators 组

Windows SSH 会读 `C:\ProgramData\ssh\administrators_authorized_keys` 而不是 `~/.ssh/authorized_keys`

```powershell
Add-Content C:\ProgramData\ssh\administrators_authorized_keys "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILwpjTpFPEzsSfb68Z5Ys13D42IFaks5jnGqqw5oR8Ym w@192.168.2.67"
```

### 4. 测试连接

```bash
ssh -o StrictHostKeyChecking=no administrator@192.168.2.166 "echo SSH_KEY_OK"
```

## 常用操作

```bash
# SSH 执行单条命令
sshpass -p '密码' ssh administrator@192.168.2.166 "命令"

# SSH 执行 PowerShell
sshpass -p '密码' ssh administrator@192.168.2.166 "powershell -Command \"命令\""
```
