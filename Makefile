all: test sleep clean

test :
	mkdir tmp/test
	touch tmp/test/testfile1
	touch tmp/test/testfile2
	mv tmp/test/testfile1 tmp/test/testfile3
	touch tmp/test/testfile2 #modify timestamp

clean:
	rm -rf tmp/test

sleep:
	sleep 2
