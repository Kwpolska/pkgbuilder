# Maintainer: Kwpolska <kwpolska@kwpolska.tk>
pkgname=pkgbuilder
_pyname=pkgbuilder
pkgver=3.0.0
pkgrel=1
pkgdesc='A Python AUR helper/library.'
arch=('any')
url='https://github.com/Kwpolska/pkgbuilder'
license=('BSD')
depends=('python' 'pyalpm>=0.5.1-1' 'python-requests' 'rsync')
options=(!emptydirs)
source=("http://pypi.python.org/packages/source/$(echo ${_pyname} | cut -c1)/${_pyname}/${_pyname}-${pkgver}.tar.gz")
md5sums=('8a4e02f3c319e2fb499b4dc254ae725f')

package() {
  cd "${srcdir}/${_pyname}-${pkgver}"
  python3 setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}

# vim:set ts=2 sw=2 et:
