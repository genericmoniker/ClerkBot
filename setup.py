from setuptools import setup, find_packages

setup(
    name='ClerkBot',
    version='0.1',
    description='Handy LDS clerk scripts',
    author='Eric Smith',
    author_email='eric@esmithy.net',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    entry_points={
       'console_scripts': [
           'clerkbot = clerkbot.__main__:main'
       ]
    },
)
