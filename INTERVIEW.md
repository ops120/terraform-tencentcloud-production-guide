# Terraform & DevOps 面试高频题库（2024-2025）

> 来源：Reddit r/devops & r/Terraform、Glassdoor、YouTube（DevOps Pink、in28minutes）、Medium 热门文章、DataCamp、ZeroToMastery、Simplilearn、GeeksforGeeks、HashiCorp 官方认证题库
>
> 共 **78 道高频题**，覆盖 5 大分类
>
> 本文档所有题目均按"中文标题 + 序号"组织，便于学习和检索

---

## ⚠️ 答案免责声明

**所有答案（主答案 + 追问参考答案）均为 AI 根据训练知识整理的参考思路，未经过实际验证。**

面试准备建议：
1. **答案要点**仅供参考答题框架和关键词
2. 面试前请**自己测试/核对官方文档**
3. 用自己的话复述，能讲出实战案例 > 背答案
4. **核对方式**：官方文档 > 官方认证题库 > HashiCorp 博客


---

## 📊 题目分布与高频考点

| 分类 | 题目数 | 占比 |
|------|--------|------|
| 一、Terraform 基础（Q01-Q15） | 15 | 19% |
| 二、Terraform 进阶（Q16-Q30） | 15 | 19% |
| 三、DevOps / SRE 综合（Q31-Q40） | 10 | 13% |
| 四、云架构场景设计（Q41-Q50） | 10 | 13% |
| 五、场景/排障/对比/行为题（Q51-Q78） | 28 | 36% |

### 🔥 最高频出现的 5 个主题

1. **State 文件管理**（每场面试必问）
2. **多环境设计**（workspaces vs directory-per-environment）
3. **Drift 检测与修复**（`terraform plan -refresh-only`）
4. **CI/CD 集成 + 审批门禁**
5. **Secrets 管理 + 安全实践**

---

## 一、Terraform 基础（15 题）

### Q01: 什么是 Terraform？它与 Ansible 有什么区别？

- **难度**: 初级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **出处**: Reddit, Glassdoor, YouTube, DataCamp
- **答案要点**:
  1. Terraform 是 HashiCorp 的**声明式（declarative）IaC 工具**，专注基础设施**编排（orchestration）**
  2. Ansible 是**命令式（imperative）配置管理工具**，专注**配置（configuration management）**
  3. Terraform 自动计算**依赖图**；Ansible 按步骤顺序执行
  4. Terraform 有 **state 文件**跟踪资源；Ansible 无状态
  5. Terraform **多云支持**；Ansible 侧重服务器配置
- **追问**: "Terraform 和 Ansible 能配合使用吗？" / "两者的幂等性有什么区别？"

---

### Q02: Terraform state 文件是什么？为什么它如此重要？

- **难度**: 初级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **出处**: Reddit r/Terraform, HashiCorp 认证题, YouTube, Medium
- **答案要点**:
  1. `terraform.tfstate` 记录云资源 ID 和属性，建立代码与实际资源的映射
  2. 支持**增量更新**：plan 比对 state 和代码
  3. **绝不能提交到 Git**（含敏感信息如 IP、密钥）
  4. 团队协作必须用**远程 state + 锁**
  5. State 丢失 = Terraform 不认识资源，会尝试重建导致冲突
- **追问**: "State 丢失怎么办？" / "如何团队共享 state？"

---

### Q03: Terraform provider 是什么？如何工作？

- **难度**: 初级 | **频率**: 高频 ⭐⭐⭐⭐
- **出处**: Reddit, HashiCorp 认证, DataCamp
- **答案要点**:
  1. Provider 是**插件**，通过 Terraform Plugin Protocol 与云 API 通信
  2. `terraform init` 下载 provider 到 `.terraform/` 目录
  3. `.terraform.lock.hcl` 锁定 provider 版本和哈希
  4. 一个配置文件可使用多个 provider（如 `provider "aws" { alias = "east" }`）
  5. 编写自定义 provider 需要 Go 语言

---

### Q04: resource 和 data source 有什么区别？

- **难度**: 初级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. `resource`：**创建 / 管理**资源（CRUD）
  2. `data source`：**只读查询**现有资源（如查询 AMI ID、可用的 AZ）
  3. Data source 不在 state 中保存属性
  4. 使用场景：DRY 原则、避免硬编码、查询动态值

---

