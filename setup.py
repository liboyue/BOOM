from distutils.core import setup

setup(
        name = 'boom',
        version = '0.1',
        description = 'An easy-to-use configuration space exploration pipeline framework.',
        author = 'Boyue Li, Nicholas Gekakis',
        author_email = 'me@boyue.li, ngekakis@andrew.cmu.edu',
        license = 'MIT',
        url = 'https://https://github.com/liboyue/BOOM/',
        #project_urls={
        #    'Documentation': 'https://boom.boyue.li/',
        #    'Source Code': 'https://https://github.com/liboyue/BOOM/',
        #},
        scripts = ['bin/boom'],
        packages = ['boom', 'boom.modules']
     )
