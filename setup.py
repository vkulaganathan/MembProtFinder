from setuptools import setup, find_packages

setup(
    name='MembProtFinder',
    version='0.0.3',
    description='A tool to identify transmembrane proteins from a given list of gene or protein IDs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pr (France). Dr. rer. nat. Vijay K. ULAGANATHAN',
    author_email=' ',  # Add your email address here
    url='https://github.com/vkulaganathan/MembProtFinder',
    packages=find_packages(),
    scripts=['MembProtFinder.py'],
    install_requires=[
        'pandas',
        'pysqlcipher3',
        'configparser',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'MembProtFinder=MembProtFinder:main',
        ],
    },
)

