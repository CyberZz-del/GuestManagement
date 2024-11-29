# 嘉宾管理系统

## 介绍
嘉宾管理系统旨在简化管理活动、酒店或其他场所嘉宾的过程。它提供了一个易于使用的界面，用于跟踪嘉宾信息、预订和其他相关活动。

## 功能
- 嘉宾信息导入
- 嘉宾信息预览
- 嘉宾信息跟踪
- 报告和分析
- 用户认证和授权

## 安装
要安装嘉宾管理系统，请按照以下步骤操作：

1. 进入项目目录：
    ```bash
    cd Guest_Management_System
    ```
2. 安装所需的依赖项：
    ```bash
    npm install --force
    pip install -r requirements.txt
    ```
3. 配置数据库连接：
    - 创建一个名为 `guest_management_system` 的数据库。
    - 在 `.env` 文件中配置数据库连接信息：
        ```env
        DB_HOST=localhost
        DB_USER=root
        DB_PASS=password
        DB_NAME=guest_management_system
        ```
4. 运行后端服务：
    ```bash
    uvicorn app.main:app --reload
    ```
5. 运行前端服务：
    ```bash
    npm start
    ```
6. 打开浏览器并导航到 `http://localhost:3000` 以访问系统。默认管理员为
    - 用户名：123@admin.com
    - 密码：123


