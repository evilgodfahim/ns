.PHONY: help install run validate docker-up docker-down docker-logs test clean

# Default target
help:
	@echo "New Scientist RSS Scraper - Available Commands:"
	@echo ""
	@echo "  make install        - Install dependencies"
	@echo "  make run            - Run scraper (with FlareSolverr if available)"
	@echo "  make validate       - Validate generated RSS feed"
	@echo "  make docker-up      - Start all Docker services"
	@echo "  make docker-down    - Stop all Docker services"
	@echo "  make docker-logs    - View Docker logs"
	@echo "  make docker-restart - Restart Docker services"
	@echo "  make test           - Run scraper and validate feed"
	@echo "  make clean          - Remove generated files"
	@echo ""

# Install Python dependencies
install:
	pip install -r requirements.txt

# Run scraper locally
run:
	@if docker ps | grep -q flaresolverr; then \
		echo "Using FlareSolverr..."; \
		FLARESOLVERR_URL=http://localhost:8191/v1 python scraper.py; \
	else \
		echo "FlareSolverr not running, using direct requests..."; \
		python scraper.py; \
	fi

# Validate RSS feed
validate:
	python validate_feed.py

# Start Docker services
docker-up:
	docker-compose up -d
	@echo ""
	@echo "Services started! Access points:"
	@echo "  - RSS Feed: http://localhost:8080/feed.xml"
	@echo "  - Landing Page: http://localhost:8080/"
	@echo "  - FlareSolverr: http://localhost:8191"
	@echo ""
	@echo "View logs with: make docker-logs"

# Stop Docker services
docker-down:
	docker-compose down

# View Docker logs
docker-logs:
	docker-compose logs -f

# Restart Docker services
docker-restart:
	docker-compose restart
	docker-compose logs -f

# Run tests
test: run validate
	@echo "✓ All tests passed!"

# Clean generated files
clean:
	rm -f feed.xml
	@echo "Cleaned generated files"

# Development: Start FlareSolverr only
flaresolverr:
	docker run -d --name trawl -p 8191:8191 ghcr.io/flaresolverr/flaresolverr:latest
	@echo "FlareSolverr started on port 8191"

# Development: Stop FlareSolverr
flaresolverr-stop:
	docker stop flaresolverr || true
	docker rm flaresolverr || true

# Development: Test FlareSolverr
flaresolverr-test:
	@curl -s http://localhost:8191/health && echo "✓ FlareSolverr is healthy" || echo "✗ FlareSolverr is not responding"

# Full reset
reset: docker-down clean
	@echo "Full reset complete"

# Deploy to GitHub
deploy:
	git add .
	git commit -m "Update scraper" || true
	git push
	@echo "Pushed to GitHub - Actions will deploy automatically"
