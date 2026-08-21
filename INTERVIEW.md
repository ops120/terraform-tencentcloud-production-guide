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
1. **主答案**仅供参考答题框架和关键词
2. **追问答案**是基于常见经验的参考，请务必自己测试/验证
3. **面试前**：用自己的话复述，能讲出实战案例 > 背答案
4. **核对方式**：官方文档 > 官方认证题库 > HashiCorp 博客
5. 标 ✅ 的答案 = 高置信度（如官方文档明示），其他 = 常见经验


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

- **难度**: 初级
- **频率**: ⭐⭐⭐⭐⭐
- **出处**: Reddit, Glassdoor, YouTube, DataCamp
- **答案要点**:
  1. Terraform 是 HashiCorp 的**声明式（declarative）IaC 工具**，专注基础设施**编排（orchestration）**
  2. Ansible 是**命令式（imperative）配置管理工具**，专注**配置（configuration management）**
  3. Terraform 自动计算**依赖图**；Ansible 按步骤顺序执行
  4. Terraform 有 **state 文件**跟踪资源；Ansible 无状态
  5. Terraform **多云支持**；Ansible 侧重服务器配置
- **追问**: "Terraform 和 Ansible 能配合使用吗？" / "两者的幂等性有什么区别？"

- **追问与参考答案（参考，未验证）**:
  - **Terraform 和 Ansible 能配合使用吗？**: 可以。典型模式：用 Terraform 创建云资源（VM、网络、数据库），用 Ansible 在创建好的 VM 上安装软件和配置。也有 `ansible` provider 可以从 Terraform 调用 Ansible。
  - **两者的幂等性有什么区别？**: 两者都是幂等的——重复执行同样的命令，最终状态相同。Terraform 的幂等来自 state 对比，Ansible 的幂等来自模块自身的检查（如 `apt` 模块会先看包是否已装）。

---

### Q02: Terraform state 文件是什么？为什么它如此重要？

- **难度**: 初级 ⭐⭐⭐⭐⭐
- **出处**: Reddit r/Terraform, HashiCorp 认证题, YouTube, Medium
- **答案要点**:
  1. `terraform.tfstate` 记录云资源 ID 和属性，建立代码与实际资源的映射
  2. 支持**增量更新**：plan 比对 state 和代码
  3. **绝不能提交到 Git**（含敏感信息如 IP、密钥）
  4. 团队协作必须用**远程 state + 锁**
  5. State 丢失 = Terraform 不认识资源，会尝试重建导致冲突
- **追问**: "State 丢失怎么办？" / "如何团队共享 state？"

- **追问与参考答案（参考，未验证）**:
  - **State 丢失怎么办？**: 灾难。需要：用 `terraform import` 重新导入所有资源（最稳妥），或从版本化的 remote backend 恢复 state。教训：必须开启 backend 版本化和备份。
  - **如何团队共享 state？**: 用 Remote Backend（S3+COS+锁），团队所有成员 `terraform plan/apply` 都连到同一个远程 state。强烈不要把 state 文件放在共享文件夹或 Git 里。

---

### Q03: Terraform provider 是什么？如何工作？

- **难度**: 初级 ⭐⭐⭐⭐
- **出处**: Reddit, HashiCorp 认证, DataCamp
- **答案要点**:
  1. Provider 是**插件**，通过 Terraform Plugin Protocol 与云 API 通信
  2. `terraform init` 下载 provider 到 `.terraform/` 目录
  3. `.terraform.lock.hcl` 锁定 provider 版本和哈希
  4. 一个配置文件可使用多个 provider（如 `provider "aws" { alias = "east" }`）
  5. 编写自定义 provider 需要 Go 语言

- **追问与参考答案（参考，未验证）**:
  - **如何升级 Provider 版本？**: 修改 `required_providers` 块的 version 约束（如 `version = "~> 1.81"`），运行 `terraform init -upgrade`。但建议先在 dev 环境验证，避免大版本升级的 breaking change。
  - **Provider 是开源的吗？**: 大部分主流云厂商的 Provider 都是开源的（GitHub 上能找到），但 HashiCorp 自己维护的 Provider（如 `random`, `archive`）和云厂商的 Provider 分工不同。

---

### Q04: resource 和 data source 有什么区别？

- **难度**: 初级 ⭐⭐⭐⭐
- **答案要点**:
  1. `resource`：**创建 / 管理**资源（CRUD）
  2. `data source`：**只读查询**现有资源（如查询 AMI ID、可用的 AZ）
  3. Data source 不在 state 中保存属性
  4. 使用场景：DRY 原则、避免硬编码、查询动态值

- **追问与参考答案（参考，未验证）**:
  - **Data source 能在 module output 里返回吗？**: 可以，但有限制。某些 data source 可能在 apply 阶段才能拿到值，module 间的传递会出错。推荐在 module 内部完成 data source 查询。
  - **Data source 在 plan 阶段会查询 API 吗？**: 会。每次 `terraform plan` 都会查询 data source（除非加了 `count` 或 `for_each` 条件）。大量 data source 会拖慢 plan 速度。

---

### Q05: Module 是什么？和直接写 resource 有什么区别？

- **难度**: 初级 ⭐⭐⭐⭐
- **答案要点**:
  1. Module 是**可复用的资源组**，封装多个 resource
  2. 输入（variables）+ 输出（outputs）+ 实现（main.tf）
  3. 支持版本管理（Git tag / Registry）
  4. **何时用**：资源超过 3 个、多团队复用、跨环境共享
  5. **何时不用**：单个文件、一次性部署

- **追问与参考答案（参考，未验证）**:
  - **模块版本升级时如何做向后兼容？**: 遵循 SemVer：patch 版本只修 bug，minor 版本新增功能（向后兼容），major 版本可能 breaking change。永远不要在 minor/patch 版本里改破坏性行为。
  - **如何测试一个模块？**: 用 `examples/` 目录提供多个示例；用 Terratest（Go 测试框架）写集成测试；在 CI 中自动跑 `terraform plan`/`apply`/`destroy` 验证。

---

### Q06: Backend 是什么？和 local 有什么区别？

