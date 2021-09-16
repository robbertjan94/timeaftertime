import setuptools

setuptools.setup(
    name="timeaftertime",
    version="0.0.1",
    url="",
    author="Robbert-Jan 't Hoen",
    author_email="robbertjanthoen@gmail.com",
    description="Package for 'Keer op Keer 2'",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    package_data={'': ['data/']}
)