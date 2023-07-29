from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        name='pymage-processor',
        version='1.0.1',
        author='Rodrigo Martins',
        description='Image processor',
        packages=find_packages(where='src', exclude=['tests']),
        entry_points= {
            'console_scripts': [
                'pymage = pymage.__main__:main'
            ]
        },
        install_requires=[
            'Pillow>=9.3.0',
            'altgraph>=0.17.2',
            'tk>=0.1.0'
        ],
        python_requires='>=3.8',
        zip_safe=False,
        package_dir={'': 'src'},
        include_package_data=True,
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown'
    )