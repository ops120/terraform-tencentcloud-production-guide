# Phase 2：腾讯云 Provider 入门

> 预计用时：2~3 天 
> 目标：配置腾讯云认证，创建第一个云资源，掌握变量与输出

---

## 2.1 腾讯云 Provider 概述

腾讯云 Terraform Provider 由腾讯云官方维护，支持管理 200+ 种云资源，覆盖计算、网络、存储、数据库、安全等各大领域。
- **官方文档**：[https://registry.terraform.io/providers/tencentcloudstack/tencentcloud/latest/docs](https://registry.terraform.io/providers/tencentcloudstack/tencentcloud/latest/docs)
- **GitHub 仓库**：[https://github.com/tencentcloudstack/terraform-provider-tencentcloud](https://github.com/tencentcloudstack/terraform-provider-tencentcloud)
- **Provider 版本**：当前稳定版 v1.81.x，建议使用 `>= 1.81.0`

### Provider 的工作原理
```
你的 .tf 文件
    → Terraform 核心引擎            → 解析 HCL、管理 State、计算差异
    → tencentcloud Provider 插件     → 调用腾讯云 API（通过 SecretId/SecretKey 认证）
    → 腾讯云 API 网关                → 接受请求并操作云资源
    → 实际的云资源（VPC / CVM / 数据库...）
```

---

## 2.2 认证配置

### 2.2.1 创建 CAM 密钥

1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
2. 进入 **访问管理 (CAM)** → **用户** → **新建用户**
3. 选择 **自定义创建** → **可访问资源并接收消息**
4. 勾选 **编程访问**（产生 SecretId 和 SecretKey）
5. 关联策略（见下文"最小权限原则"）
6. 保存生成的 `SecretId` 和 `SecretKey`

### 2.2.2 CAM 策略的最小权限原则（重要！）

> ⚠️ **生产环境严禁使用 `AdministratorAccess`！** 这是最高权限策略，一旦泄露后果严重。
**最小权限原则**：只授予 Terraform 所需的最小权限集合。
#### 方式一：使用系统预置策略（推荐学习阶段）
在学习阶段，可以创建一个自定义策略，只包含 Terraform 可能用到的服务：

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "vpc:*",
        "cvm:*",
        "clb:*",
        "mysql:*",
        "redis:*",
        "cos:*",
        "cbs:*",
        "monitor:*",
        "cam:GetUser",
        "cam:DescribeRoleList",
        "ssl:DescribeCertificates"
      ],
      "resource": ["*"]
    }
  ]
}
```

#### 方式二：按资源类型细化（生产环境推荐）
在腾讯云 CAM 中创建自定义策略，限制只能操作特定 VPC 下的资源：
```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": "cvm:*",
      "resource": [
        "qcs::cvm:ap-guangzhou::instance/*",
        "qcs::cvm:ap-guangzhou::vpc/${vpc_id}"
      ]
    },
    {
      "effect": "allow",
      "action": "vpc:DescribeVpc*",
      "resource": ["*"]
    }
  ]
}
```

#### 学习阶段推荐的策略组合
| 策略名称 | 说明 | 建议 |
|----------|------|------|
| `AdministratorAccess` | 全读写权限 | 🔴 学习阶段也不推荐 |
| `QcloudTerraformFullAccess` | 腾讯云提供的 Terraform 专用策略 | ✅ 学习阶段首选 |
| 自定义策略（按需）| 只包含需要的服务权限 | ✅ 生产环境必须 |

> 💡 **如何找到 `QcloudTerraformFullAccess`**：在 CAM 策略搜索框中输入 `Terraform` 即可找到腾讯云预置的 Terraform 策略。
### 2.2.3 配置方式（推荐：环境变量）
#### Windows PowerShell

```powershell
# 设置当前会话的环境变量（推荐）
$env:TENCENTCLOUD_SECRET_ID  = "your_secret_id"
$env:TENCENTCLOUD_SECRET_KEY = "your_secret_key"
$env:TENCENTCLOUD_REGION     = "ap-guangzhou"

