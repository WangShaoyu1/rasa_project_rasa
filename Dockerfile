# RASA Dockerfile
FROM rasa/rasa:3.6.20-full

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装额外依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制RASA项目文件
COPY . .

# 训练模型
RUN rasa train

# 暴露端口
EXPOSE 5005 5055

# 设置环境变量
ENV RASA_MODEL_PATH=/app/models

# 启动命令
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]

