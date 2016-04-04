.PHONY: output

output:
	dadaportal build canonical-articles --recursive

publish: output
	rsync --delete -asHSz output/ dadaportal:
