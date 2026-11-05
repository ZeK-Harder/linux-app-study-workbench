# hello-linux（练习脚手架）

P0 环境与工具箱的交付物：验证 gcc / make / gdb / git 全链路。

## 构建与运行

```bash
make            # 编译
make run        # 运行（默认 n=10）
./hello 100     # 传参运行
make debug      # gdb 调试
make clean      # 清理
```

## gdb 练习

```bash
gdb ./hello
(gdb) break main
(gdb) run
(gdb) next
(gdb) step        # 进入 sum_to
(gdb) bt          # 看调用栈
(gdb) print n
(gdb) quit
```

## 理解要点（P0 理解清单）

- 源码到运行：预处理 → 编译 → 汇编 → 链接 → ELF → 加载 → main
- `-Wall -Wextra` 为什么不能省
- `-g` 为什么 gdb 需要
- Makefile 的依赖与 `.PHONY`
