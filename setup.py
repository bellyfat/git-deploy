#!/usr/bin/env python2

from setuptools import setup

__author__="Adam Schubert"
__date__ ="$8.7.2014 20:26:41$"

if 'initd' in open('.target').read():
  data_files_dist=[
    ('/etc/init.d', ['etc/init.d/git-deploy']), ('/etc/git-deploy', ['etc/git-deploy/config.py'])
  ] 
else:
  data_files_dist=[
    ('/usr/lib/systemd/system/', ['usr/lib/systemd/system/git-deploy.service']), ('/etc/git-deploy', ['etc/git-deploy/config.py'])
  ]
  
setup(
  name="git-deploy",
  version=open('VERSION.txt').read(),
  author=__author__,
  author_email="adam.schubert@sg1-game.net",
  description="Git-deploy is tool written in python to allow fast and easy deployments on remote servers wia S/FTP, SSH/SCP",
  long_description=open('README.md').read(),
  license="GPL",
  install_requires=['paramiko', 'flask'],
  url="https://github.com/Salamek/git-deploy",
  packages=['git_deploy', 'git_deploy/classes'],
  package_dir={'git_deploy': 'git_deploy'},
  #package_data={},
  entry_points={
    'console_scripts': ['git-deploy = git_deploy:main']
  },
  data_files=data_files_dist
)
