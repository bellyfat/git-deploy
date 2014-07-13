# Maintainer: Adam Schubert <adam.schubert@sg1-game.net>

pkgname=git-deploy
pkgver=2.0.5
pkgrel=1
pkgdesc="Git-deploy is tool written in python to allow fast and easy deployments on remote servers wia S/FTP, SSH/SCP"
arch=('any')
license=('GPL')
url='https://github.com/Salamek/git-deploy'
depends=('python2'
 'python2-paramiko'
 'python2-twisted'
 'git')
backup=('etc/git-deploy/git-deploy.cfg')
makedepends=()
source=("https://github.com/Salamek/git-deploy/archive/$pkgver.tar.gz")
noextract=()
md5sums=('0021d34ba6d36daa6eae75928dc46d3e')

package() {
  cd "$srcdir/$pkgname-$pkgver"
  chmod +x ./setup.py
  ./setup.py install --root=$pkgdir/ --optimize=1
}