# Maintainer: Kwpolska <kwpolska@kwpolska.tk>
pkgname=pkgbuilder
pkgver=2.1.1.1
pkgrel=1
pkgdesc="A basic Python AUR helper/library."
arch=('any')
url="https://github.com/Kwpolska/pkgbuilder"
license=('BSD')
depends=('python' 'pyalpm' 'python-pyparsing')
options=(!emptydirs)
source=("http://pypi.python.org/packages/source/p/${pkgname}/${pkgname}-${pkgver}.tar.gz")
md5sums=('be6d2f31b0a13c7af4e0b1f88f1d0d2b')

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  python setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}

# vim:set ts=2 sw=2 et:
