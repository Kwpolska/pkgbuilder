# Maintainer: Kwpolska <kwpolska@kwpolska.tk>
pkgname=pkgbuilder
pkgver=2.1.4.6
pkgrel=1
pkgdesc='A Python AUR helper/library.'
arch=('any')
url='https://github.com/Kwpolska/pkgbuilder'
license=('BSD')
depends=('python' 'pyalpm>=0.5.1-1' 'python-requests')
options=(!emptydirs)
source=("http://pypi.python.org/packages/source/p/${pkgname}/${pkgname}-${pkgver}.tar.gz")
md5sums=('987ed30c5329d3f2ed6744adb9de0fc7')

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  python3 setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}

# vim:set ts=2 sw=2 et:
