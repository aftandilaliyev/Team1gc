# SDK commands
sdk-generate:
	./scripts/generate-sdk.sh

sdk-push:
	./scripts/push-sdk.sh

# Backend setup and run
backend-setup:
	@if [ ! -f backend/.env ]; then \
		echo "Error: backend/.env file not found. Please create it before running."; \
		exit 1; \
	fi

	cd backend && docker compose up --build -d

backend-down:
	cd backend && docker compose down

# Frontend setup and run
frontend-setup:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

# Combined commands
setup: backend-setup frontend-setup
	@echo "Setup complete"

dev: backend-setup frontend-dev
	@echo "Development environment started"