- **难度**: 初级 ⭐⭐⭐⭐
- **答案要点**:
  1. Backend 决定 **state 文件存储位置**和执行方式
  2. Local（默认）：state 存在本地磁盘；Remote（S3/COS/Terraform Cloud）：state 存在云端 + 自动锁
  3. 团队协作**必须用 Remote Backend**
  4. `partial-configuration` 通过 `-backend-config` 传入参数
  5. Terraform Cloud 还提供远程执行、Plan 审计、Policy 检查

- **追问与参考答案（参考，未验证）**:
  - **backend 切换时如何迁移 state？**: 先用 `terraform init -migrate-state`，Terraform 会把 state 从旧 backend 复制到新 backend 并删除旧的。注意：需要在 backend 块里同时声明 `backend "old" {}` 作为临时源。
  - **Terraform Cloud 是什么？**: HashiCorp 官方提供的 SaaS 平台，提供 Remote Backend、远程执行（Terraform Cloud 执行 apply）、Policy as Code（Sentinel）、私有模块 Registry、审计日志。免费额度够小团队用。

---

### Q07: 解释 Terraform 的 lifecycle（生命周期）块

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. `create_before_destroy`：先创建新资源再删旧的（避免 downtime）
  2. `prevent_destroy`：防止误删关键资源（如数据库）
  3. `ignore_changes`：忽略某些属性变化（如自动生成的密码）
  4. `replace_triggered_by`：强制替换资源
  5. lifecycle 是 Terraform 中**保护重要资源**的关键

- **追问与参考答案（参考，未验证）**:
  - **ignore_changes 具体怎么用？**: 示例：`lifecycle { ignore_changes = [tags["LastModified"], ami_id] }`。常用于忽略自动变化的属性（如时间戳、AMI ID 自动更新）。
  - **create_before_destroy 对所有资源都适用吗？**: 不是。有些资源不支持（如 IAM 角色名冲突），或者需要先删后建（如替换证书）。需要在实践中验证。

---

### Q08: Terraform 变量有哪些类型？sensitive 是什么？

- **难度**: 初级 ⭐⭐⭐
- **答案要点**:
  1. 类型：`string`, `number`, `bool`, `list`, `map`, `set`, `object`, `tuple`
  2. `sensitive = true`：标记为敏感，**plan/apply 输出会隐藏**，但**State 中仍明文存储**
  3. **真正安全**的做法：环境变量 + SSM/KMS + Remote Backend 加密
  4. variable 还可以有 `default`, `validation`, `nullable`

- **追问与参考答案（参考，未验证）**:
  - **sensitive 变量和标记为 sensitive 的 output 有什么区别？**: 效果类似：plan/apply 输出会隐藏。但两者都不会加密 state 文件本身，需要在 backend 层加密（S3 SSE、KMS）。
  - **object 和 tuple 区别？**: object 有字段名（`{name = string, age = number}`），tuple 按位置（`[string, number]`）。前者更像 JSON 对象，后者更像元组。

---

### Q09: 解释 Terraform 常用命令

- **难度**: 初级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. `init`：下载 provider + 初始化 backend
  2. `plan`：预览变更（不实际执行）
  3. `apply`：执行变更
  4. `destroy`：销毁资源
  5. `fmt`：格式化代码，`validate`：语法检查，`state list/show/rm/mv`：操作 state

- **追问与参考答案（参考，未验证）**:
  - **terraform validate 和 terraform fmt 区别？**: `fmt` 重新格式化代码风格（缩进、空行），`validate` 检查语法和类型错误。两者都不连云。
  - **terraform refresh 命令是什么？**: 把云上资源的最新状态同步到本地 state。1.6+ 后 `plan -refresh-only` 取代了它的常见用途，避免误操作覆盖 state。

---

### Q10: Terraform 如何处理资源依赖？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. **隐式依赖**：通过变量引用（如 `vpc_id = aws_vpc.main.id`）
  2. **显式依赖**：`depends_on = [aws_iam_role.example]`
  3. Terraform 自动构建**依赖图**，按顺序执行
  4. `create_before_destroy` 会改变依赖方向

- **追问与参考答案（参考，未验证）**:
  - **depends_on 会拖慢速度吗？**: 不会拖慢速度本身，但会改变执行顺序，可能让本来可以并行的资源变成串行。
  - **怎么查看资源依赖图？**: 用 `terraform graph | dot -Tpng > graph.png` 生成 PNG 图片，或装 Graphviz 后 `terraform graph | display`。

---

### Q11: 什么是 Terraform Registry？如何使用？

- **难度**: 初级 ⭐⭐⭐
- **答案要点**:
  1. Registry 是**公共模块库**（registry.terraform.io）
  2. 引用方式：`module "vpc" { source = "terraform-aws-modules/vpc/aws" version = "5.0.0" }`
  3. 私有的可以用 GitHub/GitLab + `git::https://...`
  4. 内部公司可搭建**私有 Registry**（如 Terraform Cloud Private Registry）

- **追问与参考答案（参考，未验证）**:
  - **Registry 模块和 Git 私有模块哪个好？**: Registry 模块有版本号、签名、自动文档，更安全；Git 模块灵活但需要自己管理版本和发布流程。生产推荐 Registry。
  - **内部如何搭建私有 Registry？**: 可以用 Terraform Cloud Private Registry、GitLab 内置 Module Registry、或自建工具（如 terraform-registry-server）。

---

### Q12: 什么是 HCL？和 JSON/YAML 比有什么优势？

- **难度**: 初级 ⭐⭐
- **答案要点**:
  1. HCL = HashiCorp Configuration Language，**专为 IaC 设计**
  2. JSON 太严格（无注释、无变量），YAML 缩进易错、复杂嵌套难读
  3. HCL 支持**表达式、函数、注释、块结构**
  4. JSON 是 Terraform 的"备份格式"（`.tf.json`），机器生成用
  5. HCL 5 引入新特性（如 `import` block、`optional()` 等）

- **追问与参考答案（参考，未验证）**:
  - **HCL 的可选类型是什么？**: HCL 2.0+ 支持 `optional(type)`，表示变量可以为 null。还有 `nullable = false` 强制非空。
  - **HCL 支持哪些高级特性？**: 支持 `for` 表达式、`splat`、函数式编程（如 `merge`、`lookup`）、`try` 错误处理、动态块。

---

