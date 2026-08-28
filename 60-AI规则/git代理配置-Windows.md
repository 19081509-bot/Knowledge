# Windows git 永久走 Clash 代理(7897)配置说明

> 2026-08-28 东哥在野外/多地网络下确认:Windows 直连 GitHub 不稳(schannel 断),需走 Clash Verge 代理(7897)才稳。
> 本文件记录配置命令,执行:`git config --global http.proxy http://127.0.0.1:7897` 与 https 同。
> 注意:东哥在野外走不同 Clash 节点,规则不通转全局或直连按需——代理端口可能变,若 7897 不通先 `git config --global --unset http.proxy` 回直连。

## 配置
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897

## 撤销(直连时)
git config --global --unset http.proxy
git config --global --unset https.proxy
