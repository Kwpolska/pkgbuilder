# Maintainer: Kwpolska <kwpolska@gmail.com>
pkgname=pkgbuilder
pkgver=2.1.0
pkgrel=1
pkgdesc="A basic Python AUR helper/library."
arch=('any')
url="https://github.com/Kwpolska/pkgbuilder"
license=('BSD')
depends=('python' 'pyalpm' 'python-pyparsing')
options=(!emptydirs)
source=('http://pypi.python.org/packages/source/p/pkgbuilder/pkgbuilder-2.1.0.tar.gz')
md5sums=('d6f495345dde0cb3774dc9f3f3eafaaa')

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  python setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}

# vim:set ts=2 sw=2 et:
