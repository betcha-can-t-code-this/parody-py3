import setuptools

setuptools.setup(
	name="parody-py3",
	version="1.0.0",
	author="Paulus Gandung Prakosa",
	author_email="gandung@lists.infradead.org",
	description="Funny VM bytecode engine.",
	url="https://github.com/betcha-can-t-code-this/parody-py3",
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	python_requires=">=3.6"
)
