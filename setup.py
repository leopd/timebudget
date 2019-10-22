import setuptools

long_description = open('README.md', 'rt').read()

setuptools.setup(
     name='timebudget',
     version='0.6',
     author="Leo Dirac",
     author_email="leo.dirac@gmail.com",
     description="Simple performance profiling tool for python",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/leopd/timebudget",
     packages=['timebudget'],
     keywords="profiling tuning",
     license="Apache-2.0",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
     ],
)

