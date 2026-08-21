# 架构图集（纯文本版）

> 适用于 GitHub 渲染 / VS Code 预览 / 终端 cat
> 所有图使用 ASCII 字符 + Markdown 表格绘制，GitHub 完美渲染

---

## 1. Phase 3 — VPC 网络架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                          🌐 Internet                                  │
└──────────────┬───────────────────────────────────┬──────────────────┘
               │ HTTPS (443)                       │ Outbound traffic
               ▼                                   ▼
       ┌───────────────┐                  ┌─────────────────┐
       │ ⚖️  CLB        │                  │ 🔀  NAT Gateway │
       │ (负载均衡)      │                  │ (出站网关)       │
       └───────┬───────┘                  └────────┬────────┘
               │                                    │
       ┌───────┴───────────────────────────────────────────────────────┐
       │  📦 VPC  10.0.0.0/16                                         │
       │  ┌──────────────────────────────────┐  ┌────────────────────┐ │
       │  │ 🟢 Public Subnet  10.0.1.0/24     │  │ 🔴 Private Subnet   │ │
       │  │ ┌────────┐    ┌────────┐          │  │ 10.0.2.0/24        │ │
       │  │ │🖥️ CVM-1│    │🖥️ CVM-2│          │  │ ┌──────┐ ┌──────┐ │ │
       │  │ │Web     │◄──►│Web     │  SQL/Cache│  │ │🗄️    │ │⚡    │ │ │
       │  │ └────────┘    └────────┘  ──────►│  │ │MySQL│ │Redis│ │ │
       │  │                                │  │ └──────┘ └──────┘ │ │
       │  └──────────────────────────────────┘  └────────────────────┘ │
       └───────────────────────────────────────────────────────────────┘
```

### 组件说明

| 组件 | 类型 | 作用 | CIDR |
|------|------|------|------|
| Internet | 公网 | 用户入口 | — |
| CLB | 公网 | HTTPS 负载均衡 (443) | — |
| NAT Gateway | 公网 | 内网出站代理 | — |
| Public Subnet | 子网 | 放 Web 服务器 | 10.0.1.0/24 |
| CVM Web-1/2 | 计算 | Nginx + Web 应用 | — |
| Private Subnet | 子网 | 放数据库 | 10.0.2.0/24 |
| MySQL | 数据库 | 主数据库 | — |
| Redis | 缓存 | 加速读性能 | — |

### 流量路径

```
User → Internet → CLB → Public Subnet → CVM Web → Private Subnet → MySQL/Redis
                    ↑                                              ↓
                    └──────────── Response ←──────────────────────┘
CVM → NAT Gateway → Internet (出站)
```

---

## 2. Phase 5 — 高可用 Web 架构 (Multi-AZ)

```
                        🌐 Users
                            │ HTTPS request
                            ▼
                  ⚖️ CLB + Auto Scaling
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│  📦 VPC  Multi-AZ                                          │
│  ┌────────────────────┐    ┌────────────────────┐         │
│  │ 🟢 AZ-1: 广州3区    │    │ 🟢 AZ-2: 广州4区    │         │
│  │                    │    │                    │         │
│  │ 🖥️ CVM Web-01      │    │ 🖥️ CVM Web-02      │         │
│  │                    │    │ 🖥️ CVM Web-03      │         │
│  │         ┌─────────┐│    │         ┌─────────┐│         │
│  │         │ 🗄️ MySQL││ ──►│         │ 🗄️ MySQL││         │
│  │         │ Master  ││ repl│         │ Replica ││         │
│  │         └─────────┘│    │         └─────────┘│         │
│  │                    │    │                    │         │
│  │         ⚡ Redis   ││ ──►│         ⚡ Redis   ││         │
│  │         │ Master  ││ rep │         │ Replica ││         │
│  │         └─────────┘│    │         └─────────┘│         │
│  └────────────────────┘    └────────────────────┘         │
│                                                            │
│                  📦 COS (Static Files)                     │
└──────────────────────────────────────────────────────────┘
```

### 组件清单

| 组件 | 数量 | AZ 分布 | 作用 |
|------|------|---------|------|
| CLB | 1 | 公网 | HTTPS 终止 + 负载均衡 |
| CVM Web | 3 | AZ-1×2 + AZ-2×1 | Web 应用 |
| MySQL | 2 | Master(AZ-1) + Replica(AZ-2) | 数据库主从 |
| Redis | 2 | Master(AZ-1) + Replica(AZ-2) | 缓存主从 |
| COS | 1 | — | 静态资源 |

---

## 3. Phase 7 — 完整生产环境

```
┌────────────────── Top ──────────────────────────────────────┐
│ 🚀 GitLab ──► 🚀 CI/CD ──────────► 📊 Monitor + Alerts │
└────────┬─────────────────────────────────────┬─────────────┘
         │                                     │
         ▼                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  📦 Production VPC  Multi-AZ                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🟢 Public Subnet                                          │  │