# 验证是否设置成功
Get-ChildItem Env:TENCENTCLOUD_*
```

#### Windows CMD（命令提示符）
```cmd
:: 注意：CMD 使用 set，不是 $env:
set TENCENTCLOUD_SECRET_ID=your_secret_id
set TENCENTCLOUD_SECRET_KEY=your_secret_key
set TENCENTCLOUD_REGION=ap-guangzhou

:: 验证
echo %TENCENTCLOUD_SECRET_ID%
```

#### macOS / Linux

```bash
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
export TENCENTCLOUD_REGION="ap-guangzhou"
```

> ⚠️ **PowerShell vs CMD 的区别**：
> - PowerShell 使用 `$env:变量名` 语法
> - CMD 使用 `set 变量名=值` 语法
> - 两者设置的变量**只在当前终端会话有效**，关闭终端后失效
> - 如果希望在 PowerShell 中持久化，可以添加到 `$PROFILE` 文件中
### 2.2.4 配置方式（内联—仅用于学习，禁止提交到 Git）
```hcl
provider "tencentcloud" {
  secret_id  = "your_secret_id"
  secret_key = "your_secret_key"
  region     = "ap-guangzhou"
}
```

> ⚠️ **生产环境严禁** 将密钥硬编码在 `.tf` 文件中，始终使用环境变量或密钥管理服务。
> 
> ⚠️ 即使你只是学习，也建议养成使用环境变量的习惯，避免不小心将密钥提交到 Git。
### 2.2.5 腾讯云 Region 列表

| Region | 代码 | 备注 |
|--------|------|------|
| 广州 | `ap-guangzhou` | 华南地区，推荐新用户使用 |
| 上海 | `ap-shanghai` | 华东地区 |
| 北京 | `ap-beijing` | 华北地区 |
| 成都 | `ap-chengdu` | 西南地区 |
| 重庆 | `ap-chongqing` | 西南地区 |
| 南京 | `ap-nanjing` | 华东地区 |
| 中国香港 | `ap-hongkong` | 境外 |
| 新加坡 | `ap-singapore` | 东南亚 |
| 硅谷 | `na-siliconvalley` | 北美 |

> 💡 **选择 Region 的建议**：
> - 选择离用户最近的 Region
> - 生产环境建议使用主流 Region（广州、上海、北京），服务更稳定
> - 不同 Region 的可用区不同，可用区代码如 `ap-guangzhou-3`、`ap-guangzhou-6`
> - 某些资源（如镜像 ID）在不同 Region 可能不同

---

## 2.3 第一个腾讯云资源：创建 CVM

### 项目结构

```bash
my-first-cvm/
├── main.tf
├── variables.tf
├── outputs.tf
└── terraform.tfvars   # 变量值（不提交到 Git）
```

### main.tf

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    tencentcloud = {
      source  = "tencentcloudstack/tencentcloud"
      version = ">= 1.81.0"
    }
  }
}

# Provider 配置
provider "tencentcloud" {
  region = var.region
}

# 创建 VPC
resource "tencentcloud_vpc" "main" {
  name       = var.vpc_name
  cidr_block = "10.0.0.0/16"
}

# 创建子网
resource "tencentcloud_subnet" "main" {
  vpc_id            = tencentcloud_vpc.main.id
  name              = var.subnet_name
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.availability_zone
}

# 创建安全组
resource "tencentcloud_security_group" "web" {
  name        = "web-sg"
  description = "Web server security group"
}

# 安全组规则——允许 HTTP 和 SSH
resource "tencentcloud_security_group_rule" "ssh" {
  security_group_id = tencentcloud_security_group.web.id
  type              = "ingress"
  cidr_ip           = "0.0.0.0/0"
  ip_protocol       = "tcp"
  port_range        = "22"
  policy            = "accept"
}

resource "tencentcloud_security_group_rule" "http" {
  security_group_id = tencentcloud_security_group.web.id
  type              = "ingress"
  cidr_ip           = "0.0.0.0/0"
  ip_protocol       = "tcp"
  port_range        = "80,443"
  policy            = "accept"
}

# 创建 CVM 实例

> 🎵 **费用提醒**：S5.LARGE8（4C8G）按量计费约 **0.4~0.5 元/小时**，一天约 10 元，一个月约 300 元。
> 学习完成后请立即执行 `terraform destroy` 清理，避免持续扣费！
> 建议在腾讯云控制台设置 **费用告警**（预算上限 100 元）。
resource "tencentcloud_cvm_instance" "web" {
  instance_name     = var.instance_name
  availability_zone = var.availability_zone
  image_id          = "img-eb30mz89"  # TencentOS Server 3.2 (64位)
  instance_type     = "S5.LARGE8"     # 4C8G 标准型（如需 2C4G 请使用 S5.MEDIUM4）
  system_disk_type = "CLOUD_SSD"
  system_disk_size = 50

  vpc_id    = tencentcloud_vpc.main.id
  subnet_id = tencentcloud_subnet.main.id

  security_groups = [tencentcloud_security_group.web.id]

  internet_max_bandwidth_out = 10
  allocate_public_ip         = true

  # 使用密码登录（生产环境建议使用密钥对）
  password = var.instance_password

  tags = {
    Name        = var.instance_name
    Environment = "dev"
  }
}
```

### variables.tf

```hcl
variable "region" {
  description = "腾讯云区域"
  type        = string
  default     = "ap-guangzhou"
}

variable "vpc_name" {
  description = "VPC 名称"
  type        = string
  default     = "demo-vpc"
}

variable "subnet_name" {
  description = "子网名称"
  type        = string
  default     = "demo-subnet"
}

variable "availability_zone" {
  description = "可用区"
  type        = string
  default     = "ap-guangzhou-3"
}

variable "instance_name" {
  description = "CVM 实例名称"
  type        = string
  default     = "web-server"
}

variable "instance_password" {
  description = "CVM 登录密码"
  type        = string
  sensitive   = true  # 标记为敏感，apply 时不会显示
}
```

### outputs.tf

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = tencentcloud_vpc.main.id
}

output "subnet_id" {
  description = "子网 ID"
  value       = tencentcloud_subnet.main.id
}

output "public_ip" {
  description = "CVM 公网 IP"
  value       = tencentcloud_cvm_instance.web.public_ip
}

output "private_ip" {
  description = "CVM 内网 IP"
  value       = tencentcloud_cvm_instance.web.private_ip
}
```

### terraform.tfvars

```hcl
region              = "ap-guangzhou"
availability_zone   = "ap-guangzhou-3"
instance_name       = "web-server-01"
instance_password   = "YourPassword123!"
```

> 将 `terraform.tfvars` 添加到 `.gitignore`，避免泄露密码。
### 部署

```bash
terraform init
terraform plan
terraform apply
```

### 清理

```bash
terraform destroy
```

> ⚠️ **重要：如果不 destroy，CVM 会持续扣费！** 按量计费的 CVM 即使关机也会收取磁盘费用。
> 可以在腾讯云控制台 → 费用中心查看当前账单，确认资源已释放。
### 如何获取镜像 ID 和实例类型？

在上面的示例中，我们直接写死了镜像 ID（`img-eb30mz89`）和实例类型（`S5.LARGE8`）。在实际项目中，应该通过以下方式获取：
**方式一：Terraform Data Source（推荐）**

```hcl
# 查询最新的 TencentOS 公共镜像
data "tencentcloud_images" "default" {
  image_type = ["PUBLIC_IMAGE"]
  os_name    = "TencentOS Server 3.2"
}

# 查询满足条件的实例类型
data "tencentcloud_instance_types" "default" {
  cpu_core_count = 2
  memory_size    = 4
}

# 使用 Data Source 查询结果
resource "tencentcloud_cvm_instance" "web" {
  image_id      = data.tencentcloud_images.default.images[0].image_id
  instance_type = data.tencentcloud_instance_types.default.instance_types[0].instance_type
}
```

**方式二：腾讯云控制台查询**

1. 进入 CVM 购买页面
2. 选择镜像和实例类型
3. 从 URL 或页面信息中获取镜像 ID

**方式三：腾讯云 CLI**

```bash
# 查询镜像
tccli cvm DescribeImages --ImageType PUBLIC_IMAGE --OsName "TencentOS Server 3.2"

