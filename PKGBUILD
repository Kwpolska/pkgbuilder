# Maintainer: Kwpolska <kwpolska@kwpolska.tk>
pkgname=pkgbuilder
pkgver=2.1.2.33
pkgrel=1
pkgdesc='A basic Python AUR helper/library.'
arch=('any')
url='https://github.com/Kwpolska/pkgbuilder'
license=('BSD')
depends=('python' 'pyalpm>=0.5.1-1' 'python-pyparsing' 'python-requests')
options=(!emptydirs)
source=('http://pypi.python.org/packages/source/p/${pkgname}/${pkgname}-${pkgver}.tar.gz')
md5sums=('11fbf28053ffd992add0250787581058')

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  python setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}

# vim:set ts=2 sw=2 et:
