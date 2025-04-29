# Maintainer: Your Name <your.email@example.com>
pkgname=silent-search
pkgver=0.1.0
pkgrel=1
pkgdesc="A powerful command-line tool for searching and managing files by name and type"
arch=('any')
url="https://github.com/yourusername/silent-search"
license=('MIT')
depends=('python' 'python-click' 'python-toml')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir/" --optimize=1
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
} 