# samples · 设备日志样本

> 格式来自《项目规格书》附录 A.1；由 `../tools/gen_sample.py` 生成（固定种子，可逐字节重现）。
> **这些样本是 P1 所有统计结果的对照答案，不要手改。**

## 文件

| 文件 | 行数 | 大小 | 入库 | 用途 |
|---|---|---|---|---|
| `devlog_1000.log` | 1000 | ~36 KB | ✅ | 演示、单测对照、`sed` 抽查坏行 |
| `devlog_1000.log.stats.txt` | — | 小 | ✅ | 1000 行样本的对照答案（生成器自己记的） |
| `devlog_100k.log` | 100000 | ~3.5 MB | ❌（生成） | 性能/流式验证：`--file` 指向它，RSS 应平稳 |
| `devlog_100k.log.stats.txt` | — | 小 | ❌（生成） | 10 万行对照答案 |

> `devlog_100k.*` 被 `.gitignore` 忽略（~3.5 MB，入库太大）：换机器/新克隆后先跑一次生成命令。

## 格式

每行 4 个空格分隔字段：`时间戳 通道 状态 数值`

```text
2026-11-05T10:00:00.100 CH2 OK 42.0
2026-11-05T10:00:00.200 CH4 OK 28.2
```

- 时间戳：`YYYY-MM-DDTHH:MM:SS.mmm`，每行 +100ms（MVP 只做字符串切分）
- 通道：`CH1`–`CH8`
- 状态：`OK` / `WARN` / `ERR`
- 数值：float，1 位小数，量程 20.0–100.0

## 坏行（约 2%，每 50 行埋 1 行，三类轮换）

| 行号（1000 行样本首次出现） | 类型 | 样例 |
|---|---|---|
| 50 | 缺字段（3 字段） | `2026-11-05T10:00:05.000 CH1 OK` |
| 100 | 未知状态 | `2026-11-05T10:00:10.000 CH3 FATAL 54.4` |
| 150 | 非法数值 | `2026-11-05T10:00:15.000 CH2 OK abc` |

正确解析器的行为：**计入 `bad_lines`，跳过该行，继续读**。

## 对照答案（1000 行，摘要）

> **不是原文**：逐字对照请 `cat samples/devlog_1000.log.stats.txt`（53 行，含分通道/分状态明细）。

```text
total_lines: 1000
good_lines: 980
bad_lines: 20              # 缺字段 7 + 未知状态 7 + 非法数值 6
status_OK: 691  status_WARN: 199  status_ERR: 90
channel_CH1: 115  CH2: 129  CH3: 126  CH4: 128
             CH5: 117  CH6: 127  CH7: 123  CH8: 115
value_min: 20.1  value_max: 100.0  value_avg: 61.36

# --status 过滤后的对照（stats.txt 里也有）
status_OK_value_min: 20.1    status_OK_value_max: 99.9    status_OK_value_avg: 61.74
status_WARN_value_min: 20.7  status_WARN_value_max: 100.0 status_WARN_value_avg: 60.68
status_ERR_value_min: 20.1   status_ERR_value_max: 99.4   status_ERR_value_avg: 59.95
status_ERR_channel_CH1: 17  CH2: 12  CH3: 8   CH4: 6
                    CH5: 9   CH6: 14  CH7: 14  CH8: 10
```

10 万行：`good_lines: 98000`、`bad_lines: 2000`、`value_min: 20.0`、`value_max: 100.0`、`value_avg: 60.14`（完整见 `devlog_100k.log.stats.txt`）。

> 统计只算「有效行」；数值 avg 保留 2 位小数，C 侧用 `double` 累加，允许最后一位 ±0.01 舍入差。
> `status_<S>_channel_<CH>` = 只看该状态时该通道的记录数，`status_<S>_value_*` = 只看该状态时的数值三项 —— 供 `--status` 过滤后的结果对照（F1-7）。
> 注意 1000 行样本的 `value_min = 20.1` 不是量程下限 20.0：如果你的 min 写死成 20.0 就会露馅。

## 重新生成 / 自查

```bash
cd "/mnt/c/Users/24552/Documents/Linux应用/项目/P1_devlogstat/devlogstat"

# 1000 行（已入库；重生成后 cmp 应一致）
python3 tools/gen_sample.py --lines 1000 --out samples/devlog_1000.log

# 10 万行（不入库，本机现场生成）
python3 tools/gen_sample.py --lines 100000 --out samples/devlog_100k.log

# 验证可重现（同一种子 → 逐字节一致）
python3 tools/gen_sample.py --lines 1000 --out /tmp/regen.log
cmp samples/devlog_1000.log /tmp/regen.log && echo 一致

# 验证是 LF 而不是 CRLF（应显示 ASCII text）
file samples/devlog_1000.log
```

参数：`--lines N`、`--out 路径`、`--seed 42`、`--bad-every 50`（0 = 不埋坏行）。

## 为什么换行符/编码不能随意（必须 LF + ASCII）

样本会被 WSL 里的 C 程序用 `fgets` 读。若文件是 CRLF，行尾 `\r` 会留在最后一个字段：

- 按空格 `strtok` / 手工切分时，`strtod` 的尾部检查会失败 → 实测 1000 行**全部**被判坏；
- 用 `sscanf("%s ...")` 时 `\r` 被当空白吃掉，可能侥幸不坏 —— 但这取决于你行的切分写法，别赌。

生成器已强制 `\n` + ASCII（`file` 应显示 `ASCII text`，不是 `with CRLF`）；解析时也建议顺手去掉行尾 `\r`/`\n`，两道保险。