### Q13: provisioner 是什么？什么时候用？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. Provisioner 在资源创建后执行**自定义逻辑**（脚本、文件传输）
  2. 类型：`local-exec`, `remote-exec`, `file`
  3. ⚠️ **最后手段**：state 无法跟踪 provisioner 执行结果
  4. 优先用 `user_data`（云初始化脚本）或自定义镜像
  5. 失败处理：`on_failure = continue`（不推荐）

- **追问与参考答案（参考，未验证）**:
  - **provisioner 失败后 Terraform 会回滚吗？**: 不会。Terraform 不管理 provisioner 创建的资源。如果 `remote-exec` 失败，VM 已创建但脚本没跑完，state 会卡住。建议用 `user_data` 或自定义镜像。
  - **null_resource 是什么？**: 一个不创建任何资源的虚拟资源，专门用于触发 provisioner。1.4+ 推荐用 `terraform_data` 替代。

---

### Q14: 如何管理敏感信息（数据库密码、API Key）？

- **难度**: 中级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. ❌ 错误：硬编码在 `.tf` 文件或 `terraform.tfvars` 提交到 Git
  2. ✅ 推荐：**环境变量**（`TF_VAR_db_password`）
  3. 生产级：**SSM/KMS/Secrets Manager** + IAM 角色
  4. 用 `sensitive = true` 标记变量（仅隐藏输出，不加密 state）
  5. 远程 Backend 必须加密（S3 启用 server-side encryption）

- **追问与参考答案（参考，未验证）**:
  - **如果不小心把敏感信息提交到 Git 怎么办？**: 立即轮换密钥！删除 Git 历史（`git filter-repo`），清理 GitHub 缓存（联系 GitHub Support），检查云厂商账单是否有异常。
  - **Vault 是什么？怎么集成？**: HashiCorp Vault 是 secrets 管理工具。Terraform 有 Vault provider，可以从 Vault 读取 secrets 作为变量值。

---

### Q15: Terraform 的 "Plan" 输出符号 `+/-/~` 什么意思？

- **难度**: 初级 ⭐⭐⭐⭐
- **答案要点**:
  1. `+ create`：新建资源
  2. `- destroy`：删除资源
  3. `~ update in-place`：就地修改（部分属性变化）
  4. `-/+ destroy and create`：替换资源（先删后建）
  5. `+/- create before destroy`：先建后删
  6. `# module.xxx`：模块内的资源

- **追问与参考答案（参考，未验证）**:
  - **plan 为什么不直接 apply？**: plan 只读，apply 才会实际改云。这样可以先看变更内容，避免误删。生产环境必备。
  - **怎么让 plan 自动 approve？**: CI/CD 中可以 `terraform apply -auto-approve`，但生产环境**绝对禁止**，必须人工审批。

---

## 二、Terraform 进阶（15 题）

### Q16: 什么是 State Locking？为什么需要？

- **难度**: 中级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 防止**多人同时 apply** 导致的 state 冲突
  2. S3 用 DynamoDB 锁；Terraform Cloud 自动锁；Azure 用 blob lease
  3. 锁未释放（CI 崩溃）：用 `terraform force-unlock <lock_id>`
  4. 锁 ID 通过 `terraform output` 或日志查看
  5. **不要在 CI 中禁用锁**（race condition 灾难）

- **追问与参考答案（参考，未验证）**:
  - **force-unlock 的风险？**: 如果另一个进程真的在 apply 中，强制解锁可能导致两人同时改 state，结果是 state 文件冲突（JSON 损坏）。必须先确认无人占用。
  - **锁的 TTL 是多长？**: S3+DynamoDB 默认没有 TTL（永久锁），靠手动 force-unlock。Terraform Cloud 默认有 30 分钟 TTL。

---

### Q17: Drift 是什么？如何检测和修复？

- **难度**: 中级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. Drift = State 记录与**实际云资源**不一致（有人改了控制台）
  2. 检测：`terraform plan -refresh-only` 或普通 `terraform plan`
  3. 修复：
     - 接受实际：`terraform apply` 让代码匹配云
     - 接受代码：`terraform refresh` 更新 state
  4. 预防：开启 CloudTrail 审计、IAM 权限最小化、Terraform 管理所有变更

- **追问与参考答案（参考，未验证）**:
  - **如何在 CI 中自动检测 drift？**: 每天定时跑 `terraform plan -detailed-exitcode`（有 drift 返回 2），发到 Slack 告警。Atlantis 和 Terraform Cloud 都有这个功能。
  - **Drift 是坏的吗？**: 不一定是坏的。如果有人手动扩容了 CVM 但忘了更新 Terraform，这是好的 drift。但意外的删除就是坏 drift，需要立即修复。

---

### Q18: `terraform import` 和 `import block` 的区别？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. `terraform import` (CLI, 1.5 之前)：导入到 state 但**不写代码**
  2. `import { to = ... id = ... }` block (1.5+)：**同时写 state 和生成代码**（`-generate-config-out`）
  3. 使用场景：迁移控制台已有资源到 Terraform 管理
  4. 需要先在 `.tf` 中**声明资源骨架**才能 import

- **追问与参考答案（参考，未验证）**:
  - **import block 的限制是什么？**: 只能导入到 state，不能导入已经存在的依赖关系；某些复杂资源（如 K8s CRD）可能需要手动写配置。
  - **如何批量 import？**: 用脚本循环遍历资源 ID，生成 `terraform import` 命令。或写 `for_each` + `import` block 数组。

---

### Q19: Workspace 和 directory-per-environment 哪个好？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. **Workspaces**：共享代码，仅 state 隔离。适合差异极小的小团队
  2. **Directory-per-environment**：完全独立目录 + state。推荐用于**生产**
  3. Workspaces 缺点：plan 输出混乱、权限隔离差、变量管理复杂
  4. 推荐：**生产用目录隔离**，workspaces 仅用于短生命周期的临时环境

- **追问与参考答案（参考，未验证）**:
  - **Workspaces 适合什么场景？**: 短生命周期的临时环境（如 PR 预览环境）、演示环境。不适合生产。
  - **Workspaces 如何切换？**: `terraform workspace select prod` 切换后，后续命令都在该 workspace 下执行。State 文件路径会加上 workspace 名前缀。

---

### Q20: `count` vs `for_each` 区别？陷阱是什么？

