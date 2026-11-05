# P3 · devhub 设备数据小服务（6 周）★ 可投递

## 目标

多客户端 TCP 上报（长度前缀 + CRC 帧），服务端解析 / 落盘 / 转发。

## 技术轴

socket、TCP、粘包半包、poll/epoll（LT 起步）、非阻塞、帧协议、日志与性能排查

## 完成标准

- **MVP**：单进程 epoll LT + 帧协议 + 落盘 + 10 连接 10 分钟不崩 + 能画数据流图
- **进阶**：ET、100 连接 30 分钟、Python 压测客户端
- 理解清单要点：非阻塞、LT/ET、EAGAIN、粘包半包、线程模型、瓶颈定位、压测方法

## 验收

MVP + 理解清单 8/10 + 数据流图 + 3 分钟口述稿。

## 目录建议

```text
devhub/
├── src/            # server.c / conn.c / frame.c / log.c
├── tests/          # 帧解析与切包单测
├── tools/          # python 压测客户端 / 设备模拟器
├── docs/           # 数据流图 + 理解清单
├── Makefile
└── README.md
```
