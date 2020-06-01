from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()


requirements = [
    "numpy",
    "pandas",
]


if __name__ == "__main__":
    setup(
        name='animanager',
        version='0.1.0',
        description='quick fix for managing animals in the lab.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Jose Cruz',
        packages=find_packages(),
        include_package_data=True,
        author_email='jose.cruz@nyu.edu',
        license='GNU-3',
        install_requires=requirements,
    )

########## More information
# https://python-packaging-user-guide.readthedocs.io/tutorials/packaging-projects/