│  │ ⚖️ CLB  🔑 Bastion  🔀 NAT  🛡️ WAF  🌍 DNSPod           │  │
│  │ [AZ-1]                          [AZ-2]                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🟠 Web Tier (ASG, prevent_destroy)                       │  │
│  │ 🖥️CVM-1  🖥️CVM-2  🖥️CVM-3  🖥️CVM-4  🖥️CVM-5         │  │
│  │ [AZ-1]  [AZ-1]   [AZ-2]  [AZ-2]   [AZ-2]                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔴 Data Tier (Private)                                   │  │
│  │ 🗄️MySQL Master 🗄️MySQL Replica ⚡Redis 📨CKafka 🗄️TDSQL│  │
│  │ [AZ-1]              [AZ-2]        [1+2]  [MQ]   [1+2]   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔵 Storage Tier                                          │  │
│  │ 📦 COS    💾 CBS    📋 Snapshot    📊 VPC Flow Logs        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│       ┌────────────────┐                                       │
│       │ 🟢 Test VPC     │◄─── Peering ───►                     │
│       └────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

### 分层组件

| 层级 | 组件 | 数量 | AZ |
|------|------|------|-----|
| **CI/CD** | GitLab, Pipeline | 各 1 | — |
| **监控** | Cloud Monitor + CLS | 1 | — |
| **Public Subnet** | CLB, Bastion, NAT, WAF, DNSPod | 各 1 | — |
| **Web Tier** | CVM (ASG) | 5 | 2+3 |
| **Data Tier** | MySQL M/R, Redis, CKafka, TDSQL-C | 6 | — |
| **Storage** | COS, CBS, Snapshot, Flow Logs | 各 1 | — |

---

## 4. Project 1 — 单机 Web 应用

```
                🌐 User Browser
                       │ HTTPS
                       ▼
        ┌──────────────────────────────────┐
        │  📦 VPC                         │
        │  ┌────────────────┐ ┌─────────┐ │
        │  │ 🖥️ CVM Server  │ │ 📦 COS   │ │
        │  │ Nginx + Web    │ │ Static  │ │
        │  │ Public IP      │ │ Files   │ │
        │  └────────────────┘ └─────────┘ │
        │       │ upload      │ download  │
        │       └──────────────┘          │
        └──────────────────────────────────┘

💰 Cost: ~0.5 CNY/h  |  Total: ~10-20 CNY (1-2 days)
🔒 Security: SSH key-pair, admin_ip restricted
```

### 组件

| 组件 | 作用 |
|------|------|
| CVM Server | Nginx + Web Page，绑定公网 IP |
| COS Bucket | 静态文件（图片、JS、CSS） |
| Security | SSH 密钥对登录 + admin_ip 限制 |

---

## 5. Project 2 — 高可用 Web 架构

```
                          🌐 Users
                            │
                            ▼
                  ⚖️ CLB + Auto Scaling
                            │
        ┌───────────────────┼───────────────────────┐
        ▼                   ▼                       ▼
┌─────────────────────────────────────────────────────────────┐
│  📦 VPC                                                       │
│  ┌─────────────────────────┐  ┌──────────────────────────┐  │
│  │ 🟢 AZ-1: 广州3区         │  │ 🟢 AZ-2: 广州4区          │  │
│  │ 🖥️ CVM-01               │  │ 🖥️ CVM-03                │  │
│  │ 🖥️ CVM-02               │  │                            │  │
│  │ 🗄️ MySQL Master ──replication──► 🗄️ MySQL Replica   │  │
│  │ ⚡ Redis Replica ◄──replication──── ⚡ Redis Master  │  │
│  └─────────────────────────┘  └──────────────────────────┘  │
│                                                              │
│  📦 COS (Static)    💾 CBS (Data)    📋 CBS Snapshot         │
└─────────────────────────────────────────────────────────────┘

💰 Cost: ~5-8 CNY/h  |  Total: ~50-100 CNY (3-4 days)
```

### 组件清单

| 组件 | AZ-1 | AZ-2 | 副本方向 |
|------|------|------|---------|
| CVM Web | 2 台 (01, 02) | 1 台 (03) | — |
| MySQL | Master | Replica | AZ-1 → AZ-2 |
| Redis | Replica | Master | AZ-2 → AZ-1 |
| COS / CBS | — | — | 跨 AZ |

---

## 6. Project 3 — 完整生产环境（含灾备）

```
┌─── Top: Multi-Account & Cost Control ─────────────────────────┐
│  🏢 Multi-Account    🚀 CI/CD Pipeline    💰 Cost + Budget   │
└────────┬─────────────────────────────────────┬────────────────┘
         │                                     │
         ▼                                     ▼
┌─────────────────────────────────────┐  ┌─────────────────────────┐
│  📦 Production VPC (Primary)         │  │ 📦 DR VPC (ap-shanghai) │
│  ┌─────────────────────────────────┐ │  │ ┌─────────────────────┐ │
│  │ 🟢 Public Subnet                │ │  │ │ 🟡 DR Subnet        │ │
│  │ ⚖️ CLB  🔑 Bastion  🔀 NAT 🛡️WAF│ │  │ │ ⚖️ CLB DR           │ │
│  └─────────────────────────────────┘ │  │ │ 🖥️ CVM Standby     │ │
│  ┌─────────────────────────────────┐ │  │ │ 🗄️ MySQL DR        │ │
│  │ 🟠 Web Tier (ASG)               │ │  │ │ ⚡ Redis DR         │ │
│  │ 🖥️CVM-1 🖥️CVM-2 🖥️CVM-3 🖥️CVM-4│ │  │ │ 📦 Object Backup    │ │
│  └─────────────────────────────────┘ │  │ │ 💾 Snapshot Mirror │ │
│  ┌─────────────────────────────────┐ │  │ └─────────────────────┘ │
│  │ 🔴 Data Tier (Private)          │ │  │   RTO < 1h             │
│  │ 🗄️MySQL M  🗄️MySQL R  ⚡Redis │ │  │   RPO < 15min           │
│  │ 📨CKafka  🗄️TDSQL-C             │ │  └─────────────────────────┘
│  └─────────────────────────────────┘ │           ▲
│  ┌─────────────────────────────────┐ │           │
│  │ 🔵 Storage                      │ │  ┌────────┴─────────┐
│  │ 📦COS  💾CBS  📊Terraform State│ │  │ async replication│
│  └─────────────────────────────────┘ │  │ CRR backup        │
└─────────────────────────────────────┘  └────────────────────┘

💰 Cost: ~10-15 CNY/h (with DR) | 5-7 days ~ 200-500 CNY
```

### 关键设计点

| 模块 | 实现 | 说明 |
|------|------|------|
| **Multi-Account** | Organizations | 生产/测试/开发账号隔离 |
| **CI/CD** | Plan → Review → Apply | 带审批门禁 |
| **Web Tier** | ASG + `prevent_destroy` | 防误删 |
| **Data Tier** | 跨 AZ 主从 | 高可用 |
| **Storage** | COS 加密 + 版本控制 | 可恢复 |
| **State** | COS Backend | 远程 + 锁定 |
| **DR Region** | 异地 VPC + async 复制 | RTO < 1h |
| **Cost** | Budget Alerts | 自动告警 |

---

## 7. 组件图标速查表

| 图标 | 含义 | 图标 | 含义 |
|------|------|------|------|
| 🌐 | Internet / User | ⚖️ | CLB (负载均衡) |
| 🔀 | NAT Gateway | 📦 | VPC |
| 🟢 | Public Subnet | 🔴 | Private Subnet |
| 🟠 | Web Tier / ASG | 🔵 | Storage |
| 🖥️ | CVM (计算) | 🗄️ | MySQL / TDSQL |
| ⚡ | Redis Cache | 📨 | CKafka (消息队列) |
| 💾 | CBS (云硬盘) | 🛡️ | WAF (防火墙) |
| 🔑 | Bastion (跳板机) | 🌍 | DNSPod (DNS) |
| 🚀 | CI/CD Pipeline | 📊 | Monitor / Logging |

---

## 8. 颜色语义约定

| 颜色 | 含义 | 典型用法 |
|------|------|---------|
| 🟢 绿色 | 公网/入口 | Public Subnet, AZ-1, Internet |
| 🔴 红色 | 内网/敏感 | Private Subnet, Database, Security |
| 🟠 橙色 | 计算层 | Web Tier, CVM, ASG |
| 🔵 蓝色 | 存储层 | COS, CBS, Storage |
| 🟡 黄色 | 监控/告警 | Monitor, DR Region, Alarms |

---

## 9. 架构选型速查

| 场景 | 选型 | 教程参考 |
|------|------|---------|
| 单机博客/测试 | CVM + COS | Project 1 |
| 中小 Web 应用 | CLB + 多 CVM + MySQL | Project 2 |
| 完整生产（单 region） | + ASG + Redis + DR 备份 | Phase 7 |
| 异地容灾 | + DR Region + async 复制 | Project 3 |
| CI/CD 自动化 | GitHub Actions / GitLab CI | Phase 5 |
| 微服务 | TKE + Nacos + CKafka | (扩展) |

---

*所有图均为纯文本 ASCII，可直接复制到任何 Markdown 渲染器使用。*
