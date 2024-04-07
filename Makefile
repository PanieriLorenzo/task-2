M10 = 10485760
G1 = 1073741824
G10 = 10737418240

genfile:
	# generate the dummy file to transfer
	mkdir -p data/
	head -c ${G1} /dev/urandom > data/bigfile.dat

clean:
	rm -r ./data || true
	rm ./bigfile.dat

client:
	./client.sh

attack:
	sudo -E env PATH=${PATH} python attack.py
