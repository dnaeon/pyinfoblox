from setuptools import setup

setup(name='pyinfoblox',
      version='0.1.1',
      description='Infoblox WAPI module for Python',
      long_description=open('README.rst').read(),
      author='Marin Atanasov Nikolov',
      author_email='dnaeon@gmail.com',
      license='BSD',
      url='https://github.com/dnaeon/pyinfoblox',
      download_url='https://github.com/dnaeon/pyinfoblox/releases',
      packages=['pyinfoblox'],
      install_requires=[
        'requests >= 2.4.3',
      ]
)
