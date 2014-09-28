from setuptools import setup, find_packages

requires = [
    'rethinkdb',
    'flask',
    'flask-restful',
    'gevent',
    'requests',
    'PyPDF2',
]

setup(
    name='vaux',
    version='0.1.0',
    description='Document Liberation',
    packages=find_packages(),
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    vaux_ingest = vaux.scripts:load_from_fs
    """
)
