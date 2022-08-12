build:
	docker compose -f "docker-compose.yml" -p "vk-bot" up --build -d
start:
	docker compose -p "vk-bot" start
stop:
	docker compose -p "vk-bot" stop