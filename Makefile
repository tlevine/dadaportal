.PHONY: output

output:
	dadaportal build canonical-articles --recursive

deploy: output
	rsync -asHSz output/ dadaportal:
