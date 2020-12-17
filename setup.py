from distutils.core import setup
from common import VERSION

setup(
    name='django_common_api',  # How you named your package folder (MyLib)
    packages=['common'],  # Chose the same as "name"
    version=VERSION,  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='App for better API management.',  # Give a short description about your library
    author='Bhaskar Neupane',  # Type in your name
    author_email="vaskrneup@gmail.com",  # Type in your E-Mail
    url='https://github.com/vaskrneup/django_contrib_common',
    keywords=['python', 'django'],  # Keywords that define your package best
    install_requires=[
        "django"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
