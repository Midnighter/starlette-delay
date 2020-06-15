################################################################################
# COMMANDS                                                                     #
################################################################################

.PHONY: clean
## Remove all dependency pins.
clean:
	rm -f requirements/*.txt

.PHONY: qa
## Apply code quality assurance tools.
qa:
	isort --recursive src/ locust/
	black src/ locust/ alembic/

## Upgrade the dependencies.
lock: requirements/requirements.txt requirements/locust.txt requirements/interactive.txt

requirements/requirements.txt:
	pip-compile --generate-hashes --upgrade --allow-unsafe requirements/requirements.in

requirements/locust.txt:
	pip-compile --generate-hashes --upgrade --allow-unsafe requirements/locust.in

requirements/interactive.txt:
	pip-compile --generate-hashes --upgrade --allow-unsafe requirements/interactive.in

.PHONY: install
install:
	pip install -r requirements/interactive.txt
	jupyter labextension install jupyterlab-plotly@4.8.1 --no-build
	jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.1 --no-build
	jupyter labextension install @jupyterlab/toc --no-build
	jupyter lab build

################################################################################
# Self Documenting Commands                                                    #
################################################################################

.DEFAULT_GOAL := show-help

# Inspired by
# <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && \
		echo '--no-init --raw-control-chars')