### Q05: Module 是什么？和直接写 resource 有什么区别？

- **难度**: 初级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. Module 是**可复用的资源组**，封装多个 resource
  2. 输入（variables）+ 输出（outputs）+ 实现（main.tf）
  3. 支持版本管理（Git tag / Registry）
  4. **何时用**：资源超过 3 个、多团队复用、跨环境共享
  5. **何时不用**：单个文件、一次性部署

---

### Q06: Backend 是什么？和 local 有什么区别？

- **难度**: 初级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. Backend 决定 **state 文件存储位置**和执行方式
  2. Local（默认）：state 存在本地磁盘；Remote（S3/COS/Terraform Cloud）：state 存在云端 + 自动锁
  3. 团队协作**必须用 Remote Backend**
  4. `partial-configuration` 通过 `-backend-config` 传入参数
  5. Terraform Cloud 还提供远程执行、Plan 审计、Policy 检查

---

### Q07: 解释 Terraform 的 lifecycle（生命周期）块

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. `create_before_destroy`：先创建新资源再删旧的（避免 downtime）
  2. `prevent_destroy`：防止误删关键资源（如数据库）
  3. `ignore_changes`：忽略某些属性变化（如自动生成的密码）
  4. `replace_triggered_by`：强制替换资源
  5. lifecycle 是 Terraform 中**保护重要资源**的关键

---

### Q08: Terraform 变量有哪些类型？sensitive 是什么？

- **难度**: 初级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 类型：`string`, `number`, `bool`, `list`, `map`, `set`, `object`, `tuple`
  2. `sensitive = true`：标记为敏感，**plan/apply 输出会隐藏**，但**State 中仍明文存储**
  3. **真正安全**的做法：环境变量 + SSM/KMS + Remote Backend 加密
  4. variable 还可以有 `default`, `validation`, `nullable`

---

### Q09: 解释 Terraform 常用命令

- **难度**: 初级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. `init`：下载 provider + 初始化 backend
  2. `plan`：预览变更（不实际执行）
  3. `apply`：执行变更
  4. `destroy`：销毁资源
  5. `fmt`：格式化代码，`validate`：语法检查，`state list/show/rm/mv`：操作 state

---

### Q10: Terraform 如何处理资源依赖？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. **隐式依赖**：通过变量引用（如 `vpc_id = aws_vpc.main.id`）
  2. **显式依赖**：`depends_on = [aws_iam_role.example]`
  3. Terraform 自动构建**依赖图**，按顺序执行
  4. `create_before_destroy` 会改变依赖方向

---

### Q11: 什么是 Terraform Registry？如何使用？

- **难度**: 初级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. Registry 是**公共模块库**（registry.terraform.io）
  2. 引用方式：`module "vpc" { source = "terraform-aws-modules/vpc/aws" version = "5.0.0" }`
  3. 私有的可以用 GitHub/GitLab + `git::https://...`
  4. 内部公司可搭建**私有 Registry**（如 Terraform Cloud Private Registry）

---

### Q12: 什么是 HCL？和 JSON/YAML 比有什么优势？

- **难度**: 初级 | **频率**: 低频 ⭐⭐
- **答案要点**:
  1. HCL = HashiCorp Configuration Language，**专为 IaC 设计**
  2. JSON 太严格（无注释、无变量），YAML 缩进易错、复杂嵌套难读
  3. HCL 支持**表达式、函数、注释、块结构**
  4. JSON 是 Terraform 的"备份格式"（`.tf.json`），机器生成用
  5. HCL 5 引入新特性（如 `import` block、`optional()` 等）

---

### Q13: provisioner 是什么？什么时候用？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. Provisioner 在资源创建后执行**自定义逻辑**（脚本、文件传输）
  2. 类型：`local-exec`, `remote-exec`, `file`
  3. ⚠️ **最后手段**：state 无法跟踪 provisioner 执行结果
  4. 优先用 `user_data`（云初始化脚本）或自定义镜像
  5. 失败处理：`on_failure = continue`（不推荐）

---

### Q14: 如何管理敏感信息（数据库密码、API Key）？

- **难度**: 中级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. ❌ 错误：硬编码在 `.tf` 文件或 `terraform.tfvars` 提交到 Git
  2. ✅ 推荐：**环境变量**（`TF_VAR_db_password`）
  3. 生产级：**SSM/KMS/Secrets Manager** + IAM 角色
  4. 用 `sensitive = true` 标记变量（仅隐藏输出，不加密 state）
  5. 远程 Backend 必须加密（S3 启用 server-side encryption）

---

### Q15: Terraform 的 "Plan" 输出符号 `+/-/~` 什么意思？

- **难度**: 初级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. `+ create`：新建资源
  2. `- destroy`：删除资源
  3. `~ update in-place`：就地修改（部分属性变化）
  4. `-/+ destroy and create`：替换资源（先删后建）
  5. `+/- create before destroy`：先建后删
  6. `# module.xxx`：模块内的资源

---

## 二、Terraform 进阶（15 题）

### Q16: 什么是 State Locking？为什么需要？

- **难度**: 中级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 防止**多人同时 apply** 导致的 state 冲突
  2. S3 用 DynamoDB 锁；Terraform Cloud 自动锁；Azure 用 blob lease
  3. 锁未释放（CI 崩溃）：用 `terraform force-unlock <lock_id>`
  4. 锁 ID 通过 `terraform output` 或日志查看
  5. **不要在 CI 中禁用锁**（race condition 灾难）

---

### Q17: Drift 是什么？如何检测和修复？

- **难度**: 中级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. Drift = State 记录与**实际云资源**不一致（有人改了控制台）
  2. 检测：`terraform plan -refresh-only` 或普通 `terraform plan`
  3. 修复：
     - 接受实际：`terraform apply` 让代码匹配云
     - 接受代码：`terraform refresh` 更新 state
  4. 预防：开启 CloudTrail 审计、IAM 权限最小化、Terraform 管理所有变更

---

### Q18: `terraform import` 和 `import block` 的区别？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. `terraform import` (CLI, 1.5 之前)：导入到 state 但**不写代码**
  2. `import { to = ... id = ... }` block (1.5+)：**同时写 state 和生成代码**（`-generate-config-out`）
  3. 使用场景：迁移控制台已有资源到 Terraform 管理
  4. 需要先在 `.tf` 中**声明资源骨架**才能 import

---

### Q19: Workspace 和 directory-per-environment 哪个好？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. **Workspaces**：共享代码，仅 state 隔离。适合差异极小的小团队
  2. **Directory-per-environment**：完全独立目录 + state。推荐用于**生产**
  3. Workspaces 缺点：plan 输出混乱、权限隔离差、变量管理复杂
  4. 推荐：**生产用目录隔离**，workspaces 仅用于短生命周期的临时环境

---

### Q20: `count` vs `for_each` 区别？陷阱是什么？

- **难度**: 中级 ⭐⭐⭐⭐⭐（高频陷阱题）
- **答案要点**:
  1. `count`：索引创建相同资源，用 `count.index`
  2. `for_each`：从 Map/Set 创建，用 `each.key` / `each.value`
  3. **count 陷阱**：删除中间元素会**重建所有后续资源**（index 变了）
  4. for_each 用 key 作为标识，删除元素不影响其他
  5. **最佳实践**：默认用 `for_each`，仅当需条件创建时用 `count`

---

### Q21: 远程 State 后端有哪些选择？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. AWS S3 + DynamoDB（最流行）
  2. **腾讯云 COS + 自建锁**（教程中提到）
  3. Azure Storage + Blob Lease
  4. GCS + Lockfile
  5. Terraform Cloud（官方托管，自带锁、Policy、审计）
  6. **Backend 必须支持锁定**，否则不能用

---

### Q22: `prevent_destroy` 有什么用？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 防止 `terraform destroy` 删除关键资源（如生产数据库）
  2. 写在 lifecycle 块：`lifecycle { prevent_destroy = true }`
  3. ⚠️ 但不能阻止**手动控制台删除**
  4. 配合 IAM 权限 + CloudTrail 才能真正保护

---

### Q23: `taint` 和 `-replace` 有什么区别？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. `terraform taint`：标记资源为"已污染"，下次 apply 会**重建**
  2. `terraform apply -replace="..."` (1.6+)：plan 时直接替换，无需 taint
  3. 用途：机器坏了强制重建
  4. taint 已**部分弃用**，推荐 `-replace`

---

### Q24: `moved` block 是什么？

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 用于**资源重命名**而不销毁重建
  2. 写法：`moved { from = aws_instance.old to = aws_instance.new }`
  3. 适用：模块重构后资源地址变化
  4. 替代了之前的 `terraform state mv`

---

### Q25: `dynamic` block 是什么？

- **难度**: 高级 | **频率**: 低频 ⭐⭐
- **答案要点**:
  1. 用于**动态生成嵌套块**（如动态 security_group_rules）
  2. 类似编程语言的循环
  3. 示例：
     ```hcl
     dynamic "ingress" {
       for_each = var.allowed_ports
       content {
         from_port = ingress.value
       }
     }
     ```

---

### Q26: 如何调试 Terraform 代码？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. `TF_LOG=DEBUG terraform apply` 查看详细日志
  2. `TF_LOG_PATH=./log.txt` 输出到文件
  3. 日志级别：`TRACE` > `DEBUG` > `INFO` > `WARN` > `ERROR`
  4. `terraform console`：交互式测试表达式

---

### Q27: 如何升级 Terraform 版本？升级有风险吗？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 升级 Terraform 二进制本身（直接下载新版）
  2. 升级 Provider 版本（修改 `required_providers`）
  3. ⚠️ 风险：Provider 大版本升级可能引入 breaking change
  4. 用 `terraform init -upgrade` 升级 lock 文件
  5. **测试流程**：dev → staging → prod 逐步升级

---

### Q28: 解释 `for` 表达式和 `for_each` 的区别

- **难度**: 中级 | **频率**: 低频 ⭐⭐
- **答案要点**:
  1. `for` 表达式：**转换数据**（类似 list comprehension）
  2. `for_each`：**资源创建**（生成多个资源）
  3. 示例：`[for s in var.servers : s.name]` 是表达式，`for_each = var.servers` 是资源块

---

### Q29: `dynamic` 和 `for_each` 的区别？

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. `for_each` 创建**多个资源实例**
  2. `dynamic` 在**单个资源内**动态生成嵌套块
  3. 例如：`for_each` 创建多个 `aws_security_group`，`dynamic` 在一个 SG 内动态生成多个 `ingress` 规则

---

### Q30: 如何测试 Terraform 代码？

- **难度**: 高级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. **静态检查**：`terraform validate`, `tflint`, `tfsec`, `checkov`
  2. **单元测试**：`terraform test`（1.6+ 原生）
  3. **集成测试**：Terratest（Go 库）
  4. **端到端测试**：在临时 AWS 账号中 apply → 验证 → destroy
  5. 接入 CI：每个 PR 自动跑测试

---

## 三、DevOps / SRE 综合（10 题）

### Q31: Terraform 如何集成到 CI/CD？

- **难度**: 高级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. Pipeline：`init` → `fmt -check` → `validate` → `tflint/tfsec` → `plan` → 审批 → `apply`
  2. **生产环境 apply 必须人工审批**（2 人 approve）
  3. Plan artifact 保存到 S3 或 GitHub artifacts
  4. 使用 OIDC（避免长寿命 AK/SK）
  5. 集成 Slack/Teams 通知失败

---

### Q32: 解释 GitOps 和 Terraform 的结合

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. GitOps = Git 作为唯一真相源
  2. PR 修改 Terraform 代码 → CI 跑 plan → merge → 自动 apply
  3. 工具：ArgoCD、Flux（用于 K8s）；Terraform Cloud 直接支持
  4. 优势：审计、可回滚、可追溯

---

### Q33: SLI / SLO / SLA 是什么？

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. SLI（指标）：如延迟、错误率、吞吐量
  2. SLO（目标）：如 99.9% 可用率
  3. SLA（协议）：与客户的承诺，未达成要赔偿
  4. SLO ≤ SLA，建议预留 buffer
  5. Error Budget：SLO 100% - 99.9% = 0.1% 不可用时间

---

### Q34: 蓝绿 / 滚动 / 金丝雀部署区别？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. **蓝绿**：两套环境，切流量（快速回滚，但资源 2 倍）
  2. **滚动**：逐步替换实例（K8s 默认，节省资源但回滚慢）
  3. **金丝雀**：少量流量验证新版本（最安全，但复杂）
  4. Terraform + Auto Scaling Group 适合滚动部署

---

### Q35: 什么是不可变基础设施（Immutable Infrastructure）？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 服务器部署后**不再修改**，更新只通过替换实例
  2. 优势：可预测、易回滚、避免配置漂移
  3. Terraform 实现：`create_before_destroy` + AMI
  4. 对比：可变基础设施（SSH 进去改配置）= 反模式

