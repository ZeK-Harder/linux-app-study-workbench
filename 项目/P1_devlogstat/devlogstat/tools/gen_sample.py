#!/usr/bin/env python3
"""生成 P1 devlogstat 的设备日志样本（格式见《项目规格书》附录 A.1）。

每行一条记录，空格分隔 4 个字段：

    2026-11-05T10:00:00.100 CH2 OK 42.0

    timestamp                channel  status  value
    YYYY-MM-DDTHH:MM:SS.mmm  CH1-CH8   OK/WARN/ERR  float（本样本统一 1 位小数）

    （上面是默认参数 --seed 42 --lines 1000 生成时的第一行；时间戳每行 +100ms。）

坏行约占 2%（默认每 50 行埋 1 行），三类轮换，用于练习「解析失败要计数并跳过」：
    missing_field   字段数不对（只有 3 个字段）
    unknown_status  状态未知（FATAL）
    bad_value       数值非法（abc）

设计要点（为什么这样写）：
1. 固定随机种子 → 同样参数生成的文件逐字节一致，方便和单测、C 程序结果对照。
2. 生成的同时用「自己写出去的数」算一份统计，写到 <out>.stats.txt，
   作为 C 程序统计结果的对照答案（不需要第二份解析器）。
   除全局统计外，还按状态给出 每通道计数 + 数值 min/max/avg，
   供 `--status OK|WARN|ERR` 过滤后的结果对照（F1-7）。
3. 换行符强制 \\n：脚本在 Windows 或 WSL 跑，产物都是 LF，
   避免 C 侧 fgets 读到行尾 \\r 导致「看起来一样的行解析失败」。
4. 时间戳每行 +100ms，和规格书示例一致；MVP 只做字符串切分，不做时间库转换。

用法（在 devlogstat/ 目录下）：
    python3 tools/gen_sample.py --lines 1000  --out samples/devlog_1000.log
    python3 tools/gen_sample.py --lines 100000 --out samples/devlog_100k.log

注意：本文件是「造数据的工具」，不是 P1 的学习重点；P1 核心 C 代码自己写。
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

CHANNELS = [f"CH{i}" for i in range(1, 9)]
STATUSES = ["OK", "WARN", "ERR"]
# 设备日志常见比例：正常多、警告次之、错误少
STATUS_WEIGHTS = [70, 20, 10]
BAD_KINDS = ["missing_field", "unknown_status", "bad_value"]

START_TIME = datetime(2026, 11, 5, 10, 0, 0)
STEP = timedelta(milliseconds=100)
VALUE_MIN = 20.0   # 模拟数值单位量程的下限
VALUE_MAX = 100.0  # 上限


def format_timestamp(moment):
    """datetime -> 2026-11-05T10:00:00.123（毫秒 3 位，与 A.1 一致）。"""
    return f"{moment:%Y-%m-%dT%H:%M:%S}.{moment.microsecond // 1000:03d}"


def make_bad_line(kind, timestamp, rng):
    """按坏行类型造一行；返回 (行文本, 坏行类型名)。"""
    channel = rng.choice(CHANNELS)
    value = rng.uniform(VALUE_MIN, VALUE_MAX)
    if kind == "missing_field":
        return f"{format_timestamp(timestamp)} {channel} OK", kind
    if kind == "unknown_status":
        return f"{format_timestamp(timestamp)} {channel} FATAL {value:.1f}", kind
    return f"{format_timestamp(timestamp)} {channel} OK abc", kind


def append_value_stats(stats_lines, prefix, count, vmin, vmax, vsum):
    """把 min/max/avg 追加到 stats_lines；没有有效行时写 n/a，避免除零。"""
    if count:
        stats_lines.append(f"{prefix}value_min: {vmin:.1f}")
        stats_lines.append(f"{prefix}value_max: {vmax:.1f}")
        stats_lines.append(f"{prefix}value_avg: {vsum / count:.2f}")
    else:
        stats_lines.append(f"{prefix}value_min: n/a")
        stats_lines.append(f"{prefix}value_max: n/a")
        stats_lines.append(f"{prefix}value_avg: n/a")


def main():
    parser = argparse.ArgumentParser(description="生成 devlogstat 设备日志样本")
    parser.add_argument("--lines", type=int, default=1000, help="总行数（默认 1000）")
    parser.add_argument("--out", default="samples/devlog_1000.log", help="输出文件")
    parser.add_argument("--seed", type=int, default=42, help="随机种子（默认 42）")
    parser.add_argument(
        "--bad-every",
        type=int,
        default=50,
        help="每 N 行埋 1 行坏行（默认 50，即 2%%；0 = 不埋坏行）",
    )
    args = parser.parse_args()

    if args.lines <= 0:
        parser.error("--lines 必须 > 0")
    if args.bad_every < 0:
        parser.error("--bad-every 不能为负")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    channel_count = {ch: 0 for ch in CHANNELS}
    status_count = {st: 0 for st in STATUSES}
    bad_by_kind = {kind: 0 for kind in BAD_KINDS}
    good_lines = 0
    value_min = None
    value_max = None
    value_sum = 0.0
    # 按状态再记一份（--status 过滤后的对照答案）
    status_channel = {st: {ch: 0 for ch in CHANNELS} for st in STATUSES}
    status_value_min = {st: None for st in STATUSES}
    status_value_max = {st: None for st in STATUSES}
    status_value_sum = {st: 0.0 for st in STATUSES}

    lines = []
    for index in range(1, args.lines + 1):
        timestamp = START_TIME + STEP * index
        is_bad = args.bad_every > 0 and index % args.bad_every == 0
        if is_bad:
            kind = BAD_KINDS[(index // args.bad_every - 1) % len(BAD_KINDS)]
            bad_line, kind = make_bad_line(kind, timestamp, rng)
            lines.append(bad_line)
            bad_by_kind[kind] += 1
            continue

        channel = rng.choice(CHANNELS)
        status = rng.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        value = round(rng.uniform(VALUE_MIN, VALUE_MAX), 1)
        lines.append(f"{format_timestamp(timestamp)} {channel} {status} {value:.1f}")

        channel_count[channel] += 1
        status_count[status] += 1
        status_channel[status][channel] += 1
        good_lines += 1
        value_sum += value
        value_min = value if value_min is None else min(value_min, value)
        value_max = value if value_max is None else max(value_max, value)
        status_value_sum[status] += value
        status_value_min[status] = (
            value if status_value_min[status] is None else min(status_value_min[status], value)
        )
        status_value_max[status] = (
            value if status_value_max[status] is None else max(status_value_max[status], value)
        )

    out_path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")

    bad_lines = args.lines - good_lines
    stats_lines = [
        f"total_lines: {args.lines}",
        f"good_lines: {good_lines}",
        f"bad_lines: {bad_lines}",
    ]
    for kind in BAD_KINDS:
        stats_lines.append(f"bad_{kind}: {bad_by_kind[kind]}")
    for status in STATUSES:
        stats_lines.append(f"status_{status}: {status_count[status]}")
    for channel in CHANNELS:
        stats_lines.append(f"channel_{channel}: {channel_count[channel]}")
    stats_lines.append(f"value_min: {value_min:.1f}" if value_min is not None else "value_min: n/a")
    stats_lines.append(f"value_max: {value_max:.1f}" if value_max is not None else "value_max: n/a")
    stats_lines.append(f"value_avg: {value_sum / good_lines:.2f}" if good_lines else "value_avg: n/a")

    # --status 过滤后的对照：先每通道计数，再数值 min/max/avg
    for status in STATUSES:
        for channel in CHANNELS:
            stats_lines.append(
                f"status_{status}_channel_{channel}: {status_channel[status][channel]}"
            )
    for status in STATUSES:
        append_value_stats(
            stats_lines,
            f"status_{status}_",
            status_count[status],
            status_value_min[status],
            status_value_max[status],
            status_value_sum[status],
        )

    stats_path = out_path.with_suffix(out_path.suffix + ".stats.txt")
    stats_path.write_text("\n".join(stats_lines) + "\n", encoding="utf-8", newline="\n")

    print(f"写出 {out_path}：{args.lines} 行（有效 {good_lines} / 坏行 {bad_lines}）")
    print(f"对照统计 {stats_path}")
    print(f"坏行分布：{bad_by_kind}")


if __name__ == "__main__":
    main()
