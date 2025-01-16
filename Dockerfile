FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i http://pypi.magic.com/repository/pypi/simple --trusted-host pypi.magic.com

# 复制应用代码
COPY . .
RUN python manage.py makemigrations api_main && python manage.py migrate
# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]