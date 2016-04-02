.PHONY: output

output:
	dadaportal build canonical-articles --recursive

deploy: output
	rsync --delete -asHSz output/ dadaportal:
