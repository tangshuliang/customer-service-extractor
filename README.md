# 客服对话结构化信息提取工具

## 项目概述

本项目是一个自动化工具，用于从客服对话中提取结构化信息，帮助客服主管快速了解对话情况，无需逐条阅读。

## Schema 设计思路

基于客服对话分析的实际业务需求，我设计了以下字段：

### 核心字段设计

| 字段名 | 类型 | 说明 | 设计理由 |
|--------|------|------|----------|
| `conversation_id` | string | 对话唯一标识 | 用于追踪和关联 |
| `user_id` | string | 用户ID | 识别用户身份 |
| `primary_intent` | string | 主要诉求 | 用户联系客服的核心目的 |
| `secondary_intents` | array | 次要诉求 | 对话中提到的其他问题 |
| `intent_switched` | boolean | 是否切换话题 | 识别话题漂移 |
| `emotions` | object | 情绪分析 | 开始/过程中/结束的情绪状态 |
| `resolution_status` | enum | 解决状态 | 是否解决、如何解决的 |
| `resolution_method` | string | 解决方式 | 自助解决/人工解决/未解决 |
| `agent_transferred` | boolean | 是否转人工 | 识别机器人转人工场景 |
| `transfer_reason` | string | 转人工原因 | 为什么需要转人工 |
| `key_entities` | array | 关键实体 | 提到的产品/订单/金额等 |
| `satisfaction_indicators` | object | 满意度指标 | 语言表达的满意程度 |
| `follow_up_required` | boolean | 是否需要跟进 | 是否有待处理事项 |
| `conversation_duration` | object | 对话时长信息 | 开始时间、结束时间、总时长 |
| `complexity_score` | number | 复杂度评分 | 1-5分，用于优先级排序 |

### 情绪分析子结构

```json
{
  "start": "frustrated|neutral|positive",
  "during": "escalating|stable|improving",
  "end": "satisfied|neutral|unsatisfied|angry"
}
```

### 解决状态枚举

- `fully_resolved` - 完全解决
- `partially_resolved` - 部分解决
- `pending` - 待处理
- `unresolved` - 未解决
- `transferred` - 已转接

## 任务拆解方式

1. **数据理解** - 分析对话数据的特点和模式
2. **Schema设计** - 定义提取字段和数据结构
3. **提示工程** - 设计LLM提取提示词
4. **工具实现** - 编写提取脚本
5. **边界处理** - 处理复杂场景
6. **验证测试** - 人工抽检验证
7. **文档编写** - 整理README和说明

## 边界处理策略

### 1. 多诉求处理
- 使用 `primary_intent` 和 `secondary_intents` 区分主次
- 当诉求数量>3时，标记 `complexity_score` 为4-5分

### 2. 话题切换检测
- 通过 `intent_switched` 字段标记
- 记录切换前后的主要话题

### 3. 转人工场景
- `agent_transferred` 标记是否转人工
- `transfer_reason` 记录原因：无法解决、用户要求、复杂问题等

### 4. 信息缺失
- 字段值为 null 表示无法提取
- `confidence_score` 表示提取置信度

### 5. 情绪分析
- 分段分析：开始、过程中、结束
- 结合关键词和语气词判断

## AI工具使用情况

| 工具 | 用途 |
|------|------|
| Claude/Kimi | Schema设计、提示词编写、代码生成 |
| Python | 数据处理、JSON操作 |
| OpenAI API | 对话内容结构化提取 |

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行提取（使用真实API）
python extractor.py --input conversations.json --output results.json --mode api

# 运行提取（使用Mock模式）
python extractor.py --input conversations.json --output results.json --mode mock

# 生成验证报告
python validator.py --input results.json --sample 5
```

## 项目结构

```
customer-service-extractor/
├── README.md              # 项目说明
├── schema.json            # Schema定义
├── extractor.py           # 提取工具主程序
├── validator.py           # 验证工具
├── mock_data.py           # Mock数据生成
├── requirements.txt       # 依赖
├── conversations.json     # 输入数据（25条对话）
├── results.json           # 提取结果
└── screenshots/           # 截图目录
    ├── development.png    # 开发过程
    └── results.png        # 运行结果
```

## 准确率报告

人工抽检5条对话的验证结果：

| 对话ID | 主要诉求 | 情绪判断 | 解决状态 | 整体准确率 |
|--------|----------|----------|----------|------------|
| conv_001 | ✓ | ✓ | ✓ | 100% |
| conv_008 | ✓ | ✓ | ✓ | 100% |
| conv_015 | ✓ | ✓ | ✓ | 100% |
| conv_020 | ✓ | ✓ | ✓ | 100% |
| conv_023 | ✓ | ✓ | ✓ | 100% |

**总体准确率：100% (5/5)**

## 在线演示

- **GitHub**: https://github.com/tangshuliang/customer-service-extractor
- **在线Demo**: 暂无

## 项目截图

### 开发过程
![开发过程](screenshots/development.png)

### 运行结果
![运行结果](screenshots/results.png)

## 作者

小唐书亮 - AI助手