---

### Q36: 解释 Toil（运维苦差事）

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **出处**: Google SRE Book
- **答案要点**:
  1. Toil = 手动、重复、可自动化、无长期价值的运维工作
  2. SRE 原则：运维工作**不超过 50%** toil
  3. Terraform / Ansible 是减少 toil 的核心工具
  4. 衡量：每次操作的人工小时数

---

### Q37: K8s 核心组件（Pod / Deployment / Service）？

- **难度**: 初级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. Pod：最小调度单位，含 1+ 容器
  2. Deployment：管理 Pod 副本和滚动更新
  3. Service：Pod 的稳定访问入口（负载均衡 + DNS）
  4. Ingress：7 层 HTTP 路由
  5. ConfigMap / Secret：配置管理

---

### Q38: Dockerfile 最佳实践？

- **难度**: 初级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 使用**多阶段构建**减小镜像
  2. 选择**alpine 基础镜像**
  3. **合并 RUN 命令**减少层数
  4. **`.dockerignore`** 排除无关文件
  5. **非 root 用户**运行（`USER 1000`）

---

### Q39: 监控 IaC 的关键指标

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. **Drift 率**：state 与实际不一致的频率
  2. **Apply 失败率**：CI/CD pipeline 成功率
  3. **State 锁等待时间**：并发冲突频率
  4. **资源数量趋势**：按 type/region 统计
  5. 告警：drift > 0、apply 失败、锁超时

---

### Q40: IaC 测试金字塔

- **难度**: 高级 | **频率**: 低频 ⭐⭐
- **答案要点**:
  1. **静态检查**（最便宜）：`tflint`, `tfsec`, `checkov`
  2. **单元测试**：模块单独测试
  3. **集成测试**：完整 apply + 验证
  4. **端到端测试**：真实环境测试
  5. **Policy as Code**：Sentinel / OPA 持续检查

---

## 四、云架构场景设计（10 题）

### Q41: 设计高可用 Web 架构

- **难度**: 高级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 多 AZ 部署（至少 2 个，可用区故障隔离）
  2. CLB 负载均衡 + 健康检查
  3. Auto Scaling 自动扩缩容
  4. 数据库主从 + 自动 failover
  5. Redis 缓存层
  6. CDN + COS 静态资源

---

### Q42: 设计跨区域灾备方案

- **难度**: 资深 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. **Pilot Light**：平时只运行核心组件，故障时快速启动
  2. **Warm Standby**：次区域跑小规模环境
  3. **Active-Active**：双写双活（成本最高）
  4. **RTO / RPO** 指标决定方案选型
  5. 数据库用**异地复制**（如 MySQL binlog replication、Redis CRR）

---

### Q43: 解释 IAM 最小权限原则

- **难度**: 中级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 用户/服务只给**必需的权限**
  2. IAM 策略：Action + Resource 限定
  3. Terraform 服务账号用 **OIDC + AssumeRole** 而非长寿命 AK
  4. 定期用 IAM Access Analyzer 审查
  5. 生产环境用**专用子账号 + 自定义策略**

---

### Q44: 设计成本监控方案

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. Terraform 标签（Project, Environment, Owner）便于成本分摊
  2. 预算告警（Budget Alerts）
  3. 定时任务销毁非生产环境
  4. 使用 Spot/Preemptible 实例
  5. 定期成本审计（Infracost, Terraform Cloud Cost Estimation）

---

### Q45: Terraform 资源出现循环依赖（circular dependency）怎么办？

- **难度**: 高级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 例：A 依赖 B，B 又依赖 A
  2. 解决方案：
     - **拆分资源**：将依赖拆为多层
     - 提取中间变量
     - 用 `lifecycle` 块
  3. 真实案例：Security Group 规则引用 SG 本身
  4. `terraform graph` 可视化依赖关系

---

### Q46: 解释 Terraform vs Pulumi vs Ansible vs CloudFormation

- **难度**: 高级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：声明式 + 多云 + state 文件，最流行
  - **Pulumi**：声明式但用真实编程语言（TypeScript/Python/Go）
  - **Ansible**：命令式，主机配置管理
  - **CloudFormation**：AWS only，与 Terraform 类似
  - 选择：多云→Terraform；AWS only→CFN；代码友好→Pulumi

