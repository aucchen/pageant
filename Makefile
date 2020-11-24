all:
	dendry make-html
	cp out/html/* ./
	zip game.zip *.js *.html *.css

deploy:
	butler push game.zip red-autumn/pageant:win-mac-linux
