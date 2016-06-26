tests:
	python runtests.py

release:
	rm -r dist
	python setup.py sdist bdist_wheel
	twine upload dist/*

changelog: 
	git changelog -a docs/changelog.rst

tags:
	ctags -R **/*.py

clean:
	rm -rf build dist 
