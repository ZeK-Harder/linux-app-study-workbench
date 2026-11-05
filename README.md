# Linux应用 · 学习工作区

2026-11-05 新建，用于执行《嵌入式 Linux 应用开发 · 学习计划（重开版 V1.2）》。

- 权威计划：`C:\Users\24552\Desktop\嵌入式Linux应用-学习计划-重开版V1.2.docx`
- 当前状态：`PROGRESS.md`（只看这个）
- 进度条：`项目进度.md`
- 第一个项目：`项目/P0_环境与工具/`
- 练习脚手架：`练习/hello-linux/`

## 环境（2026-11-05 实测）

| 项 | 结果 |
|---|---|
| WSL | Ubuntu-22.04（WSL2；停止时用 `wsl -d Ubuntu-22.04` 启动） |
| gcc | 11.4.0 |
| gdb | 12.1 |
| make | 4.3 |
| git | 2.34.1（WSL 内）/ 2.55.0（Windows） |
| g++ | **未安装**（P2.5 前装：`sudo apt install g++`；P0–P2 只用 C） |
| python3 | 3.10.12 |
| VS Code | 1.144.0（Windows 端，Remote-WSL 可用） |

## 第一次跑通

```bash
# Windows 终端
wsl -d Ubuntu-22.04

# WSL 里
cd /mnt/c/Users/24552/Documents/Linux应用/练习/hello-linux
make
./hello
gdb ./hello        # 进去后：break main → run → bt → quit
```

## Git

- 本地仓库已 `git init` 并提交初始版本；远程仓库待建（建议名 `linux-app-study-workbench`）。
- 提交规范：`<type>: <一句话>`（feat / fix / docs / chore / test）。
- 当前 git 身份：ZeK-Harder / 2455219615@qq.com（全局配置）。

## 目录约定

- `练习/`：环境脚手架，不要求完美。
- `项目/`：正式项目，每个目录一个仓库级工程（P0 之后可各自 git init 或共用本仓库大目录）。
- `验收/`：每个新项目复制一份模板到项目目录。
- `台账/`：概念卡、面试追问库、踩坑记录。
- `复盘/`：每月复盘。
