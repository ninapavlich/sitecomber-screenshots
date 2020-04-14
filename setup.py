from setuptools import setup, find_packages
# this is a test
setup(name='sitecomber-screenshots',
      description='Article screenshots for Sitecomber platform',
      version='0.0.1',
      url='https://github.com/ninapavlich/sitecomber-screenshots',
      author='Nina Pavlich',
      author_email='nina@ninalp.com',
      license='MIT',
      packages=find_packages(),
      package_data={'sitecomber_article_tests': ['*.py', '*.html', '*.css', '*.js', '*.jpg', '*.png']},
      include_package_data=True,
      install_requires=[],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved',
          'Operating System :: OS Independent',
          'Programming Language :: Python'
      ]
      )