- **难度**: 中级 ⭐⭐⭐⭐⭐（高频陷阱题）
- **答案要点**:
  1. `count`：索引创建相同资源，用 `count.index`
  2. `for_each`：从 Map/Set 创建，用 `each.key` / `each.value`
  3. **count 陷阱**：删除中间元素会**重建所有后续资源**（index 变了）
  4. for_each 用 key 作为标识，删除元素不影响其他
  5. **最佳实践**：默认用 `for_each`，仅当需条件创建时用 `count`

- **追问与参考答案（参考，未验证）**:
  - **for_each 支持哪些类型？**: Map 或 Set。List 不行（因为 list 索引会变化，导致同样的 count 陷阱）。需要把 list 转成 set（`toset(var.servers)`）。
  - **count 和 for_each 能混用吗？**: 可以，但不推荐。混用会让依赖关系混乱，建议一个资源只用一种方式。

---

### Q21: 远程 State 后端有哪些选择？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. AWS S3 + DynamoDB（最流行）
  2. **腾讯云 COS + 自建锁**（教程中提到）
  3. Azure Storage + Blob Lease
  4. GCS + Lockfile
  5. Terraform Cloud（官方托管，自带锁、Policy、审计）
  6. **Backend 必须支持锁定**，否则不能用

- **追问与参考答案（参考，未验证）**:
  - **自建 lock（如 COS）可靠吗？**: 没有 S3+DynamoDB 那么成熟，需要自己保证强一致性。教程里用的是腾讯云 CAM 权限 + 对象锁机制，可以工作但不推荐用于大规模生产。
  - **如何降低 Remote Backend 成本？**: S3 用 lifecycle 策略清理旧版本；COS 用归档存储；Terraform Cloud 免费额度对 5 人以下团队够用。

---

### Q22: `prevent_destroy` 有什么用？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. 防止 `terraform destroy` 删除关键资源（如生产数据库）
  2. 写在 lifecycle 块：`lifecycle { prevent_destroy = true }`
  3. ⚠️ 但不能阻止**手动控制台删除**
  4. 配合 IAM 权限 + CloudTrail 才能真正保护

- **追问与参考答案（参考，未验证）**:
  - **prevent_destroy 如何临时禁用？**: 没有临时禁用，要么移除 lifecycle 块后 apply，要么用 `terraform state rm` 移出 state（极端情况）。生产用 CI 检查防止误移除。
  - **prevent_destroy 配合什么用？**: 配合 IAM 权限（即使手动控制台删除也需要 MFA）和 CloudTrail 审计。

---

### Q23: `taint` 和 `-replace` 有什么区别？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. `terraform taint`：标记资源为"已污染"，下次 apply 会**重建**
  2. `terraform apply -replace="..."` (1.6+)：plan 时直接替换，无需 taint
  3. 用途：机器坏了强制重建
  4. taint 已**部分弃用**，推荐 `-replace`

- **追问与参考答案（参考，未验证）**:
  - **taint 之后怎么解除？**: `terraform untaint <resource>` 解除。但 1.6+ 推荐用 `-replace`，更直观。
  - **taint 和 destroy 区别？**: taint 标记后下次 apply 会 destroy + create（中间有短暂不可用）；destroy 直接删除资源，state 中也删除。

---

### Q24: `moved` block 是什么？

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. 用于**资源重命名**而不销毁重建
  2. 写法：`moved { from = aws_instance.old to = aws_instance.new }`
  3. 适用：模块重构后资源地址变化
  4. 替代了之前的 `terraform state mv`

- **追问与参考答案（参考，未验证）**:
  - **moved block 适用版本？**: 1.1+ 支持。比 `terraform state mv` 更优雅（可以写进 PR review）。
  - **moved block 跨模块怎么写？**: `moved { from = module.old.aws_instance.foo to = module.new.aws_instance.foo }`，模块路径会变化。

---

### Q25: `dynamic` block 是什么？

- **难度**: 高级 ⭐⭐
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

- **追问与参考答案（参考，未验证）**:
  - **dynamic block 有什么限制？**: 生成的资源类型必须一致；for_each 必须遍历 Map/Set；content 块内的语法和静态块相同。
  - **什么时候用 dynamic 而不是 for_each？**: 当同一资源的嵌套块需要动态生成时（如 SG 规则），用 `dynamic`。当需要创建多个独立资源时，用 `for_each`。

---

### Q26: 如何调试 Terraform 代码？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. `TF_LOG=DEBUG terraform apply` 查看详细日志
  2. `TF_LOG_PATH=./log.txt` 输出到文件
  3. 日志级别：`TRACE` > `DEBUG` > `INFO` > `WARN` > `ERROR`
  4. `terraform console`：交互式测试表达式

- **追问与参考答案（参考，未验证）**:
  - **TF_LOG=TRACE 有多详细？**: 极其详细，包含 HTTP 请求、Provider 调用、SQL（如果有）。可能产生 GB 级日志，只在排错时临时开。
  - **terraform console 怎么用？**: 进入交互式 REPL，可以测试表达式：`> var.instance_type`，输出 `"S5.LARGE8"`。

---

### Q27: 如何升级 Terraform 版本？升级有风险吗？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. 升级 Terraform 二进制本身（直接下载新版）
  2. 升级 Provider 版本（修改 `required_providers`）
  3. ⚠️ 风险：Provider 大版本升级可能引入 breaking change
  4. 用 `terraform init -upgrade` 升级 lock 文件
  5. **测试流程**：dev → staging → prod 逐步升级

- **追问与参考答案（参考，未验证）**:
  - **Terraform 大版本升级怎么测试？**: 在 dev 环境用 `terraform init -upgrade` 升级，跑完整 plan 看是否有 breaking change（标 `~` 或 `-/+`），有问题先改代码再升生产。
  - **Provider major 版本如何测试？**: 先在单独分支升级，跑 plan 看变更；用 `terratest` 跑集成测试；灰度环境验证。

---

### Q28: 解释 `for` 表达式和 `for_each` 的区别

- **难度**: 中级 ⭐⭐
- **答案要点**:
  1. `for` 表达式：**转换数据**（类似 list comprehension）
  2. `for_each`：**资源创建**（生成多个资源）
  3. 示例：`[for s in var.servers : s.name]` 是表达式，`for_each = var.servers` 是资源块