# 查询实例类型
tccli cvm DescribeInstanceTypeConfigs --Filters "Name=zone,Values=ap-guangzhou-3"
```

> 💡 **为什么镜像 ID 不推荐硬编码？** 因为腾讯云会定期更新公共镜像，修复安全漏洞。硬编码镜像 ID 意味着你不会自动获得这些更新。使用 Data Source 按 `os_name` 查询可以获取最新版本。
---

## 2.4 变量进阶

### 变量类型

```hcl
# 字符串
variable "name" {
  type    = string
  default = "default-name"
}

# 数字
variable "count" {
  type    = number
  default = 3
}

# 布尔值
variable "enabled" {
  type    = bool
  default = true
}

# 列表
variable "azs" {
  type    = list(string)
  default = ["ap-guangzhou-3", "ap-guangzhou-4"]
}

# 映射
variable "tags" {
  type = map(string)
  default = {
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

# 对象（复杂结构）
variable "instance" {
  type = object({
    name   = string
    type   = string
    count  = number
    tags   = map(string)
  })
  default = {
    name  = "web"
    type  = "S5.LARGE8"
    count = 2
    tags  = {}
  }
}
```

### 变量赋值优先级（从低到高）

```
1. 默认值（default）                    → 最不优先
2. 环境变量 TF_VAR_<name>               → 适合 CI/CD
3. terraform.tfvars（或 *.auto.tfvars）  → 适合开发者本地
4. -var 或 -var-file 命令行参数          → 最优先，适合临时覆盖
```

> 💡 **环境变量方式**：设置 `TF_VAR_db_password=mysecret` 可以覆盖变量 `db_password` 的值，不需要创建 `.tfvars` 文件，非常适合 CI/CD 环境。
### sensitive 变量的实际效果
当变量标记为 `sensitive = true` 时：

```hcl
variable "instance_password" {
  description = "CVM 登录密码"
  type        = string
  sensitive   = true
}
```

**效果：**

1. **`terraform plan` 输出中**：密码值显示为 `(sensitive value)` 而不是明文
2. **`terraform apply` 输出中**：密码值不会显示
3. **`terraform output` 中**：如果 output 也标记了 `sensitive = true`，输出显示为 `<sensitive>`

```bash
# 有 sensitive 标记的输出
$ terraform output db_password
╷
│ Warning: Output refers to sensitive values
│
│ To still see them, use the `-raw` flag.
╵
<sensitive>

# 使用 -raw 查看（慎用！）
terraform output -raw db_password
```

> ⚠️ **注意**：`sensitive` 只是**防止在终端显示**，State 文件中仍然以明文存储密码。所以远程 State 的安全至关重要（如使用 COS 加密存储）。
### 空值（null）和可选变量
```hcl
variable "disk_size" {
  description = "数据盘大小，不传则不创建数据盘"
  type        = number
  default     = null  # 表示"未设置"
}

# 使用条件判断
resource "tencentcloud_cbs_storage" "data" {
  count        = var.disk_size != null ? 1 : 0
  storage_size = var.disk_size
}
```

---

## 2.5 输出进阶

```hcl
# 输出敏感信息
output "db_password" {
  value     = var.db_password
  sensitive = true  # apply 后显示为 <sensitive>
}

# 输出时描述
output "instance_id" {
  description = "CVM 实例 ID"
  value       = tencentcloud_cvm_instance.web.id
}

# 输出多个值（列表）
output "public_ips" {
  description = "所有 CVM 的公网 IP"
  value = tencentcloud_cvm_instance.web[*].public_ip
}

# 输出时进行转换
output "instance_ids_with_ips" {
  description = "实例 ID 和 IP 的映射"
  value = {
    for instance in tencentcloud_cvm_instance.web :
    instance.id => instance.public_ip
  }
}
```

### 查看输出

```bash
# 查看所有输出
terraform output

# 查看特定输出
terraform output public_ip

# 查看敏感输出（不隐藏）
terraform output -raw db_password

# 输出为 JSON 格式
terraform output -json
```

---

## 2.6 常见错误与排查
### 认证相关错误

```bash
# 错误 1：SecretId/SecretKey 未设置
Error: Missing required argument
  on main.tf line 10:
   10: provider "tencentcloud"
  The argument "region" is required, but no definition was found.

# 错误 2：密钥错误
Error: TencentCloud API error: InvalidSecretId
  Reason: 您提供的 SecretId 不存在或已禁用
# 错误 3：密钥被禁用
Error: TencentCloud API error: UnauthorizedOperation
  Reason: 密钥已被禁用，请登录 CAM 控制台检查
```

**排查步骤：**
1. 检查环境变量是否已设置：`echo $env:TENCENTCLOUD_SECRET_ID`（PowerShell）
2. 检查密钥是否已过期：登录 CAM 控制台查看
3. 检查密钥关联的策略是否足够：临时关联 `AdministratorAccess` 测试

### 资源创建错误

```bash
# CVM 实例类型在当前可用区不可用
Error: Code=InvalidParameterValue
  Reason: 指定的实例类型在当前可用区已售罄

# 解决：更换可用区或实例类型
```

---

## 🎯 互动练习

### 自测题
<details>
<summary>📝 第 1 题：配置腾讯云 Provider 认证，推荐的方式是什么？</summary>

A) 在 `.tf` 文件中写死 `secret_id` 和 `secret_key`  
B) 使用环境变量 `TENCENTCLOUD_SECRET_ID` 和 `TENCENTCLOUD_SECRET_KEY`  
C) 把密钥写在 `terraform.tfvars` 中  
D) 不配置，直接运行

**答案：B**。环境变量方式避免密钥被提交到 Git，是推荐做法。A 和 C 都有泄露风险。</details>

<details>
<summary>📝 第 2 题：以下哪个命令可以查看 CVM 创建后的公网 IP？</summary>

A) `terraform show`  
B) `terraform output`  
C) `terraform plan`  
D) `terraform state list`

**答案：B**。`terraform output` 可以查看定义的 output 值，包括 `public_ip`。</details>

<details>
<summary>📝 第 3 题：如何在多个环境中使用不同的变量值？</summary>

**答案**：为每个环境创建独立的 `terraform.tfvars` 文件（如 `dev.tfvars`、`prod.tfvars`），通过 `-var-file` 参数指定：
```bash
terraform apply -var-file=dev.tfvars
terraform apply -var-file=prod.tfvars
```
</details>

### 🪄 动手试一试
1. 修改 `terraform.tfvars` 中的 `instance_name`，重新 `apply`，观察 plan 输出中的 `~` 修改标记
2. 尝试用 `terraform output -json` 查看所有输出的 JSON 格式
3. 用 `terraform state show tencentcloud_cvm_instance.web` 查看 State 中 CVM 的完整属性
### 💡 思考题

> 执行 `terraform destroy` 后，State 文件还在吗？如果重新 `apply`，会创建新的资源还是使用旧的？
> <details>
> <summary>点击查看答案</summary>
> `destroy` 会清空 State 文件但不会删除文件本身。重新 `apply` 会创建全新的资源（新的 IP、新的 ID），因为旧资源已被销毁。State 文件里是空的，Terraform 认为没有任何资源存在。
> </details>

---

## ✅ 本阶段掌握要点
- [ ] 创建腾讯云 CAM 密钥（非 AdministratorAccess）
- [ ] 理解最小权限原则
- [ ] 配置 Provider 认证（环境变量方式）
- [ ] 理解 PowerShell 和 CMD 设置环境变量的区别
- [ ] 编写完整的 Terraform 项目（main + variables + outputs）
- [ ] 创建 VPC、子网、安全组、CVM 资源
- [ ] 理解如何获取镜像 ID 和实例类型
- [ ] 理解变量类型和赋值优先级
- [ ] 理解 sensitive 变量的实际效果
- [ ] 理解输出（output）的作用
- [ ] 成功执行 `apply` 和 `destroy`
- [ ] 了解常见错误的排查方法
---

**下一步 → [03-核心资源实战](03-核心资源实战.md)**