# Maintainer: Kwpolska <kwpolska@kwpolska.tk>
pkgname=pkgbuilder
pkgver=2.1.2.13
pkgrel=1
pkgdesc="A basic Python AUR helper/library."
arch=('any')
url="https://github.com/Kwpolska/pkgbuilder"
license=('BSD')
depends=('python' 'pyalpm>=0.5.1-1' 'python-pyparsing' 'pacman>=4.0.0-1')
options=(!emptydirs)
source=("http://pypi.python.org/packages/source/p/${pkgname}/${pkgname}-${pkgver}.tar.gz")
md5sums=('171434d2f351f855f9011bfe75632a1a')

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  python setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}

# vim:set ts=2 sw=2 et:
