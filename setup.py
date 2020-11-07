from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AShareData',
    version='0.0.1',
    description='Gather data for A share and store in MySQL database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jicewarwick/AShareData',
    author='Ce Ji',
    author_email='Mr.Ce.Ji@outlook.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tushare mysql',
    packages=find_packages(exclude=['docs', 'tests', 'AShareData/complimentary_code']),
    python_requires='>=3.5, <4',
    install_requires=['numpy',
                      'pandas',
                      'tushare',
                      'sqlalchemy',
                      'tqdm',
                      'requests',
                      ],
    package_data={
        'json': ['data/*.json'],
    },
    entry_points={
        'console_scripts': [
            'sample=A_share_data_update_routine:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/jicewarwick/AShareData/issues',
        'Source': 'https://github.com/jicewarwick/AShareData',
    },
)
