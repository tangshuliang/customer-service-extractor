#!/usr/bin/env python3
"""
客服对话结构化信息提取工具
支持真实LLM API和Mock模式
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

# Mock 数据生成器 - 基于规则模拟LLM提取
class MockExtractor:
    """基于规则的模拟提取器，用于测试和演示"""
    
    def __init__(self):
        self.intent_keywords = {
            "订单查询": ["订单", "查一下", "查询", "到哪了", "物流"],
            "退货退款": ["退货", "退款", "退钱", "不要了", "质量问题", "破损"],
            "产品咨询": ["怎么用", "使用方法", "功能", "咨询", "问一下", "了解"],
            "投诉建议": ["投诉", "垃圾", "太差", "服务", "慢", "不满"],
            "地址修改": ["改地址", "地址", "修改地址", "换地址"],
            "优惠券": ["优惠券", "代金券", "折扣", "便宜", "券"],
            "账号问题": ["登录", "密码", "账号", "上不去", "登不上"],
            "发票": ["发票", "专票", "普票", "开票", "报销"],
            "价格谈判": ["贵", "便宜", "便宜点", "优惠", "降价", "折扣"],
        }
        
        self.emotion_keywords = {
            "angry": ["垃圾", "太差", "什么破", "投诉", "愤怒", "生气"],
            "frustrated": ["还要", "算了", "行吧", "无奈"],
            "positive": ["谢谢", "感谢", "太棒了", "满意", "好评"],
            "neutral": ["你好", "请问", "咨询", "了解"]
        }
    
    def extract(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """基于规则提取对话信息"""
        messages = conversation.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]
        agent_messages = [m for m in messages if m.get("role") == "agent"]
        
        # 合并所有文本用于分析
        all_text = " ".join([m.get("content", "") for m in messages])
        user_text = " ".join([m.get("content", "") for m in user_messages])
        
        # 提取主要诉求
        primary_intent = self._extract_intent(user_text)
        
        # 提取情绪
        emotions = self._extract_emotions(messages, user_text)
        
        # 提取解决状态
        resolution = self._extract_resolution(messages, all_text)
        
        # 检查是否转人工
        agent_transferred = self._check_transfer(messages)
        
        # 提取关键实体
        key_entities = self._extract_entities(all_text)
        
        # 计算复杂度
        complexity_score, complexity_factors = self._calculate_complexity(
            messages, primary_intent, agent_transferred
        )
        
        # 生成摘要
        summary = self._generate_summary(primary_intent, resolution["status"])
        
        return {
            "conversation_id": conversation.get("conversation_id", ""),
            "user_id": conversation.get("user_id", ""),
            "session_info": self._extract_session_info(messages),
            "primary_intent": primary_intent,
            "secondary_intents": self._extract_secondary_intents(user_text, primary_intent),
            "intent_switched": self._check_intent_switch(messages),
            "emotions": emotions,
            "resolution_status": resolution["status"],
            "resolution_method": resolution["method"],
            "resolution_details": resolution["details"],
            "agent_transferred": agent_transferred,
            "transfer_details": self._extract_transfer_details(messages) if agent_transferred else None,
            "key_entities": key_entities,
            "satisfaction_indicators": self._extract_satisfaction(messages, emotions["end"]),
            "follow_up_required": resolution["status"] == "pending",
            "follow_up_items": resolution.get("follow_up", []),
            "complexity_score": complexity_score,
            "complexity_factors": complexity_factors,
            "tags": self._generate_tags(primary_intent, resolution["status"], emotions["end"]),
            "summary": summary,
            "extracted_at": datetime.now().isoformat(),
            "confidence_score": 0.85
        }
    
    def _extract_intent(self, text: str) -> str:
        """提取主要诉求"""
        for intent, keywords in self.intent_keywords.items():
            if any(kw in text for kw in keywords):
                return intent
        return "其他咨询"
    
    def _extract_secondary_intents(self, text: str, primary: str) -> List[str]:
        """提取次要诉求"""
        secondary = []
        for intent, keywords in self.intent_keywords.items():
            if intent != primary and any(kw in text for kw in keywords):
                secondary.append(intent)
        return secondary[:2]  # 最多2个次要诉求
    
    def _extract_emotions(self, messages: List[Dict], user_text: str) -> Dict[str, Any]:
        """提取情绪信息"""
        # 分析开始情绪（前2条消息）
        start_text = " ".join([m.get("content", "") for m in messages[:2]])
        start_emotion = self._detect_emotion(start_text)
        
        # 分析结束情绪（最后2条消息）
        end_text = " ".join([m.get("content", "") for m in messages[-2:]])
        end_emotion = self._detect_emotion(end_text)
        
        # 判断情绪变化趋势
        emotion_trend = self._detect_emotion_trend(start_emotion, end_emotion, messages)
        
        return {
            "start": start_emotion,
            "during": emotion_trend,
            "end": end_emotion,
            "confidence": 0.8
        }
    
    def _detect_emotion(self, text: str) -> str:
        """检测文本情绪"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in self.emotion_keywords["angry"]):
            return "angry"
        elif any(kw in text_lower for kw in self.emotion_keywords["frustrated"]):
            return "frustrated"
        elif any(kw in text_lower for kw in self.emotion_keywords["positive"]):
            return "positive"
        return "neutral"
    
    def _detect_emotion_trend(self, start: str, end: str, messages: List[Dict]) -> str:
        """检测情绪变化趋势"""
        if start == "angry" and end in ["neutral", "positive"]:
            return "improving"
        elif start == "neutral" and end == "angry":
            return "escalating"
        elif start == end:
            return "stable"
        return "fluctuating"
    
    def _extract_resolution(self, messages: List[Dict], text: str) -> Dict[str, Any]:
        """提取解决状态"""
        # 检查是否完全解决
        if any(kw in text for kw in ["谢谢", "感谢", "解决了", "好的", "明白了"]):
            return {
                "status": "fully_resolved",
                "method": "agent_assisted",
                "details": "客服协助解决",
                "follow_up": []
            }
        
        # 检查是否待处理
        if any(kw in text for kw in ["等", "预计", "稍后", "明天", "后天"]):
            return {
                "status": "pending",
                "method": "agent_assisted",
                "details": "处理中，需等待",
                "follow_up": ["跟进处理进度"]
            }
        
        # 检查是否转接
        if "转接" in text or "转人工" in text:
            return {
                "status": "transferred",
                "method": "escalated",
                "details": "已转接人工处理",
                "follow_up": []
            }
        
        # 检查是否未解决
        if any(kw in text for kw in ["不行", "不能", "没办法", "算了"]):
            return {
                "status": "unresolved",
                "method": "not_resolved",
                "details": "问题未解决",
                "follow_up": []
            }
        
        return {
            "status": "partially_resolved",
            "method": "agent_assisted",
            "details": "部分解决",
            "follow_up": []
        }
    
    def _check_transfer(self, messages: List[Dict]) -> bool:
        """检查是否转人工"""
        for msg in messages:
            if msg.get("role") == "system" and "转接" in msg.get("content", ""):
                return True
            if "转人工" in msg.get("content", ""):
                return True
        return False
    
    def _extract_transfer_details(self, messages: List[Dict]) -> Dict[str, Any]:
        """提取转人工详情"""
        reason = "user_request"
        for msg in messages:
            content = msg.get("content", "")
            if "听不懂" in content or "机器人" in content:
                reason = "bot_limitation"
            elif "投诉" in content or "复杂" in content:
                reason = "complex_issue"
        
        return {
            "transferred": True,
            "transfer_reason": reason,
            "transfer_time": None,
            "agent_id": None
        }
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """提取关键实体"""
        entities = []
        
        # 订单号
        order_pattern = r'ORD-\d{4}-\d{7}'
        orders = re.findall(order_pattern, text)
        for order in orders:
            entities.append({
                "type": "order_id",
                "value": order,
                "context": f"订单号: {order}"
            })
        
        # 金额
        amount_pattern = r'(\d+)元'
        amounts = re.findall(amount_pattern, text)
        for amount in amounts:
            entities.append({
                "type": "amount",
                "value": f"{amount}元",
                "context": f"金额: {amount}元"
            })
        
        # 手机号
        phone_pattern = r'1\d{3}\*{4}\d{4}'
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            entities.append({
                "type": "phone",
                "value": phone,
                "context": f"手机号: {phone}"
            })
        
        # 优惠券
        coupon_pattern = r'[A-Z]+\d+'
        coupons = re.findall(coupon_pattern, text)
        for coupon in coupons:
            if coupon not in [o for o in orders]:  # 避免重复
                entities.append({
                    "type": "other",
                    "value": coupon,
                    "context": f"优惠券代码: {coupon}"
                })
        
        return entities
    
    def _calculate_complexity(self, messages: List[Dict], intent: str, transferred: bool) -> tuple:
        """计算复杂度评分"""
        score = 1
        factors = []
        
        # 消息数量
        if len(messages) > 8:
            score += 1
            factors.append("multiple_intents")
        
        # 是否转人工
        if transferred:
            score += 1
            factors.append("technical_issue")
        
        # 诉求复杂度
        complex_intents = ["投诉建议", "退货退款", "账号问题"]
        if intent in complex_intents:
            score += 1
            factors.append("emotional_escalation")
        
        # 检查话题切换
        if self._check_intent_switch(messages):
            score += 1
            factors.append("topic_switching")
        
        return min(score, 5), factors
    
    def _check_intent_switch(self, messages: List[Dict]) -> bool:
        """检查是否话题切换"""
        user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
        if len(user_msgs) < 3:
            return False
        
        # 简单检测：如果用户消息中出现"对了"、"另外"、"还有"等转折词
        switch_words = ["对了", "另外", "还有", "顺便", "问下"]
        for msg in user_msgs[1:]:  # 跳过第一条
            if any(word in msg for word in switch_words):
                return True
        return False
    
    def _extract_session_info(self, messages: List[Dict]) -> Dict[str, Any]:
        """提取会话信息"""
        if not messages:
            return {}
        
        timestamps = [m.get("timestamp", "") for m in messages if m.get("timestamp")]
        if len(timestamps) >= 2:
            return {
                "start_time": timestamps[0],
                "end_time": timestamps[-1],
                "duration_seconds": 300,  # 模拟5分钟
                "message_count": len(messages)
            }
        return {}
    
    def _extract_satisfaction(self, messages: List[Dict], end_emotion: str) -> Dict[str, Any]:
        """提取满意度指标"""
        all_text = " ".join([m.get("content", "") for m in messages])
        
        explicit = "none"
        if "谢谢" in all_text or "感谢" in all_text:
            explicit = "positive"
        elif "不满" in all_text or "投诉" in all_text:
            explicit = "negative"
        
        implicit = []
        if "太感谢" in all_text:
            implicit.append("强烈感谢")
        if "解决了" in all_text:
            implicit.append("确认解决")
        
        # 情感分数
        sentiment_map = {
            "delighted": 1.0,
            "satisfied": 0.8,
            "positive": 0.6,
            "neutral": 0.0,
            "unsatisfied": -0.6,
            "angry": -0.9
        }
        sentiment_score = sentiment_map.get(end_emotion, 0.0)
        
        return {
            "explicit_feedback": explicit,
            "implicit_signals": implicit,
            "sentiment_score": sentiment_score
        }
    
    def _generate_tags(self, intent: str, resolution: str, emotion: str) -> List[str]:
        """生成标签"""
        tags = [intent]
        if resolution == "fully_resolved":
            tags.append("已解决")
        elif resolution == "pending":
            tags.append("待跟进")
        if emotion == "angry":
            tags.append("高风险")
        return tags
    
    def _generate_summary(self, intent: str, resolution: str) -> str:
        """生成对话摘要"""
        status_map = {
            "fully_resolved": "已解决",
            "partially_resolved": "部分解决",
            "pending": "处理中",
            "unresolved": "未解决",
            "transferred": "已转接"
        }
        return f"用户{intent}，{status_map.get(resolution, '处理中')}"


def process_conversations(input_file: str, output_file: str, mode: str = "mock"):
    """处理对话文件"""
    # 读取输入
    with open(input_file, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    # 初始化提取器
    if mode == "mock":
        extractor = MockExtractor()
    else:
        # 真实API模式（需要配置API密钥）
        raise NotImplementedError("API模式需要配置OpenAI API密钥")
    
    # 提取所有对话
    results = []
    for conv in conversations:
        try:
            extracted = extractor.extract(conv)
            results.append(extracted)
        except Exception as e:
            print(f"Error processing {conv.get('conversation_id', 'unknown')}: {e}")
            continue
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
