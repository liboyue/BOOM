from distutils.core import setup

setup(name='src',
      version='0.0.0',
      scripts=['bin/boom'],
      description='An easy-to-use question answering pipeline framework.',
      author='Boyue & Nico',
      author_email='boyuel@andrew.cmu.edu',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['src', 'src.modules', 'src.modules.bioasq']
     )