- **追问与参考答案（参考，未验证）**:
  - **for 表达式能用在 output 里吗？**: 可以。`output "names" { value = [for s in var.servers : s.name] }`。
  - **for 表达式的 in 后能用什么？**: List、Map、Set 都可以。Map 返回的是 value，List/Set 返回的是元素。

---

### Q29: `dynamic` 和 `for_each` 的区别？

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. `for_each` 创建**多个资源实例**
  2. `dynamic` 在**单个资源内**动态生成嵌套块
  3. 例如：`for_each` 创建多个 `aws_security_group`，`dynamic` 在一个 SG 内动态生成多个 `ingress` 规则

- **追问与参考答案（参考，未验证）**:
  - **dynamic block 在 output 里能引用吗？**: 不能直接引用 `dynamic` 块本身，但可以引用 `dynamic` 块创建的资源的属性。
  - **dynamic 和 count 在同一资源里能混用吗？**: 可以但非常复杂，不推荐。

---

### Q30: 如何测试 Terraform 代码？

- **难度**: 高级 ⭐⭐⭐⭐
- **答案要点**:
  1. **静态检查**：`terraform validate`, `tflint`, `tfsec`, `checkov`
  2. **单元测试**：`terraform test`（1.6+ 原生）
  3. **集成测试**：Terratest（Go 库）
  4. **端到端测试**：在临时 AWS 账号中 apply → 验证 → destroy
  5. 接入 CI：每个 PR 自动跑测试

- **追问与参考答案（参考，未验证）**:
  - **terraform test 怎么写？**: 在 `.tftest.hcl` 文件里写测试用例，类似 Go 测试。`run "test" { command = plan }` 测试 plan 是否符合预期。
  - **CI 中测试 Terraform 的最佳实践？**: 每 PR：fmt → validate → tflint → tfsec → checkov → plan → test（如果有）。

---

## 三、DevOps / SRE 综合（10 题）

### Q31: Terraform 如何集成到 CI/CD？

- **难度**: 高级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. Pipeline：`init` → `fmt -check` → `validate` → `tflint/tfsec` → `plan` → 审批 → `apply`
  2. **生产环境 apply 必须人工审批**（2 人 approve）
  3. Plan artifact 保存到 S3 或 GitHub artifacts
  4. 使用 OIDC（避免长寿命 AK/SK）
  5. 集成 Slack/Teams 通知失败

- **追问与参考答案（参考，未验证）**:
  - **Plan artifact 怎么用？**: `terraform plan -out=tfplan` 保存 plan 文件到磁盘，CI 保存到 S3 artifact，审批后 apply 同一 plan（避免 drift 导致 apply 不同的变更）。
  - **如何防止 plan 过期？**: Plan 应该在短时间内 apply（几小时内），超过 24 小时建议重新 plan。CI/CD 中可加超时检查。

---

### Q32: 解释 GitOps 和 Terraform 的结合

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. GitOps = Git 作为唯一真相源
  2. PR 修改 Terraform 代码 → CI 跑 plan → merge → 自动 apply
  3. 工具：ArgoCD、Flux（用于 K8s）；Terraform Cloud 直接支持
  4. 优势：审计、可回滚、可追溯

- **追问与参考答案（参考，未验证）**:
  - **Terraform Cloud 和 ArgoCD 区别？**: 前者管 Terraform（基础设施），后者管 K8s（应用）。可以配合使用：ArgoCD 触发 Terraform Cloud 的 plan/apply。
  - **GitOps 的 rollback 怎么做？**: Git revert 到上一个 commit → CI 自动 apply → 基础设施回滚。但 state 文件可能漂移，需要 `terraform plan -refresh-only` 检查。

---

### Q33: SLI / SLO / SLA 是什么？

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. SLI（指标）：如延迟、错误率、吞吐量
  2. SLO（目标）：如 99.9% 可用率
  3. SLA（协议）：与客户的承诺，未达成要赔偿
  4. SLO ≤ SLA，建议预留 buffer
  5. Error Budget：SLO 100% - 99.9% = 0.1% 不可用时间

- **追问与参考答案（参考，未验证）**:
  - **Error Budget 耗尽了怎么办？**: 暂停新功能上线，所有工程资源都投入稳定性修复，直到 budget 恢复（下一个计费周期）。
  - **SLI 如何选择？**: 用户能感知的指标：延迟（p99）、错误率（5xx 比例）、可用性（成功请求/总请求）。

---

### Q34: 蓝绿 / 滚动 / 金丝雀部署区别？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. **蓝绿**：两套环境，切流量（快速回滚，但资源 2 倍）
  2. **滚动**：逐步替换实例（K8s 默认，节省资源但回滚慢）
  3. **金丝雀**：少量流量验证新版本（最安全，但复杂）
  4. Terraform + Auto Scaling Group 适合滚动部署

- **追问与参考答案（参考，未验证）**:
  - **金丝雀部署如何自动化？**: 用 Argo Rollouts、Flagger 或 Spinnaker。先把 5% 流量切到新版本，观察 metrics，逐步增加比例。
  - **Terraform 支持蓝绿部署吗？**: 支持。用 `aws_route53_record` 切换 DNS 权重，或用 ALB 的两个 Target Group 切换。

---

### Q35: 什么是不可变基础设施（Immutable Infrastructure）？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. 服务器部署后**不再修改**，更新只通过替换实例
  2. 优势：可预测、易回滚、避免配置漂移
  3. Terraform 实现：`create_before_destroy` + AMI
  4. 对比：可变基础设施（SSH 进去改配置）= 反模式

- **追问与参考答案（参考，未验证）**:
  - **不可变基础设施和容器的关系？**: 容器本身就是不可变的（image 一旦构建就不变）。EC2 也可以做到：用 Packer 构建 AMI，每次更新替换整个实例。
  - **Packer 是什么？**: HashiCorp 的镜像构建工具，和 Terraform 配合：Packer 构建 AMI → Terraform 用 AMI 创建 EC2。

---

### Q36: 解释 Toil（运维苦差事）

- **难度**: 中级 ⭐⭐⭐
- **出处**: Google SRE Book
- **答案要点**:
  1. Toil = 手动、重复、可自动化、无长期价值的运维工作
  2. SRE 原则：运维工作**不超过 50%** toil
  3. Terraform / Ansible 是减少 toil 的核心工具
  4. 衡量：每次操作的人工小时数

