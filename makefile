SHELL = /bin/sh

install: requirements.txt
	pip install -r requirements.txt > success_log

