# devlogstat · 设备日志统计 CLI

> 读设备日志（`时间戳 通道 状态 数值`），统计每通道记录数 / 状态分布 / 数值 min·max·avg，输出 TopN 通道。

- **当前状态**：Step 1（日志样本）已就绪；**C 源码还没开始写**（Step 2 从 `main.c` + Makefile 开始）。
- 开工简报（需求 / 六步路线 / 验收 / 坑 / 面试题）：[`../开工简报.md`](../开工简报.md)
- 规格：`《项目规格书 V1.0》§2` + 附录 A.1

## 目录

```text
devlogstat/
├── src/       # main.c（参数与流程） / parse.c（行解析） / stats.c（统计） / *.h
├── tests/     # 解析、统计纯函数单测（≥8 用例）
├── tools/     # gen_sample.py（样本生成器）
├── samples/   # 日志样本 + 对照答案（见 samples/README.md）
├── docs/      # 理解清单、数据流图
└── README.md
```

## 现在能跑的命令（只有造样本）

```bash
python3 tools/gen_sample.py --lines 1000 --out samples/devlog_1000.log
python3 tools/gen_sample.py --lines 100000 --out samples/devlog_100k.log
```

## 后续命令（Step 2 起逐步补上）

```bash
make            # 构建（-Wall -Wextra 零警告）
./devlogstat --file samples/devlog_1000.log --top 5
./devlogstat --file samples/devlog_1000.log --status ERR
make test       # 单测全绿
```