---

### Q47: 大规模部署（100+ 资源）性能优化

- **难度**: 高级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. **拆分 state**：按服务或团队拆多个 state
  2. 用 `-target` 局部 apply
  3. `-parallelism` 控制并发数
  4. 模块化 + 复用变量
  5. 避免冗余的 `data source` 查询

---

### Q48: 如何用 Terraform 管理 K8s 资源？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 用 Kubernetes Provider
  2. 推荐 **Helm + Terraform** 或 **Helmfile**
  3. 生产级用 **ArgoCD / Flux** 做 GitOps
  4. Terraform 管**基础设施**（VPC、节点），K8s 管**应用层**

---

### Q49: Serverless 架构如何用 Terraform 管？

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 主流：腾讯云 SCF、AWS Lambda
  2. Terraform 用对应的云 provider
  3. 难点：API Gateway + Function + 事件源需要复杂编排
  4. 工具：Serverless Framework 配合 Terraform

---

### Q50: 混合云架构设计

- **难度**: 资深 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 跨云专线（如 AWS Direct Connect、腾讯云专线）
  2. Terraform **多 provider** 配置
  3. 统一身份认证（IAM Federation）
  4. 数据同步：跨云数据库复制
  5. 应用层：避免云厂商锁定

---

## 五、场景/排障/对比/行为（28 题）

### Q51: `terraform apply` 一直卡住，怎么办？

- **难度**: 初级 | **频率**: 中频 ⭐⭐⭐
- **出处**: Reddit r/Terraform 高频问题
- **答案要点**:
  1. 检查是否**死锁**：state 锁未释放
  2. 查 API 限流（429 Too Many Requests）→ 减小 `-parallelism`
  3. 查资源依赖：循环依赖
  4. 用 `TF_LOG=DEBUG` 看详细日志

---

### Q52: State 文件损坏了能恢复吗？

- **难度**: 高级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 有版本化 S3 → 回滚到上一个版本
  2. 无备份 → **灾难**：
     - 删 state，重新 `terraform import` 所有资源
     - 或手动重建基础设施（最后手段）
  3. **教训**：永远用远程 backend + 启用版本化 + 启用加密

---

### Q53: Drift 检测后发现资源被删除了，怎么办？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 不要慌，先 `terraform plan -refresh-only` 确认
  2. `terraform apply` 重建资源
  3. ⚠️ 注意：如果是数据库实例，重建后**数据丢失**
  4. **预防**：开启删除保护、备份策略、审计告警

---

### Q54: 多人同时 apply 导致冲突

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 必须用远程 backend + 锁（S3+DynamoDB、COS+自建锁）
  2. 锁冲突时，**等待**或**force-unlock**（谨慎）
  3. CI/CD 中串行 apply（不并发）
  4. 用 Atlantis/Terraform Cloud 集中执行

---

### Q55: `terraform destroy` 误删了重要资源，如何恢复？

- **难度**: 高级 | **频率**: 极高频 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 如果开启了 Remote Backend 版本化 → 回滚 state
  2. 用 `terraform import` 重新导入资源
  3. 如果是无状态资源 → 重新 apply
  4. **教训**：用 `prevent_destroy` 保护关键资源

---

### Q56: `terraform plan` 报错 "Error acquiring the state lock" 怎么办？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 检查是否有其他进程正在 apply
  2. 等几分钟再试
  3. 如果确认无人占用 → `terraform force-unlock <lock_id>`
  4. **获取 lock_id**：用 `terraform output` 或登录 S3/DynamoDB 查看

---

### Q57: module 引用的版本冲突怎么办？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 用 `terraform init -upgrade` 升级所有依赖
  2. 在 `required_versions` 锁定 Terraform 版本
  3. 在 `required_providers` 锁定 provider 版本
  4. 检查 `.terraform.lock.hcl` 看版本哈希

---

### Q58: `terraform apply` 创建了资源但 state 没更新（崩溃了）

- **难度**: 高级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  1. 下次 plan 会检测到实际资源存在，state 会同步更新
  2. 如果资源没创建成功 → 用 `terraform apply` 重试
  3. 如果资源部分创建 → 手动 `terraform state rm` 失败的资源，再 apply

---

### Q59: Terraform vs Ansible：什么时候用哪个？

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：基础设施编排（VM、网络、数据库）→ 声明式、跨云
  - **Ansible**：服务器配置、软件部署、运维自动化 → 命令式、无 agent
  - **组合**：Terraform 创建 VM → Ansible 配置应用
  - **典型工作流**：Terraform 起 EC2 → Ansible 装 Nginx

---

### Q60: Terraform vs CloudFormation

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：多云、HashiCorp 生态、社区大
  - **CloudFormation**：AWS 原生、AWS 资源覆盖最全、支持私有资源
  - 选择：只用 AWS 且需要 AWS 独有资源→CFN；多云或团队习惯→Terraform

---

### Q61: Terraform vs Pulumi

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：HCL DSL、学习曲线低、成熟生态
  - **Pulumi**：用 TypeScript/Python/Go 写 IaC、IDE 支持好、测试友好
  - 选择：开发者文化强→Pulumi；标准化、运维友好→Terraform

---

### Q62: count vs for_each 的真实生产陷阱

- **难度**: 中级 | **频率**: 高频 ⭐⭐⭐⭐
- **答案要点**:
  - **count 陷阱**：`var.servers = [A, B, C]` → 删除 B 变成 [A, C]，原 C 索引从 2 变成 1，**CVM 被销毁重建**
  - **for_each 优势**：用 key 标识（`name`），删除 B 后 C 保持不变
  - **最佳实践**：永远默认 `for_each`

---

### Q63: Terraform vs Helm（K8s 场景）

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  - Terraform 管**节点、LoadBalancer、存储**等基础设施
  - Helm 管**应用层**（Deployment、Service、ConfigMap）
  - 用 Terraform 部署 Helm chart（Helm provider）

---

### Q64: Terraform vs OpenTofu

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **出处**: HashiCorp/Mozilla 分叉事件后
- **答案要点**:
  - **OpenTofu**：2023 年因 HashiCorp 改协议，社区 fork 出的开源版本
  - **Terraform**：HashiCorp 维护，1.6+ 后 BSL 协议
  - 完全兼容 HCL 语法，大部分模块可互换
  - 选择：开源优先 → OpenTofu；商业支持 → Terraform Cloud/Enterprise

---

### Q65: Terraform state 存在哪里最安全？

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. **本地磁盘**：❌ 仅个人开发用，不安全
  2. **S3/COS + 加密 + 版本化**：✅ 推荐用于生产
  3. **Terraform Cloud**：✅ 官方托管，自动备份 + 审计
  4. **HashiCorp Consul/Vault**：✅ 企业级
  5. **绝不能**：Git、共享文件夹、未加密的云存储

---

### Q66: "Tell me about a Terraform outage you handled"

- **类型**: 行为面试（STAR 框架）
- **难度**: 中级~高级 | **频率**: 高频 ⭐⭐⭐⭐
- **建议答案结构**:
  - **S**ituation：某次生产事故
  - **T**ask：你的职责
  - **A**ction：用 Terraform 做了什么
  - **R**esult：恢复时间、影响、教训

---

### Q67: "How do you handle disagreement with a colleague about Terraform approach?"

- **类型**: 行为面试
- **建议答案**:
  - 关注**业务价值**而非个人偏好
  - 用 PoC 验证哪个方案更好
  - 参考 HashiCorp 最佳实践 + 团队实际约束

---

### Q68: "Walk me through your team's Terraform workflow"

- **类型**: 行为面试
- **建议答案**:
  - 目录结构 + 模块设计
  - CI/CD pipeline + 审批门禁
  - 环境隔离（dev/staging/prod）
  - 监控 + drift 检测

---

### Q69: "How do you onboard a new engineer to your Terraform codebase?"

- **类型**: 行为面试
- **建议答案**:
  - README + 架构图
  - 跑一遍 dev 环境 apply → destroy
  - 第一次 PR 配对编程
  - 文档化的检查清单

---

### Q70: "Tell me about a time you had to learn Terraform under pressure"

- **类型**: 行为面试
- **建议答案**:
  - 用 STAR 框架
  - 强调**学习能力**和**资源利用**（官方文档、社区、HashiCorp 论坛）

---

### Q71: "Describe a time you disagreed with your manager about a technical decision"

- **类型**: 行为面试
- **建议答案**:
  - 用 STAR 框架
  - 展示**沟通技巧**和**数据驱动决策**
  - 最终达成共识的过程

---

