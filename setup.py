from distutils.core import setup


setup(
    name='logstashHandler',
    version='0.1.3',
    packages=['logstashHandler'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Log handler that ships json formatted messages to logstash via TCP and UDP',
    long_description=open('README.txt').read(),
    author='Stewart Rutledge',
    author_email='stew.rutledge@gmail.com',
    url='https://github.com/stewrutledge/logstashHandler'
)
