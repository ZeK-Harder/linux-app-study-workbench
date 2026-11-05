# 进度台账

> 每周更新。只写「能演示的」和「没答上的」。规则见 `AGENTS.md`；进度条数据源是 `项目进度.md`。

## 现在

- 更新：2026-11-05（**P0 亲跑验收完成 → 环境与工具箱打通，下一站 P1 devlogstat**）
- 阶段：试跑第 1 周（2026.11）· 起步
- 当前项目：**P0 环境与工具箱（已完成）** → 下一站 **P1 devlogstat**
- 本周三件事（第 1 周）：
  1. ✅ WSL2 环境验收：亲手跑 `wsl -d Ubuntu-22.04` + `gcc/make/gdb/git`（版本见下表）
  2. ✅ `练习/hello-linux`：`make clean && make` → `./hello 100` → `gdb` 断点 + `bt` 四层栈
  3. ✅ git 首次提交 + Makefile + 《理解清单》模板各就位（概念卡 3 张已记）
- 进度条：6 段 / 35 条小步，已完成 6 条（**P0 全部**，亲手验收：见下「P0 验收记录」）
- 下一个里程碑：**第 4 周末：P1 devlogstat 完成 + 理解清单 8/10**（试跑门判据）
- 投递倒计时：**2026.12 中旬**起投 2027 寒假日常实习（练手，目标面 3–5 场，不设 offer 目标）
- 决策门：2027.1 寒假前，4–6 周试跑结束 → 继续 Linux 应用 V1.3 或回设备软件 V1.3（C# 成果保留）

## 环境实测（2026-11-05）

| 项 | 命令 | 结果 |
|---|---|---|
| WSL | `wsl -l -v` | Ubuntu-22.04 · WSL2 · 状态 Stopped（用时启动） |
| 内核 | `uname -a` | Linux 6.18.33.2-microsoft-standard-WSL2 x86_64 |
| gcc | `gcc --version` | 11.4.0（Ubuntu 11.4.0-1ubuntu1~22.04.3） |
| gdb | `gdb --version` | 12.1 |
| make | `make --version` | 4.3 |
| git（WSL） | `git --version` | 2.34.1 |
| git（Windows） | `git --version` | 2.55.0.windows.2 |
| python3 | `python3 --version` | 3.10.12 |
| g++ | `g++ --version` | **未安装**（P2.5 前装；`sudo apt install g++`） |
| VS Code | `code --version` | 1.144.0 |

> 搭建记录（2026-11-05，DSH 完成）：`make` 零警告、`./hello 100` 输出 `sum(1..100) = 5050`、`gdb -batch -ex 'break main' -ex run -ex bt` 断点命中 `main at hello.c:13`。**当天已亲手跑完验收，见下节。**

## P0 验收记录（2026-11-05，亲手跑）

> 起点：`cd /mnt/c/Users/24552/Documents/Linux应用/练习/hello-linux`（WSL 里）

| 项 | 命令 | 结果 |
|---|---|---|
| make 构建 | `make clean && make` | 零 warning；`./hello 100` → `sum(1..100) = 5050` |
| 参数/退出码 | `./hello` / `./hello 0; echo $?` | 默认 10 → `sum(1..10) = 55`；0 → usage 到 stderr、`$?`=1 |
| gdb 断点 + 栈 | `set backtrace past-main on` → `break main` → `run 100` → `bt` | `#0 main` → `#1 __libc_start_call_main` → `#2 __libc_start_main_impl` → `#3 _start` |
| `-g` 实物对比 | `readelf -S hello \| grep -c '\.debug'` vs 不带 `-g` | 6 : 0 |
| execve 证据 | `strace -f -e trace=execve ./hello 100` | `execve("./hello", ["./hello","100"], ...)` |
| 缓冲证据 | `strace -e trace=write`（终端 vs 重定向） | 终端 2 次 write（14/19 字节）；文件 1 次 write（33 字节） |

> **没答上的（已补讲，明天不看代码口述复述一遍）**
> 1. 编译四阶段：预处理 → 编译 → 汇编 → 链接（产物 `.i/.s/.o/可执行`）
> 2. `_start` 不在 `hello.o` 里：链接时从 `Scrt1.o` 并入；ELF 入口地址就是 `_start`（`0x10c0`）
> 3. 符号表（函数名→地址，`strip` 删）vs DWARF（行号/变量，只有 `-g` 有）
> 4. `printf` → libc 用户态缓冲 → `write(2)`；终端行缓冲、文件全缓冲（看着「没输出」是还没交内核）

