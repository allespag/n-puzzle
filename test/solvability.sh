while ((1))
do
	filename="solvability.log.rm"
	i=3
	solvable="-s"
	while (($i < 10)) 
	do
		python2 ../resources/npuzzle-gen.py $solvable $i > $filename
		python3 ../__main__.py --file $filename
		((i+=1))
	done
	i=0
done
exit 0
