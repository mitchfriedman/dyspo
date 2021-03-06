import setuptools


setuptools.setup(
    name='dyspo',
    version='0.0.2',
    author='Mitchell Friedman',
    author_email='mitchfriedman5@gmail.com',
    description='A web framework',
    url='https://github.com/mitchfriedman/dyspo',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp==3.3.2',
        'async-timeout==3.0.0',
        'attrs==18.1.0',
        'chardet==3.0.4',
        'idna==2.7',
        'idna-ssl==1.1.0',
        'multidict==4.3.1',
        'yarl==1.2.6',
    ]
)