- **追问与参考答案（参考，未验证）**:
  - **如何衡量 toil？**: 记录每个运维任务的人工小时数，统计月度趋势。SRE 团队目标：toil ≤ 50% 工作时间。
  - **Toil 和技术债有什么区别？**: Toil 是重复性手动工作（如重启服务），技术债是代码/架构的妥协。Toil 是症状，技术债是原因之一。

---

### Q37: K8s 核心组件（Pod / Deployment / Service）？

- **难度**: 初级 ⭐⭐⭐⭐
- **答案要点**:
  1. Pod：最小调度单位，含 1+ 容器
  2. Deployment：管理 Pod 副本和滚动更新
  3. Service：Pod 的稳定访问入口（负载均衡 + DNS）
  4. Ingress：7 层 HTTP 路由
  5. ConfigMap / Secret：配置管理

- **追问与参考答案（参考，未验证）**:
  - **Pod 和 Container 区别？**: Pod 是 K8s 调度单位，可以包含 1+ 紧密相关的容器（如 app + sidecar）。Container 是镜像实例。
  - **Deployment 和 StatefulSet 区别？**: Deployment 适合无状态服务，StatefulSet 适合有状态服务（如数据库），有稳定的网络标识和持久存储。

---

### Q38: Dockerfile 最佳实践？

- **难度**: 初级 ⭐⭐⭐
- **答案要点**:
  1. 使用**多阶段构建**减小镜像
  2. 选择**alpine 基础镜像**
  3. **合并 RUN 命令**减少层数
  4. **`.dockerignore`** 排除无关文件
  5. **非 root 用户**运行（`USER 1000`）

- **追问与参考答案（参考，未验证）**:
  - **Alpine 镜像有什么坑？**: Alpine 用 musl libc 而不是 glibc，某些二进制（如 Python wheels）可能不兼容。需要测试。
  - **为什么用多阶段构建？**: 构建阶段包含完整工具链（如 gcc、npm），运行时阶段只复制产物（如编译好的二进制）。最终镜像可以小 10 倍以上。

---

### Q39: 监控 IaC 的关键指标

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. **Drift 率**：state 与实际不一致的频率
  2. **Apply 失败率**：CI/CD pipeline 成功率
  3. **State 锁等待时间**：并发冲突频率
  4. **资源数量趋势**：按 type/region 统计
  5. 告警：drift > 0、apply 失败、锁超时

- **追问与参考答案（参考，未验证）**:
  - **Drift 率怎么计算？**: `(drift 资源数 / 总资源数) * 100%`。建议 < 1%，> 5% 需要告警。
  - **Terraform apply 失败怎么监控？**: CI/CD pipeline 上报 metrics 到 Prometheus，统计失败率。失败 > 5% 告警。

---

### Q40: IaC 测试金字塔

- **难度**: 高级 ⭐⭐
- **答案要点**:
  1. **静态检查**（最便宜）：`tflint`, `tfsec`, `checkov`
  2. **单元测试**：模块单独测试
  3. **集成测试**：完整 apply + 验证
  4. **端到端测试**：真实环境测试
  5. **Policy as Code**：Sentinel / OPA 持续检查

- **追问与参考答案（参考，未验证）**:
  - **Sentinel 和 OPA 区别？**: Sentinel 是 HashiCorp 的 Policy 框架（Terraform Cloud 内置），OPA 是 CNCF 的通用 Policy 框架（更灵活，但集成复杂）。
  - **如何写自定义 Policy？**: Sentinel 用 `.sentinel` 文件，OPA 用 Rego 语言。两者都支持 deny/allow 规则。

---

## 四、云架构场景设计（10 题）

### Q41: 设计高可用 Web 架构

- **难度**: 高级 ⭐⭐⭐⭐
- **答案要点**:
  1. 多 AZ 部署（至少 2 个，可用区故障隔离）
  2. CLB 负载均衡 + 健康检查
  3. Auto Scaling 自动扩缩容
  4. 数据库主从 + 自动 failover
  5. Redis 缓存层
  6. CDN + COS 静态资源

- **追问与参考答案（参考，未验证）**:
  - **多 AZ 部署就够高可用了吗？**: 单 region 多 AZ 够 99.99% 可用性。要 99.999% 需要多 region + 异地容灾。
  - **Auto Scaling 缩容到 0 会怎样？**: 会完全停止所有实例，导致服务不可用。生产环境建议设置 `min_size >= 2`。

---

### Q42: 设计跨区域灾备方案

- **难度**: 资深 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. **Pilot Light**：平时只运行核心组件，故障时快速启动
  2. **Warm Standby**：次区域跑小规模环境
  3. **Active-Active**：双写双活（成本最高）
  4. **RTO / RPO** 指标决定方案选型
  5. 数据库用**异地复制**（如 MySQL binlog replication、Redis CRR）

- **追问与参考答案（参考，未验证）**:
  - **Pilot Light 和 Warm Standby 选哪个？**: 看 RTO 要求：Pilot Light 适合 RTO > 1 小时（成本最低），Warm Standby 适合 RTO < 30 分钟。Active-Active 适合 RTO < 1 分钟（成本最高）。
  - **数据库跨区域复制延迟多少？**: MySQL 异步复制：秒级；半同步：百毫秒级；同步：受距离影响（跨 region 通常 > 50ms）。

---

### Q43: 解释 IAM 最小权限原则

- **难度**: 中级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 用户/服务只给**必需的权限**
  2. IAM 策略：Action + Resource 限定
  3. Terraform 服务账号用 **OIDC + AssumeRole** 而非长寿命 AK
  4. 定期用 IAM Access Analyzer 审查
  5. 生产环境用**专用子账号 + 自定义策略**

- **追问与参考答案（参考，未验证）**:
  - **OIDC 和 AK/SK 区别？**: OIDC 是短期凭证（CI 跑完自动失效），AK/SK 是长期凭证（泄露风险高）。CI/CD 中**必须用 OIDC**。
  - **如何审计 IAM 权限？**: 用 AWS IAM Access Analyzer 或腾讯云 CAM 审计。定期 review 用户的实际权限和需要的权限。

---

