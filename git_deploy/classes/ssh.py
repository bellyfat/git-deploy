"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__="Adam Schubert"
__date__ ="$6.7.2014 0:01:09$"

import StringIO
import paramiko
import socket
import os
import errno
  
class Ssh:
  connection = None
  ssh = None
  root = None
  
  def __init__(self, host, user, root = '/', port = 22, password = None):
    #paramiko.util.log_to_file('paramiko.log')
    self.root = root
    
    self.ssh = paramiko.SSHClient() 
    self.ssh.load_system_host_keys()
    self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    
    try:
      self.ssh.connect(host, port, user, password, None, None, 10)
    except (paramiko.SSHException, socket.error):
      raise Exception('Failed to connect to server!')
    
    try:
      self.connection = self.ssh.open_sftp() 
    except Exception as err:
      raise Exception( "Failed to start SFTP session from connection to {}. Check that SFTP service is running and available. Reason: {}".format( hostname, str(err) ))
    
  """
   * Method reads file from remote server
   * @param string $filePath path to file on remote server
   * @return string file content
  """
  def read_file(self, file_path):
    buf = StringIO.StringIO()
    try:
      opened_file = self.connection.open(file_path)
      for line in opened_file:
        buf.write(line)
      opened_file.close()
      
      return buf.getvalue()
    except Exception as err:
      raise Exception( "Failed load remote file {} Reason: {}".format( file_path, str(err) ))

  """
   * Method downloads file from remote server
   * @param string $filePath
   * @param string $fileTarget
   * @throws Exception
  """
  def get_file(self, file_path, file_target):
    self.connection.get(file_path, file_target)

  """
   * Uploads file on remote server
   * @param string $from
   * @param string $to
   * @param string $premisson
   * @throws Exception
  """
  def upload_file(self, from_file, to_file, premisson = 664):
    self.create_path(to_file, premisson)
    self.connection.put(from_file, to_file)
    if premisson:
      self.connection.chmod(to_file, premisson)
    
   
  """
   * Uploads string on remote server
   * @param string $filePath
   * @param string $string
   * @param string $premisson
  """
  def upload_string(self, file_path, string, premisson = 664):
    self.create_path(file_path, premisson)
    f = self.connection.open(file_path, 'wb')
    f.write(string)
    f.close()
    
    if premisson:
      self.connection.chmod(file_path, premisson)

  """
   * Deletes file on remote server
   * @param type $file
   * @throws Exception
  """
  def delete_file(self, file):
    self.connection.remove(file)

  """
   * Creates path on remote server
   * @param type $filePath
   * @param type $premisson
  """
  def create_path(self, file_path, premisson = 755):
    dir_path = os.path.dirname(file_path)
    try:
      self.connection.stat(dir_path)
    except IOError as e:
      if(e.errno == errno.ENOENT):
        try:
          self.connection.mkdir(dir_path, premisson)
        except IOError as e:
          raise Exception('Failed to create path {} on server Reason: {}'.format(dir_path, str(e)))
      else:
        raise Exception('Failed to stat path {} on server Reason: {}'.format(dir_path, str(e)))
  
