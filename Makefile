all:
	chmod +x build.py
	python build.py
	sudo cp -r dist/* /usr/local/bin