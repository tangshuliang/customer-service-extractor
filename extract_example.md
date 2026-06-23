# 提取示例

## 示例对话

```
用户: 我要退货！这什么破质量
客服: 非常抱歉给您带来不好的体验。请问具体是什么问题呢？
用户: 衣服收到就有破洞！这也能发货？
客服: 实在抱歉，这确实是我们的失误。我立即为您办理退货退款，并承担运费。
用户: 行吧，希望能快点
```

## 提取结果示例

```json
{
  "conversation_id": "conv_002",
  "user_id": "user_4521",
  "primary_intent": "退货退款",
  "secondary_intents": ["投诉建议"],
  "emotions": {
    "start": "angry",
    "during": "improving",
    "end": "neutral"
  },
  "resolution_status": "fully_resolved",
  "resolution_method": "agent_assisted",
  "agent_transferred": false,
  "key_entities": [
    {"type": "order_id", "value": "ORD-2024-9988776"}
  ],
  "complexity_score": 3,
  "summary": "用户因商品质量问题申请退货，客服协助办理退款"
}
```

## 字段说明

- **conversation_id**: 对话唯一标识
- **primary_intent**: 主要诉求（退货退款/订单查询/产品咨询等）
- **emotions**: 情绪变化（开始→过程中→结束）
- **resolution_status**: 解决状态（fully_resolved/pending/unresolved）
- **agent_transferred**: 是否转人工
- **complexity_score**: 复杂度评分（1-5）
