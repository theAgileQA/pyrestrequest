import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Future is needed for pip distribution for python 3 support
dependencies = ['pyyaml', 'requests']
test_dependencies = ['django==1.6.5', 'django-tastypie==0.12.1', 'jsonpath', 'jmespath']

# Add additional compatibility shims
if sys.version_info[0] > 2:
    dependencies.append('future')  # Only works with direct local installs, not via pip
else:
    test_dependencies.append('mock')
    test_dependencies.append('discover')

setup(name='pyresttest',
      version='dev.2.0',
      description='Python RESTful API Testing & Microbenchmarking Tool',
      long_description='Python RESTful API Testing & Microbenchmarking Tool',
      author='refactored by Tamara Macul Mendes at OCI, based off Sam Van Oort pyresttest',
      author_email='mara.macul.mendes@oracle.com',
      url='https://github.corp.dyndns.com/InternetIntelligence/pyrestrequest',
      keywords=['rest', 'web', 'http', 'testing'],
      classifiers=[
          'Environment :: Console',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Utilities'
      ],
      py_modules=['pyresttest.resttest', 'pyresttest.generators', 'pyresttest.binding',
                  'pyresttest.parsing', 'pyresttest.validators', 'pyresttest.contenthandling',
                  'pyresttest.benchmarks', 'pyresttest.tests', 
                  'pyresttest.six',
                  'pyresttest.ext.validator_jsonschema',
                  'pyresttest.ext.extractor_jmespath',
                  'pyresttest.oci_signer', 'pyresttest.metric'],
      install_requires=dependencies,
      tests_require=test_dependencies,
      extras_require={
        'JSONSchema': ['jsonschema'],
        'JMESPath': ['jmespath']
      },
      # Make this executable from command line when installed
      scripts=['util/pyresttest', 'util/resttest.py'],
      provides=['pyresttest']
      )
