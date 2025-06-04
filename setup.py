from setuptools import setup, find_packages

setup(
    name='minimap2_simplified',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'biopython',
        'setuptools',
    ],
    author='Yukai Wang',
    author_email='wang.yukai@outlook.com',
    description='A simplified Python implementation of the Minimap2 alignment algorithm.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/wangyukai585/bio2502_final_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
