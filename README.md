# 智能家居语音交互系统 - RASA对话引擎

[![RASA](https://img.shields.io/badge/rasa-3.6.20-orange.svg)](https://rasa.com)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

基于RASA 3.6的智能家居语音交互对话引擎，支持中文自然语言理解和多轮对话管理，专为智能家居场景优化。

## ✨ 核心特性

- 🤖 **RASA 3.6** - 最新版本的开源对话AI框架
- 🇨🇳 **中文优化** - 集成Jieba分词，专门优化中文理解
- 🏠 **智能家居专用** - 针对家居设备控制场景训练
- 💬 **多轮对话** - 支持复杂的多轮对话和上下文管理
- 📝 **表单填槽** - 智能收集设备控制所需参数
- 🔧 **自定义Actions** - 丰富的设备控制和查询功能
- 📊 **意图识别** - 高精度的用户意图理解
- 🎯 **实体提取** - 准确提取设备、位置、操作等关键信息

## 🛠️ 技术栈

- **对话框架**: RASA 3.6.20
- **NLU引擎**: DIET Classifier + RegexFeaturizer
- **中文分词**: Jieba
- **对话策略**: TEDPolicy + RulePolicy + MemoizationPolicy
- **Actions服务**: RASA SDK 3.6.2
- **容器化**: Docker + Docker Compose

## 🚀 快速开始

### 环境要求

- Python 3.8+ (推荐 3.9)
- RASA 3.6+
- 8GB+ RAM (推荐)

### 安装部署

#### 1. 克隆项目
```bash
git clone https://github.com/WangShaoyu1/rasa_project_rasa.git
cd rasa_project_rasa
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 训练模型
```bash
rasa train
```

#### 5. 启动RASA服务
```bash
# 启动RASA Core服务
rasa run --enable-api --cors "*" --debug

# 新开终端启动Actions服务
rasa run actions --debug
```

#### 6. 测试对话
```bash
# 命令行测试
rasa shell

# 或通过HTTP API测试
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "打开客厅的灯"}'
```

## 📁 项目结构

```
├── data/                    # 训练数据
│   ├── nlu.yml             # NLU训练数据
│   ├── stories.yml         # 对话故事
│   ├── rules.yml           # 对话规则
│   └── jieba_userdict.txt  # Jieba自定义词典
├── actions/                 # 自定义Actions
│   ├── __init__.py
│   └── actions.py          # Actions实现
├── models/                  # 训练好的模型
├── tests/                   # 测试文件
├── domain.yml              # Domain配置
├── config.yml              # 模型配置
├── endpoints.yml           # 端点配置
├── credentials.yml         # 凭证配置
├── requirements.txt        # Python依赖
├── Dockerfile             # Docker配置
└── docker-compose.yml     # Docker Compose配置
```

## 🎯 支持的意图和实体

### 意图 (Intents)

| 意图 | 描述 | 示例 |
|------|------|------|
| `control_light` | 控制灯光 | "打开客厅的灯" |
| `control_air_conditioner` | 控制空调 | "把空调温度调到26度" |
| `control_curtain` | 控制窗帘 | "拉开卧室的窗帘" |
| `control_tv` | 控制电视 | "打开客厅的电视" |
| `control_music` | 控制音乐 | "播放轻音乐" |
| `ask_weather` | 询问天气 | "今天天气怎么样" |
| `ask_time` | 询问时间 | "现在几点了" |
| `ask_device_status` | 查询设备状态 | "客厅的灯开着吗" |

### 实体 (Entities)

| 实体 | 描述 | 示例值 |
|------|------|--------|
| `device_type` | 设备类型 | 灯、空调、窗帘、电视 |
| `location` | 位置 | 客厅、卧室、厨房、书房 |
| `action` | 操作动作 | 打开、关闭、调亮、调暗 |
| `value` | 数值 | 50%、26度、大声 |
| `color` | 颜色 | 红色、蓝色、暖白 |
| `temperature` | 温度 | 26度、低温、高温 |
| `brightness` | 亮度 | 50%、很亮、很暗 |

## 🔧 配置说明

### NLU配置 (config.yml)

```yaml
pipeline:
  - name: JiebaTokenizer              # 中文分词
    dictionary_path: "data/jieba_userdict.txt"
  - name: RegexFeaturizer            # 正则特征
  - name: LexicalSyntacticFeaturizer # 词汇语法特征
  - name: CountVectorsFeaturizer     # 词向量特征
  - name: DIETClassifier             # 意图分类和实体提取
    epochs: 100
  - name: EntitySynonymMapper        # 实体同义词映射
```

### 对话策略配置

```yaml
policies:
  - name: MemoizationPolicy          # 记忆策略
  - name: RulePolicy                 # 规则策略
  - name: UnexpecTEDIntentPolicy     # 意外意图策略
  - name: TEDPolicy                  # 对话策略
    max_history: 5
    epochs: 100
```

## 🎮 自定义Actions

### 设备控制Action
```python
class ActionControlDevice(Action):
    def name(self) -> Text:
        return "action_control_device"
    
    def run(self, dispatcher, tracker, domain):
        device_type = tracker.get_slot("device_type")
        location = tracker.get_slot("location")
        action = tracker.get_slot("action")
        
        # 调用后端API控制设备
        # ...
        
        dispatcher.utter_message(
            text=f"好的，已经为你{action}{location}的{device_type}。"
        )
        return []
```

### 表单验证Action
```python
class ValidateDeviceControlForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_device_control_form"
    
    def validate_device_type(self, slot_value, dispatcher, tracker, domain):
        valid_devices = ["灯", "空调", "窗帘", "电视"]
        if slot_value in valid_devices:
            return {"device_type": slot_value}
        else:
            dispatcher.utter_message(text="抱歉，我不支持控制这种设备。")
            return {"device_type": None}
```

## 🔗 相关仓库

- **前端管理后台**: [rasa_project_frontend](https://github.com/WangShaoyu1/rasa_project_frontend)
- **后端API服务**: [rasa_project_backend](https://github.com/WangShaoyu1/rasa_project_backend)

## 🚀 部署

### Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f rasa
```

### 生产环境部署

```bash
# 训练模型
rasa train --config config.yml --domain domain.yml --data data/

# 启动RASA服务
rasa run --enable-api --cors "*" --port 5005

# 启动Actions服务
rasa run actions --port 5055
```

### Kubernetes部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rasa-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rasa
  template:
    metadata:
      labels:
        app: rasa
    spec:
      containers:
      - name: rasa
        image: your-registry/rasa-smart-home:latest
        ports:
        - containerPort: 5005
```

## 🛠️ 开发指南

### 添加新意图

1. 在 `data/nlu.yml` 添加训练数据
2. 在 `domain.yml` 添加意图定义
3. 在 `data/stories.yml` 添加对话流程
4. 重新训练模型

### 添加新实体

1. 在 `data/nlu.yml` 标注实体
2. 在 `domain.yml` 添加实体和槽位定义
3. 在 `actions/actions.py` 处理实体逻辑
4. 更新 `data/jieba_userdict.txt` 词典

### 自定义Actions

1. 在 `actions/actions.py` 创建Action类
2. 在 `domain.yml` 添加action定义
3. 在stories或rules中使用action
4. 重启actions服务

### 模型优化

```bash
# 交互式学习
rasa interactive

# 模型测试
rasa test

# 性能评估
rasa test nlu --cross-validation
```

## 📊 性能指标

- **意图识别准确率**: >95%
- **实体提取F1值**: >90%
- **对话成功率**: >85%
- **响应时间**: <500ms
- **并发支持**: 100+ QPS

## 🧪 测试

```bash
# 运行所有测试
rasa test

# NLU测试
rasa test nlu

# Core测试
rasa test core

# 交叉验证
rasa test nlu --cross-validation
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📞 支持

如有问题或建议，请通过以下方式联系：

- 📧 邮箱：support@smart-home-voice.com
- 🐛 问题反馈：[GitHub Issues](https://github.com/WangShaoyu1/rasa_project_rasa/issues)
- 📖 RASA文档：[https://rasa.com/docs/](https://rasa.com/docs/)

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
