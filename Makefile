EXT:=com.github.ahaasler.ulauncher-tmux

.PHONY: help dev
.DEFAULT_GOAL := help

##@ Development

dev: ## Run ulauncher and extension on development mode
	@killall ulauncher &> /dev/null || printf ''
	@ln -sfn $(shell pwd) ~/.local/share/ulauncher/extensions/${EXT}.dev
	@trap 'kill %1' SIGINT
	@ulauncher --dev --no-extensions |& grep "${EXT}.dev" & sleep 1; VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/${EXT}.dev PYTHONPATH=/usr/lib/python3.9/site-packages python main.py
	@rm -r ~/.local/share/ulauncher/extensions/${EXT}.dev

##@ Help

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
