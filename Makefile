all:
	make install-reqs
	pip3 install pyinstaller
	python3 -m PyInstaller --windowed --onedir --name="One Button Pong" pong.py
install-reqs:
	pip3 install -r requirements.txt
clean:
	rm -f *.spec
	rm -rf dev
	rm -rf build
	rm -rf __pycache__
