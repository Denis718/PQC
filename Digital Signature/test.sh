rm PQCsignKAT.rsp
for dir in $(find . -mindepth 1 -maxdepth 1 -type d);do
	echo $dir
	cp ./PQCgenKAT_sign.c $dir
	cd $dir
	make &
	wait
	./PQCgenKAT_sign $dir &
	wait
	cat PQCsignKAT.rsp >> ../PQCsignKAT.rsp
	cd -
done
