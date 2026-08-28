# Mac 端安装 Hermes Agent(配硅基流动 DeepSeek-V4-Flash)

> 本方案由 Windows 侧侦察后编写(2026-08-24),供 Mac 端 agent 自执行。
> 执行环境:Mac `hymacbook-pro`(Intel x86_64, macOS 15.7.7),用户 `w`。
> 目标:装上 Hermes CLI 核心,模型走硅基流动 DeepSeek-V4-Flash,完成 Windows↔Mac 联动基础。

## 功能(本方案做完能得到什么)

- **Mac 上装有 Hermes CLI 核心**(agent 本体,`hermes-mac` 命令),模型走硅基流动 DeepSeek-V4-Flash,中文界面。
- **Windows ↔ Mac 联动通道**:Windows 侧 `ssh w@100.83.233.122 "hermes-mac <任务>"` 即可远程指挥 Mac 上的 Hermes 干活(出差/办公室时遥控家里 Mac)。
- 为后续升级留好底子:联动跑通后可再补 A2A 网关(端口 9900)、桌面 GUI、消息平台等。

## 装什么(安装内容清单)

| 组件 | 说明 | 类型 |
|---|---|---|
| **Hermes Agent CLI 核心**(v0.20.5) | agent 本体,`hermes` 命令;本方案装的就是它 | 要装的软件 |
| **uv 0.12.5** | Python 包管理器/环境工具,由安装流程管理 | 工具(已有) |
| **Python 3.13.13** | Hermes 运行环境(>=3.11,<3.14);用 Mac 已有 Homebrew 版 | 运行时(已有) |
| **cryptography 48.0.1** | Hermes 依赖的加密库;**关键降级点**见下 | 依赖 |
| 其余约 253 个依赖包 | pydantic、httpx 等,由 uv 自动按 uv.lock 拉齐 | 依赖 |

> **为什么降 cryptography**:Hermes 依赖 `cryptography==50.0.0`(CVE 修复钉死),但 50 没有 Intel Mac 预编译包,要源码编译 → 需要 Rust 工具链 + crates.io 下载,而本网络 crates.io 被 403 拦死、Mac 无 Rust。**48.0.1 有 `macosx_10_9_universal2` wheel(Intel 直接用,免编译免 Rust)**——本方案把它临时降到 48.0.1。这是 Intel Mac 上可用的最高 universal2 版本(49/50 无 universal2)。旧一版的实际风险对本机(工作/联动机)很低,trade-off 已记录;要 CVE 完整版时走文末第 6 节编译路线。

## 依赖(前置条件,装前需满足)

| 依赖 | 检查命令 | 本机现状 |
|---|---|---|
| uv | `ls ~/.hermes/bin/uv` | ✅ 0.12.5 已装 |
| Python 3.11~3.13 | `/usr/local/bin/python3.13 --version` | ✅ 3.13.13(Homebrew) |
| git(仅首次拉代码用) | `git --version` | ✅ 有 |
| 网络:清华 PyPI 镜像 | `curl -sI https://pypi.tuna.tsinghua.edu.cn/simple/` | ✅ 200 |
| 网络:官方 PyPI(兜底) | `curl -sI https://files.pythonhosted.org` | ⚠️ 慢但通 |
| 网络:crates.io(编译路线才用) | — | ❌ 403,别走 |
| 硅基流动 API 密钥 | `grep SILICONFLOW ~/.zshrc` | ✅ 已有(环境变量) |

## 在哪里下载(全部来源)

| 内容 | 下载地址 | 备注 |
|---|---|---|
| Hermes 源码 | **GitHub**:`https://github.com/NousResearch/hermes-agent.git` | Windows 侧已 success clone 到 `C:\Users\Administrator\AppData\Local\Temp\hermes-src`,并打包 scp 到 Mac `~/.hermes/hermes-agent`(已含 .git);GitHub 直连在 Windows 通、Mac 侧 clone 不稳定,所以用传过去的副本 |
| Python(3.13) | **Homebrew**(Mac 本机已有,无需下载) | `/usr/local/bin/python3.13` |
| uv | 安装脚本自带(已装 ~/.hermes/bin) | 版本 0.12.5 |
| 全部 Python 依赖(含 cryptography 48.0.1 wheel) | **清华 PyPI 镜像**:`https://pypi.tuna.tsinghua.edu.cn/simple`(主源) / 阿里云 `https://mirrors.aliyun.com/pypi/simple`(备份) / 官方 `https://pypi.org`(兜底) | uv sync 时经 `UV_INDEX_URL` 指定;cryptography 48.0.1 的 universal2 wheel 在清华镜像有、官方 PyPI 实测可下(慢~40s) |
| 硅基流动模型(运行时) | 硅基流动官方 API:`https://api.siliconflow.cn/v1` | 运行时调用,非安装下载 |

---

## 0. 已探明的环境事实(不要重复侦察)

| 项目 | 状态 |
|---|---|
| 代码已解压 | `~/.hermes/hermes-agent`(含 .git,Windows clone 后 scp 过去) |
| uv | `~/.hermes/bin/uv`(0.12.5) |
| Python | 系统 3.9.6 太旧;**用 `/usr/local/bin/python3.13`(3.13.13)** |
| 唯一卡点 | `cryptography==50.0.0` 无 Intel wheel → 源码编译 → Rust+crates.io → 403 | 
| 出路 | **降 48.0.1**(universal2 wheel,清华镜像有,免编译) |
| 网络关键事实 | ① 清华 PyPI 通(200) ② 官方 pypi.org JSON 通 ③ files.pythonhosted 慢但通 ④ GitHub 直连 Windows 通(Mac 不稳定) ⑤ **static.crates.io / crates.io api = 403(别走编译路)** ⑥ index.crates.io 200 ⑦ static.rust-lang.org 200(可装 Rust 但 crate 下载被拦) ⑧ Mac 的 Clash 代理(mixed-port 7897)转发 GitHub 握手失败,别依赖 |
| 前次失败记录 | uv sync 两次卡 `Building cryptography==50.0.0`;`uv sync --override` 参数本版本不支持 |

