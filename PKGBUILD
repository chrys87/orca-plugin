# Maintainer: alex19EP <aarnaarn2@gmail.com>
# Contributor: Steve Holmes <steve.holmes88@gmail.com>
# Contributor: William Rea <sillywilly@gmail.com>

pkgname=orca-git
pkgver=41.0
pkgrel=1
pkgdesc="Screen reader for individuals who are blind or visually impaired (development version)"
arch=('any')
license=('LGPL')
url="https://wiki.gnome.org/Projects/Orca"
depends=('gtk3' 'at-spi2-atk' 'python-atspi' 'python-dbus' 'python-xdg'
         'speech-dispatcher' 'liblouis' 'brltty' 'xorg-xmodmap' 'gst-plugins-base'
         'gst-plugins-good' 'libpeas')
makedepends=('git' 'yelp-tools' 'itstool' 'intltool')
provides=('orca')
conflicts=('orca')
source=(${pkgname%-git}::'git+https://github.com/chrys87/orca-plugin.git')
md5sums=('SKIP')

prepare() {
	cd "${srcdir}/${pkgname%-git}"
	git checkout plugin_system
	./autogen.sh
}

build() {
	cd "${srcdir}/${pkgname%-git}"
	./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
	make
}

package() {
	cd "${srcdir}/${pkgname%-git}"
	make DESTDIR="${pkgdir}" install
}