### Q44: 设计成本监控方案

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. Terraform 标签（Project, Environment, Owner）便于成本分摊
  2. 预算告警（Budget Alerts）
  3. 定时任务销毁非生产环境
  4. 使用 Spot/Preemptible 实例
  5. 定期成本审计（Infracost, Terraform Cloud Cost Estimation）

- **追问与参考答案（参考，未验证）**:
  - **Infracost 是什么？**: 第三方工具，在 `terraform plan` 时估算本次变更的成本。支持 AWS/Azure/GCP，免费版够用。
  - **如何自动销毁非生产环境？**: GitHub Actions 定时任务（cron）每天晚上 destroy 非生产环境；或用 Terraform Cloud 的 Drift Detection + 自动销毁策略。

---

### Q45: Terraform 资源出现循环依赖（circular dependency）怎么办？

- **难度**: 高级 ⭐⭐⭐⭐
- **答案要点**:
  1. 例：A 依赖 B，B 又依赖 A
  2. 解决方案：
     - **拆分资源**：将依赖拆为多层
     - 提取中间变量
     - 用 `lifecycle` 块
  3. 真实案例：Security Group 规则引用 SG 本身
  4. `terraform graph` 可视化依赖关系

- **追问与参考答案（参考，未验证）**:
  - **循环依赖的常见原因？**: 1) Security Group 规则引用 SG 本身；2) IAM Role 信任关系循环；3) 网络 ACL 和 Route Table 互相依赖。
  - **terraform graph 输出什么格式？**: DOT 格式（Graphviz），需要 `dot` 命令转 PNG：`terraform graph | dot -Tpng > graph.png`。

---

### Q46: 解释 Terraform vs Pulumi vs Ansible vs CloudFormation

- **难度**: 高级 ⭐⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：声明式 + 多云 + state 文件，最流行
  - **Pulumi**：声明式但用真实编程语言（TypeScript/Python/Go）
  - **Ansible**：命令式，主机配置管理
  - **CloudFormation**：AWS only，与 Terraform 类似
  - 选择：多云→Terraform；AWS only→CFN；代码友好→Pulumi

- **追问与参考答案（参考，未验证）**:
  - **Terraform Cloud 和 OpenTofu 区别？**: Terraform Cloud 是 HashiCorp 商业产品（额外功能），OpenTofu 是社区 fork 的开源版本。核心 IaC 引擎基本兼容。
  - **Pulumi 的劣势？**: 1) 学习曲线更陡（需要写代码）；2) 社区比 Terraform 小；3) 某些第三方模块不可用。

---

### Q47: 大规模部署（100+ 资源）性能优化

- **难度**: 高级 ⭐⭐⭐⭐
- **答案要点**:
  1. **拆分 state**：按服务或团队拆多个 state
  2. 用 `-target` 局部 apply
  3. `-parallelism` 控制并发数
  4. 模块化 + 复用变量
  5. 避免冗余的 `data source` 查询

- **追问与参考答案（参考，未验证）**:
  - **拆分 state 后跨模块引用怎么办？**: 用 `terraform_remote_state` data source 从其他 state 文件读取 outputs。例：`data "terraform_remote_state" "network" { backend = "s3" config = { ... } }`。
  - **parallelism 调多大好？**: 默认是 10。增大（如 20）能加速，但可能触发云 API 限流。建议先用默认，跑几次后观察日志再调整。

---

### Q48: 如何用 Terraform 管理 K8s 资源？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. 用 Kubernetes Provider
  2. 推荐 **Helm + Terraform** 或 **Helmfile**
  3. 生产级用 **ArgoCD / Flux** 做 GitOps
  4. Terraform 管**基础设施**（VPC、节点），K8s 管**应用层**

- **追问与参考答案（参考，未验证）**:
  - **K8s Provider 怎么认证？**: 用 K8s 集群的 `kubeconfig` 文件，或 Service Account token。生产用 Service Account + RBAC。
  - **Terraform 和 Helm 哪个先学？**: 先 Helm（理解 K8s 应用层），再 Terraform（管理 K8s 基础设施）。

---

### Q49: Serverless 架构如何用 Terraform 管？

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. 主流：腾讯云 SCF、AWS Lambda
  2. Terraform 用对应的云 provider
  3. 难点：API Gateway + Function + 事件源需要复杂编排
  4. 工具：Serverless Framework 配合 Terraform

- **追问与参考答案（参考，未验证）**:
  - **API Gateway 和 Function 怎么连？**: Terraform 中创建 `aws_apigatewayv2_api` + `aws_lambda_permission` 授权 API Gateway 调用 Lambda。
  - **Serverless 冷启动怎么解决？**: 预留并发（Provisioned Concurrency）、预热函数、或用 `SnapStart`（AWS）。

---

### Q50: 混合云架构设计

- **难度**: 资深 ⭐⭐⭐⭐
- **答案要点**:
  1. 跨云专线（如 AWS Direct Connect、腾讯云专线）
  2. Terraform **多 provider** 配置
  3. 统一身份认证（IAM Federation）
  4. 数据同步：跨云数据库复制
  5. 应用层：避免云厂商锁定

- **追问与参考答案（参考，未验证）**:
  - **跨云专线带宽多少钱？**: AWS Direct Connect 1Gbps 大约 $0.03/小时 + 端口费。腾讯云专线类似。需要评估带宽需求。
  - **如何避免云厂商锁定？**: 1) 用 Terraform（多云 IaC 工具）；2) 抽象基础设施层（K8s）；3) 用云中立服务（如数据库用 PostgreSQL 而不是 RDS）。

---

## 五、场景/排障/对比/行为（28 题）

### Q51: `terraform apply` 一直卡住，怎么办？

- **难度**: 初级 ⭐⭐⭐
- **出处**: Reddit r/Terraform 高频问题
- **答案要点**:
  1. 检查是否**死锁**：state 锁未释放
  2. 查 API 限流（429 Too Many Requests）→ 减小 `-parallelism`
  3. 查资源依赖：循环依赖
  4. 用 `TF_LOG=DEBUG` 看详细日志

---

### Q52: State 文件损坏了能恢复吗？

- **难度**: 高级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 有版本化 S3 → 回滚到上一个版本
  2. 无备份 → **灾难**：
     - 删 state，重新 `terraform import` 所有资源
     - 或手动重建基础设施（最后手段）
  3. **教训**：永远用远程 backend + 启用版本化 + 启用加密