## 1. 降 cryptography(核心改动)

```bash
cd ~/.hermes/hermes-agent
cp pyproject.toml pyproject.toml.bak-crypto50
# 两处 ==50.0.0 → ==48.0.1:① [project] dependencies ② [tool.uv] override-dependencies
sed -i '' 's/cryptography==50\.0\.0/cryptography==48.0.1/g' pyproject.toml
grep -n "cryptography" pyproject.toml   # 确认两处都变成 48.0.1
```
[tool.uv] 里 `cryptography<49` 的抗住逻辑(48<49)依然成立,不冲突。

## 2. 安装依赖(清华镜像,后台+日志)

```bash
cd ~/.hermes/hermes-agent
export UV_PYTHON=/usr/local/bin/python3.13
export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
pkill -f "uv sync" 2>/dev/null; sleep 1
nohup ~/.hermes/bin/uv sync > ~/.hermes/uv-sync-final.log 2>&1 &
echo "PID $! — 日志 ~/.hermes/uv-sync-final.log"
```
- 下载慢正常(网络),**耐心等**,别因"看起来没动"就杀。
- 日志出现 `Resolved N packages` → 逐步 `Downloaded/Installed`。
- 不要走 `--override` CLI 参数(本版本报 unexpected argument)。

### 2.1 若仍尝试 Building cryptography(48.0.1 wheel 没被命中)
```bash
curl -s "https://pypi.tuna.tsinghua.edu.cn/simple/cryptography/" | grep -o "cryptography-48\.0\.1-[^"]*universal2\.whl" | head -1
# 有 → 说明 env 没生效,重查第 2 步的 export
# 仍不行 → 手动下载 wheel 到本地目录,用 UV_FIND_LINKS 指向:
mkdir -p ~/.hermes/wheels
curl -sL -o ~/.hermes/wheels/c48.whl "https://files.pythonhosted.org/packages/1b/bc/ee4137cbbe105652c0ee4252792b78fc8e7afa4b8e61d9d5dc05a7f45731/cryptography-48.0.1-cp311-abi3-macosx_10_9_universal2.whl"
# (官方直链实测可下;失效则用 pypi.org/pypi/cryptography/48.0.1/json 查最新)
export UV_FIND_LINKS="$HOME/.hermes/wheels"
nohup ~/.hermes/bin/uv sync > ~/.hermes/uv-sync-final.log 2>&1 &
```
注:wheel 文件名 cp311-abi3 是 abi3 通用(兼容 3.13)。

## 3. 配置 Hermes(硅基流动 + DeepSeek-V4-Flash)

```bash
~/.hermes/hermes-agent/.venv/bin/hermes --version   # 先验证装好
mkdir -p ~/.hermes
cat > ~/.hermes/config.yaml <<'EOF'
model:
  default: deepseek-ai/DeepSeek-V4-Flash
  provider: siliconflow
  base_url: https://api.siliconflow.cn/v1
providers:
  siliconflow:
    base_url: https://api.siliconflow.cn/v1
    key_env: SILICONFLOW_API_KEY
display:
  language: zh
terminal:
  cwd: ~
EOF
```
- key 读环境变量;`~/.zshrc` 已有 `SILICONFLOW_API_KEY`,交互会话自动带上。
- launchd/crontab 场景需在该 shell `source ~/.zshrc`。

## 4. 验证(三项)

```bash
~/.hermes/hermes-agent/.venv/bin/hermes --version
~/.hermes/hermes-agent/.venv/bin/hermes chat -q "回复四个字:通道正常" --model deepseek-ai/DeepSeek-V4-Flash
ln -sf ~/.hermes/hermes-agent/.venv/bin/hermes /usr/local/bin/hermes-mac
```

## 5. 兜底 / 备选

| 情形 | 处理 |
|---|---|
| uv sync 网络中断 | 多次重试(抖动,可续传);别删 venv 重来 |
| 清华缺某 wheel | `UV_INDEX_URL` 换阿里云 `https://mirrors.aliyun.com/pypi/simple` |
| 必须 cryptography 50(CVE 完整) | 编译路线:Rust 可装(static.rust-lang.org 200),但 cargo 拉 crate 403 → 配 rsproxy.cn 稀疏索引(`sparse+https://rsproxy.cn/index/`,index 200)后可编——成本高,默认不走 |
| chat 报模型错误 | 查 `SILICONFLOW_API_KEY` 在会话环境否;`curl https://api.siliconflow.cn/v1/models` 带 key 验证 |

## 6. 完成判定

- [ ] `hermes --version` 输出版本号
- [ ] `hermes chat -q "回复四个字:通道正常"` 返回"通道正常"
- [ ] `/usr/local/bin/hermes-mac` 可执行(若做了符号链接)
- [ ] Windows 侧 `ssh w@100.83.233.122 "hermes-mac --version"` 能通(联动通道)

## 7. 后续可选项(本方案不做)

| 项目 | 说明 |
|---|---|
| A2A 网关 | `gateway.platforms.a2a.enabled=true`,端口 9900,让 Mac 的 Hermes 可被协议级调用 |
| 桌面 GUI | 核心装好后 `hermes desktop` 起图形界面(联动机不用,可选) |
| 消息平台 | Telegram/Discord 等网关(需要时再配) |