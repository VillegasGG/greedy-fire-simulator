from setuptools import setup, find_packages

setup(
    name='greedyff',
    version='0.1.0',
    description='A greedy simulation for firefighter problem',
    author='Getsemani Villegas',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'networkx',
        'matplotlib',
        'pandas',
        'scipy',
        'tqdm',
        'jsonschema'
    ],
    python_requires='>=3.6',
)