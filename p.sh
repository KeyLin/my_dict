git add .
if [ '$1' == '0' ]; then
	git commit -m '\$1'
else
	git commit -m 'default'
fi