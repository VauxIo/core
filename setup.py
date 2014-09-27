from setuptools import setup, find_packages

requires = [
    'rethinkdb',
    'flask',
    'gevent'
]

setup(
    name='docliber',
    version='0.1.0',
    description='Document Liberation',
    packages=find_packages(),
    install_requires=requires,
    zip_safe=False
)