> **盲讲首试（2026-11-05）**：段 1 编译链 ✅（顺序与产物都记得）；段 2 启动链 ⚠️（`execve` 位置说反，漏 `__libc_start_main` 一环）；段 3 输出/返回 ⚠️（缓冲→`write` ✅、返回值链 ✅；`write` 之后怎么显示到屏幕 ❌）。
> **判定：未达 3 分钟盲讲标准**，第 1 周清单 §5 不勾。明天补 2 个点（execve 的正确位置 / `write` 之后到屏幕）后重讲。

## 本周三件事（2026.11 第 1 周）

1. ✅ hello-linux：`make` + `./hello` + `gdb` 断点（第 1 周主线）
2. ✅ 理解清单模板：建好并在 P0 填一页（hello 从源码到运行）
3. ✅ git：首次提交 + 提交规范确认（conventional commits 已用；二进制用 `.gitignore` 挡）

## 环境坑（下次别重踩）

- **gdb 12.1 默认 `backtrace past-main = off`**：在 `main` 里 `bt` 只显示 `#0`；要看 libc 帧必须先 `set backtrace past-main on`。
- **终端一次粘多行命令**（`gcc`、`readelf`、`echo` 混在一起）时，回显全挤在前面，分不清哪段输出属于哪条 → 一行一行敲，或每条前加 `echo "--- 标签 ---"`。
- `.gitignore` 只写了 `hello` 这个文件名；做对比实验的 `hello_nog` 之类新二进制不会被忽略 → 实验产物放 `/tmp`，或补进 `.gitignore`。

## 换版记录

### 2026-11-05 · P0 收尾（亲手验收）

- P0 六步全部打勾：WSL2/gcc/gdb 之前已就位，今天亲手跑通 `make` 构建、`./hello` 参数与退出码、gdb 断点 + 四层 `bt`。
- 额外实证（写进验收记录）：`-g` 有无的 `.debug_*` 段数 6:0、`strace` 看到 `execve` 的 argv、终端 vs 文件两种缓冲的 `write` 差异。
- 概念卡 3 张（ELF / 链接 / gdb 断点）已记；建议 P1 前补两张：「符号表 vs DWARF」「printf 缓冲」。**明天先做 3 分钟不看代码口述（第 1 周清单 §5 最后一项）**。


### 2026-11-05 · 补强（按面试竞争力反馈）

- P2 加「埋 bug 定位 1 次（死锁 / 内存泄漏）」；P3 加「CMake 升为必须 + 阶梯压测数据（10/50/100）+ 埋 bug 定位（SIGPIPE / 悬垂指针 / ET 漏读）」；P4 加「端到端联调（serialmon → devhub 上报核对）」。
- 项目进度：31 条 → 35 条小步；计划 V1.3 与规格书 V1.0 原地更新（不新建版本文件）。

### 2026-11-05 · 重启日：记忆与进度条插件接上新计划

- 全局记忆 `~/.dsh/AGENTS.md` 的主线从「设备软件 V1.3」切到「Linux 应用主线」，设备软件降为暂停/备选（记忆与工作区保留不删）；代码环境改为 WSL2 Ubuntu 22.04。
- 进度条插件 `@local/dsh-project-progress` 的解析器改为同时认 `##`/`###` 大步骤与 `- [ ]`/`- ✅` 两种小步方言，并把只做分组的 `## 试跑段` 丢弃 —— 现在进度条显示的是本工作区的 6 个项目 / 35 条小步（当前 P0）。
- 工作区记忆小错修正：PROGRESS.md 的「40 条小步」→ 31；README 的「重开版 V1.2」→ V1.3（与桌面上 docx 文件名一致）。

### 2026-11-05 · 新建工作区（Linux 应用 V1.3 试跑）

- 从 `C:\Users\24552\Documents\设备软件`（C# 路线的 V1.3）单独迁出，新建 `Linux应用` 工作区；设备软件 V1.3 暂停不删。
- 执行计划：`嵌入式Linux应用-学习计划-重开版V1.3.docx` + `嵌入式Linux应用-项目规格书-V1.0.docx`（弄懂优先 + 性价比裁剪版，约 450h；P1–P4 做到懂，P5/P6 已裁；每项目功能/验收见规格书）。
- 试跑门：4–6 周后按「P1 完成 + 理解清单 8/10 + 每周 12h」判断是否正式切换。
