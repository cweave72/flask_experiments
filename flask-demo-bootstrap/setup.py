from setuptools import setup

setup(
    name='flask-demo-bootstrap',
    packages=['flask-demo-bootstrap'],
    include_package_data=True,
    install_requires=[
        'flask',
        'bootstrap-flask',
        'rich',
    ],
)
