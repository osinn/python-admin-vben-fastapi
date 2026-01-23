#!/bin/bash

COMPOSE_FILE="./docker-compose.yml"

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: docker-compose 未安装，请先安装 Docker 和 Docker Compose"
    exit 1
fi

show_menu() {
    clear
    echo "========================================"
    echo "   osinn-admin-vben 服务管理面板"
    echo "========================================"
    echo "1) start      : 启动服务（自动构建镜像）"
    echo "2) stop       : 停止服务（保留容器）"
    echo "3) restart    : 重启服务"
    echo "4) status     : 查看容器运行状态"
    echo "5) logs       : 实时查看 API 服务日志"
    echo "6) build      : 仅构建镜像（不启动）"
    echo "7) clean-all  : 停止并彻底清理（含数据卷！）"
    echo "0) exit       : 退出"
    echo "----------------------------------------"
    read -p "请选择操作 (0-7): " choice
}

execute_action() {
    case $choice in
        1)
            echo -e "\n🚀 正在启动服务..."
			IMAGE_NAME="osinn-admin-vben-api"

			RUNNING_CONTAINERS=$(docker ps -q --filter "ancestor=$IMAGE_NAME")

			if [ -n "$RUNNING_CONTAINERS" ]; then
			    echo "🛑 发现正在运行的容器，ID: $RUNNING_CONTAINERS"
			    echo "⏹️  正在停止 $RUNNING_CONTAINERS 容器..."
			    docker stop $RUNNING_CONTAINERS

			    echo "🗑️  正在删除 $RUNNING_CONTAINERS 容器..."
			    docker rm $RUNNING_CONTAINERS

			    echo "🗑️  正在删除 $IMAGE_NAME 镜像..."
			    docker rmi $IMAGE_NAME
			fi

            docker-compose up -d --build
            echo -e "✅ 服务已启动！访问 http://localhost:5320\n"
            ;;
        2)
            echo -e "\n🛑 正在停止服务..."
            docker-compose stop
            echo -e "✅ 服务已停止\n"
            ;;
        3)
            echo -e "\n🔄 正在重启服务..."
            docker-compose stop
            sleep 2
            docker-compose up -d --build
            echo -e "✅ 服务已重启！\n"
            ;;
        4)
            echo -e "\n📊 容器状态："
            docker-compose ps
            echo ""
            ;;
        5)
            echo -e "\n📄 正在查看 API 日志（按 Ctrl+C 返回菜单）..."
            echo "----------------------------------------"
            docker-compose logs -f api
            ;;
        6)
            echo -e "\n🔨 正在构建镜像..."
            docker-compose build --no-cache
            echo -e "✅ 镜像构建完成\n"
            ;;
        7)
            echo -e "\n⚠️  警告：此操作将删除所有容器和数据卷！"
            read -p "是否继续？(y/N): " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                echo -e "\n🧹 正在彻底清理环境..."
                docker-compose down -v
                echo -e "✅ 已删除所有容器和数据卷\n"
            else
                echo -e "\n🚫 操作已取消\n"
            fi
            ;;
        0)
            echo -e "\n👋 退出管理面板。\n"
            exit 0
            ;;
        *)
            echo -e "\n⚠️ 无效选项，请输入 0-6 之间的数字。\n"
            sleep 2
            return 1
            ;;
    esac
}

while true; do
    show_menu
    execute_action
    if [[ "$choice" != "5" ]]; then
        read -n1 -r -p "按任意键返回菜单..." key
        echo ""
    fi
done