---

### Q53: Drift 检测后发现资源被删除了，怎么办？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. 不要慌，先 `terraform plan -refresh-only` 确认
  2. `terraform apply` 重建资源
  3. ⚠️ 注意：如果是数据库实例，重建后**数据丢失**
  4. **预防**：开启删除保护、备份策略、审计告警

---

### Q54: 多人同时 apply 导致冲突

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. 必须用远程 backend + 锁（S3+DynamoDB、COS+自建锁）
  2. 锁冲突时，**等待**或**force-unlock**（谨慎）
  3. CI/CD 中串行 apply（不并发）
  4. 用 Atlantis/Terraform Cloud 集中执行

---

### Q55: `terraform destroy` 误删了重要资源，如何恢复？

- **难度**: 高级 ⭐⭐⭐⭐⭐
- **答案要点**:
  1. 如果开启了 Remote Backend 版本化 → 回滚 state
  2. 用 `terraform import` 重新导入资源
  3. 如果是无状态资源 → 重新 apply
  4. **教训**：用 `prevent_destroy` 保护关键资源

---

### Q56: `terraform plan` 报错 "Error acquiring the state lock" 怎么办？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  1. 检查是否有其他进程正在 apply
  2. 等几分钟再试
  3. 如果确认无人占用 → `terraform force-unlock <lock_id>`
  4. **获取 lock_id**：用 `terraform output` 或登录 S3/DynamoDB 查看

---

### Q57: module 引用的版本冲突怎么办？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. 用 `terraform init -upgrade` 升级所有依赖
  2. 在 `required_versions` 锁定 Terraform 版本
  3. 在 `required_providers` 锁定 provider 版本
  4. 检查 `.terraform.lock.hcl` 看版本哈希

---

### Q58: `terraform apply` 创建了资源但 state 没更新（崩溃了）

- **难度**: 高级 ⭐⭐⭐⭐
- **答案要点**:
  1. 下次 plan 会检测到实际资源存在，state 会同步更新
  2. 如果资源没创建成功 → 用 `terraform apply` 重试
  3. 如果资源部分创建 → 手动 `terraform state rm` 失败的资源，再 apply

---

### Q59: Terraform vs Ansible：什么时候用哪个？

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：基础设施编排（VM、网络、数据库）→ 声明式、跨云
  - **Ansible**：服务器配置、软件部署、运维自动化 → 命令式、无 agent
  - **组合**：Terraform 创建 VM → Ansible 配置应用
  - **典型工作流**：Terraform 起 EC2 → Ansible 装 Nginx

---

### Q60: Terraform vs CloudFormation

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：多云、HashiCorp 生态、社区大
  - **CloudFormation**：AWS 原生、AWS 资源覆盖最全、支持私有资源
  - 选择：只用 AWS 且需要 AWS 独有资源→CFN；多云或团队习惯→Terraform

---

### Q61: Terraform vs Pulumi

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  - **Terraform**：HCL DSL、学习曲线低、成熟生态
  - **Pulumi**：用 TypeScript/Python/Go 写 IaC、IDE 支持好、测试友好
  - 选择：开发者文化强→Pulumi；标准化、运维友好→Terraform

---

### Q62: count vs for_each 的真实生产陷阱

- **难度**: 中级 ⭐⭐⭐⭐
- **答案要点**:
  - **count 陷阱**：`var.servers = [A, B, C]` → 删除 B 变成 [A, C]，原 C 索引从 2 变成 1，**CVM 被销毁重建**
  - **for_each 优势**：用 key 标识（`name`），删除 B 后 C 保持不变
  - **最佳实践**：永远默认 `for_each`

---

### Q63: Terraform vs Helm（K8s 场景）

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  - Terraform 管**节点、LoadBalancer、存储**等基础设施
  - Helm 管**应用层**（Deployment、Service、ConfigMap）
  - 用 Terraform 部署 Helm chart（Helm provider）

---

### Q64: Terraform vs OpenTofu

- **难度**: 中级 ⭐⭐⭐
- **出处**: HashiCorp/Mozilla 分叉事件后
- **答案要点**:
  - **OpenTofu**：2023 年因 HashiCorp 改协议，社区 fork 出的开源版本
  - **Terraform**：HashiCorp 维护，1.6+ 后 BSL 协议
  - 完全兼容 HCL 语法，大部分模块可互换
  - 选择：开源优先 → OpenTofu；商业支持 → Terraform Cloud/Enterprise

---

### Q65: Terraform state 存在哪里最安全？

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. **本地磁盘**：❌ 仅个人开发用，不安全
  2. **S3/COS + 加密 + 版本化**：✅ 推荐用于生产
  3. **Terraform Cloud**：✅ 官方托管，自动备份 + 审计
  4. **HashiCorp Consul/Vault**：✅ 企业级
  5. **绝不能**：Git、共享文件夹、未加密的云存储

---

### Q66: "Tell me about a Terraform outage you handled"

- **类型**: 行为面试（STAR 框架）
- **难度**: 中级~高级 ⭐⭐⭐⭐
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

- **难度**: 中级 ⭐⭐
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

- **难度**: 中级 ⭐⭐⭐
- **建议答案**:
  - 如果用过：说具体功能（Remote Run、Policy as Code、Audit Logs）
  - 如果没用：说计划 + 对比自建方案

---

### Q76: "How do you handle Terraform when the cloud provider has no resource support?"

- **难度**: 高级 ⭐⭐⭐
- **答案要点**:
  1. 用 `terraform_data` + provisioner 自定义资源
  2. 写自定义 Provider（Go 语言）
  3. 等社区贡献或提交 PR
  4. 用 `null_resource` 占位（已弃用）

---

### Q77: "What's your team's approach to Terraform module versioning?"

- **难度**: 中级 ⭐⭐⭐
- **答案要点**:
  1. 用 Git tag（v1.0.0, v1.1.0）+ SemVer
  2. 通过 Terraform Registry 或私有 registry 分发
  3. 主项目用 `version = "~> 1.0"` 约束
  4. 每次模块变更发 CHANGELOG

---

### Q78: "How do you test infrastructure changes before applying to production?"

- **难度**: 中级 ⭐⭐⭐
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
