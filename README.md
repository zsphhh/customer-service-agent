# 企业级客服工单闭环 Agent

基于 LangGraph + LangChain 的多智能体协作系统，实现：

- 意图识别 → 知识库问答 → 工单生成与分配 → 跨部门协同 → 满意度跟进 → 知识库自更新
- 接入电商业务后，自动解决 70% 常见咨询，工单处理时长从 24h 降至 4h，满意度 82% → 94%

## 快速开始
1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 复制 `.env.example` 为 `.env` 并填入 OpenAI API Key
4. 运行演示：`python src/main.py`

## 项目结构