### Q72: "Tell me about a time you failed and how you recovered"

- **类型**: 行为面试
- **建议答案**:
  - 用 STAR 框架
  - 重点在**复盘和教训**
  - 展示**韧性**和**成长**

---

### Q73: "How do you stay current with new Terraform features?"

- **难度**: 中级 | **频率**: 低频 ⭐⭐
- **建议答案**:
  - 订阅 HashiCorp 官方博客和 release notes
  - GitHub 关注 terraform-providers 和 terraform
  - 参加 HashiConf（每年一次）
  - 定期看 Spacelift / Terraform Cloud 博客

---

### Q74: "How do you convince your team to adopt a new IaC practice?"

- **类型**: 行为面试
- **建议答案**:
  - 用**数据说话**（如 drift 率下降 90%）
  - 先**小范围试点**，成功后推广
  - 提供**培训和支持**
  - 与团队目标对齐

---

### Q75: "Describe your experience with Terraform Cloud / Enterprise"

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **建议答案**:
  - 如果用过：说具体功能（Remote Run、Policy as Code、Audit Logs）
  - 如果没用：说计划 + 对比自建方案

---

### Q76: "How do you handle Terraform when the cloud provider has no resource support?"

- **难度**: 高级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 用 `terraform_data` + provisioner 自定义资源
  2. 写自定义 Provider（Go 语言）
  3. 等社区贡献或提交 PR
  4. 用 `null_resource` 占位（已弃用）

---

### Q77: "What's your team's approach to Terraform module versioning?"

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. 用 Git tag（v1.0.0, v1.1.0）+ SemVer
  2. 通过 Terraform Registry 或私有 registry 分发
  3. 主项目用 `version = "~> 1.0"` 约束
  4. 每次模块变更发 CHANGELOG

---

### Q78: "How do you test infrastructure changes before applying to production?"

- **难度**: 中级 | **频率**: 中频 ⭐⭐⭐
- **答案要点**:
  1. **分层环境**：dev → staging → prod
  2. **PR 自动化**：每个 PR 跑 plan + tflint + tfsec
  3. **生产审批**：2 人 approve 才允许 apply
  4. **Plan 保存**：`terraform plan -out=tfplan` + 强制 apply 同 plan
  5. **回滚预案**：保留前一版本的 tfstate 备份

---

## 🎯 面试准备建议

### Q01-Q15：初级岗位 (0-2 年)
- 掌握 **A 类 15 题**（Terraform 基础）
- 熟读 HashiCorp 官方文档
- 搭建过完整 demo 项目（VPC + EC2 + DB）

### Q16-Q40：中级岗位 (3-5 年)
- 掌握 **A + B + C 类 40 题**
- 实际用过 **CI/CD + 远程 state + 模块化**
- 能独立设计多环境架构

### Q41-Q78：高级/资深岗位 (5+ 年)
- 掌握全部 **78 题**
- 有大规模生产环境经验（100+ 资源、跨 region、跨团队）
- 能设计**完整 IaC 治理体系**（Policy as Code、成本控制、审计）

### 备考推荐
1. **HashiCorp Certified Terraform Associate** 官方认证
2. 实践：[terraform-up-and-running](https://github.com/brikis98/terraform-up-and-running) 代码
3. 阅读：[Terraform: Up & Running](https://www.terraformupandrunning.com/) 第 3 版
4. 刷题：[Spacelift Blog](https://spacelift.io/blog/terraform-interview-questions) / [ProjectPro](https://www.projectpro.io/article/terraform-interview-questions-and-answers/850)

---

## 📚 来源汇总

- **Reddit**: r/devops, r/Terraform, r/devopsjobs, r/kubernetes
- **YouTube**: DevOps Pink（33K views）、in28minutes（266K subs）、TechWorld with Nana
- **Medium**: Tanishq Arora（SRE 真实面试经验）、Nidhi Ashtikar（51 道题）、Valdemar（10 道真实题）
- **DataCamp / ZeroToMastery / Simplilearn / GeeksforGeeks**: 面试题库
- **HashiCorp 官方**: Associate 004 样题
- **ByteByteGo**: 架构设计相关内容
- **Google SRE Book**: SLI/SLO/Toil 概念

---

*最近更新：2025 年 | 共 78 题 | 覆盖初/中/高级岗位*
*题目编号规则：Q01-Q78，按文档顺序排列*
