��    r      �  �   <      �	  �  �	    �     �     �     �     �     �  "   �  "        <     K     e     �  (   �  $   �     �  '   
     2  *   B     m     �     �  +   �  R   �     A     \     c     ~  5   �  '   �     �     
  �   #          7     U  &   r     �  �   �  �   �  (   3     \     v     {     �     �     �     �  R   �           ;      \  !   }     �  1   �     �               9     Y  "   p     �  +   �  0   �  :      !   ;     ]     f  &   t     �     �  &   �  ,   �  2   &     Y     t     �  !   �     �     �     �  2   �          )  
   ,  	   7  
   A     L     _     g  (   x     �     �  #   �     �     	     &  +   =     i     �  �   �     �     �  9   �     �     �     �               1  (   D     m     �  �  �    N  :  j     �   	   �      �      �      �   &   �   &   !     @!  "   Q!  6   t!  "   �!  :   �!  3   	"  %   ="      c"     �"  (   �"  !   �"      �"     #  +   "#  M   N#     �#     �#     �#     �#  :   �#  *    $     K$     g$  �   �$  )   ~%  "   �%     �%  0   �%  !   &  �   <&  �   )'  .   �'  $   (     5(     ;(     U(     b(     x(     �(  \   �(  %   �(  (   )  %   7)      ])     ~)  ]   �)     �)     *  !   0*  +   R*     ~*  (   �*     �*  (   �*  "   �*  F   +      `+     �+     �+  -   �+  9   �+     ,  +   ,  ?   I,  8   �,     �,     �,     �,  $   -     *-     <-     M-  2   \-     �-     �-     �-     �-  
   �-     �-     �-     �-  2   .     8.     O.     c.  #   �.  &   �.     �.  /   �.  $   /  	   9/    C/     S0     k0  7   q0     �0     �0     �0     �0     �0     �0  -   1     51     L1           &   -   8       p   3   '   I   1           S   ^         k       i   7                  +       _   b   ?   ,   E   0                              *                  "       H      d   $       \   P      h       ;   j       <                   6   [   g   B             N   =       (   L       !      f       T          @      o   `   ]   A      M      /   m   4   r   #           C           l   )   Q      q   K   %   
   Z   c   2   J       e       X       W          O          F   R       >   9   5       a          V   n       G       U      .           	   Y   :   D                 

Read the above output.  If the script had any problems, run it
again.  You can also try to debug the work of this script yourself.
All the files this script was working on are placed in
    {0}
(the number is random).

If everything went fine, though, congratulations!  You can now use
PKGBUILDer.  For standalone usage, type `pkgbuilder` into the prompt
(zsh users: hash -r, other shells may need another command).  For
python module usage, type `import pkgbuilder` into the python prompt.
 

Something went wrong.  Please read makepkg's output and try again.
You can also try to debug the work of this script yourself.
All the files this script was working on are placed in
    {0}
(the number is random).

If I am wrong, though, congratulations!
  [installed: {0}]  [installed] %(prog)s <operation> [...] (dummy) 0 bytes downloaded :: Retrieving packages from abs... :: Retrieving packages from aur... AUR Error: {0} AUR/ABS packages to build Aborted by user! Exiting... Also accepting ABS packages. An AUR helper (and library) in Python 3. Build finished with return code {0}. Build the git version? [y/N]  Building more AUR packages is required. Building {0}... Cannot create the configuration directory. Checking dependencies... Connection error: {0} (via {1}) Didn’t pass any packages. Do you want to cancel the current operation Do you want to cancel the current operation and upgrade these packages now? [Y/n]  Downloading the tarball... ERROR: Extracting AUR packages... Extracting... Failed to fulfill package dependency requirement: {0} Failed to retieve {0} (from ABS/rsync). Fetching package information... HTTP Error {0} (via {1}) Hello!

PKGBUILDer is now available as an AUR package.  It is the suggested
way of installing PKGBUILDer.  This script will download the AUR
package and install it.  If you will have problems, please download
and compile the package manually.

 Hit Enter/Return to continue.  Initializing pacman access... Installing built packages... Installing missing AUR dependencies... Interrupt signal received
 It looks like you want to quit.  Okay then, goodbye.
All the files this script was working on are placed in
    {0}
(the number is random).

If that's what you want to do, go for it.  If it isn't, run this
script again. It looks like you want to quit.  Okay then, goodbye.
No work has been started yet.

If that's what you want to do, go for it.  If it isn't, run this
script again. LANG locale by AUTHOR <MAIL@IF.YOU.WANT> Logs will not be created. Name Network error: {0} (via {1}) New Version No files extracted. Old Version PACKAGE PKGBUILDer (or the requests library) had problems with fulfilling an HTTP request. PKGBUILDer Failsafe Upgrade Package {0} not found. (via {1}) Performing a dependency check... Proceed with installation? [Y/n]  Retrieving from ABS... Running PKGBUILDer as root can break your system! Sanity error!  {0} (via {1}) Search query too short Searching for exact match... Starting full system upgrade... Successfully fetched:  Synchronizing package databases... Targets ({0}):  The build function reported a proper build. The following packages should be upgraded first: Trying to use utils.print_package_info with an ABS package Validating installation status... WARNING: [out of date] and upgrade these packages now? [Y/n]  clean up work files after build display debug messages don't  install packages after building don't check dependencies (may break makepkg) don't check if packages were installed after build don't use colors in output fetch package files found found an existing package for {0} found in repos found in system found in the AUR makepkg (or someone else) failed and returned {0}. makepkg returned {0}. no none found not found operations optional arguments options pacman-like mode perform a failsafe upgrade of PKGBUILDer positional arguments retrieving {0} search the AUR for matching strings show this help message and exit show version number and quit there is nothing to do upgrade all the VCS/date-versioned packages upgrade installed AUR packages usage usage:  {0} <operation> [...]

PBWrapper, a wrapper for pacman and PKGBUILDer.

{1}

Pacman and PKGBUILDer syntaxes apply.  Consult their manpages/help
commands for more details.

Additional options:
  -L, --unlock         unlock the pacman database view package information votes warning: insufficient columns available for table display yes {0} (Package: {1}) {0} files extracted {0} kB downloaded {0}: NOT installed {0}: installed {1} {0}: local ({1}) is newer than aur ({2}) {0}: not an AUR package {0}: outdated {1} Project-Id-Version: 3.3.1
Report-Msgid-Bugs-To: Kwpolska <kwpolska@kwpolska.tk>
POT-Creation-Date: 2014-05-31 12:42+0200
PO-Revision-Date: 2014-02-04 16:11+0000
Last-Translator: Kwpolska <kwpolska@gmail.com>
Language-Team: Turkish (http://www.transifex.com/projects/p/pkgbuilder/language/tr/)
Language: tr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n > 1);
 
⏎
⏎
Yukarıdaki çıktıyı okuyun. Script hata verirse yeniden çalıştırın.⏎
Script çalışmasındaki hatayı kendiniz de giderebilirsiniz.⏎
Script in çalışması için gerekli dosyalar {0} içindedir.⏎
(the number is random).⏎
⏎
Her şey yolunda ise tebrikler! Şimdi PKGBUILD yapıcıyı kullanabilirsiniz.⏎
Kullanmak için uçbirime `pkgbuilder` yazın⏎
(zsh kullanıcılar: hash -r, diğer kabuklar başka komutlar isteyebilir).⏎
Python modülü için python uçbirimine ⏎
`import pkgbuilder` yazın.⏎
 
⏎
⏎
Bir şeyler ters gitti. Lütfen makepkg çıktısını okuyun ve tekrar deneyin.⏎
Script çalışmasının hata onarımını kendiniz de yapabilirsiniz .⏎
Script in çalışmak için kullandığı tüm dosyalar⏎
{0} içindedir⏎
(rakam rastgeledir).⏎
⏎
Eğer hatalıysam, yine de tebrikler!⏎
 [Kurulan: {0}] [Kuruldu] %(prog)s <operation> [...] (sahte) o byte indirildi :: ABS den paketler geri alınıyor... :: AUR dan paketler geri alınıyor... AUR Hatası: {0}  İnşa edilecek AUR/ABS paketleri Kullanıcı tarafından iptal edildi! Çıkılıyor... Ayrıca ABS paketi kabul ediliyor. Python 3 içinde bir AUR yardımcısı (ve kütüphanesi). İnşa işlemi {0}geri dönüş kodu ile bitirildi. Git sürümü inşa edilsin mi? (E/H) Daha fazla AUR paketi gerekiyor. {0} İnşa ediliyor... Yapılandırma dizini oluşturulamıyor. Bağımlılıklara bakılıyor... Bağlantı hatası:{0} (via {1}) Hiç bir paket atlanmadı. Geçerli işlemi iptal etmek istiyormusunuz Geçerli işlemi sonlandırıp bu paketleri yükseltmek istiyormusunuz? [E/H] Tarball indiriliyor... HATA: AUR paketleri açılıyor... Açılıyor... Paket bağımlılığı şartı gerçekleştirilemedi :{0} {0} geri yüklenmesi durdu (ABS/rsync ten) Paket bilgisi alınıyor... HTTP hatası {0} (via {1}) Merhaba!⏎
⏎
PKGBUILD yapıcı şimdi AUR paketi olarak mevcut. Bu PKGBUILD yapıcı⏎
yüklemek için önerilen yoldur. Bu script AUR paketini indirip yükleyecektir.⏎
Eğer sorun yaşarsanız lütfen paketi indirin ve kendiniz derleyin⏎
⏎
 Geri dönmek için Enter/Dön tuşlayın. Pacman erişimi başlatılıyor... İnşa paketleri kuruluyor... Kurulum AUR bağımlılıklarını bulamıyor... Sinyal kesilmesi algılandı⏎

 Çıkmak istiyor gibisiniz. Pekala hoşçakalın. ⏎ Bu script ile çalışan tüm dosyalar ⏎ {0}⏎  içinde.(numara rastgeledir). ⏎ ⏎ Eğer yapmak istediğiniz bu ise devam edin. Değilse bu ⏎ script i tekrar çalıştırın. Çıkmak istiyor gibisibiz.Pekala öyleyse hoşçakalın.⏎
Henüz herhangi bir işlem başlamadı.⏎
⏎
İstediğiniz bu ise devam edin. Değilse bu scrpt i⏎
yeniden başlatın. Dil yerelleştirmesini yapan yfdogan@gmail.com Kayıt dosyaları oluşturulamıyor. İsim {0} (via {1}) Ağ hatası Yeni sürüm Bir dosya açılmadı Eski sürüm PAKET PKGBUILD yapıcı (ya da istenen kütüphane) HTTP istemcisini doldurmada başarısız oldu. PKGBUILD yapıcı güvenli yükseltme {0} Paketi (via {1}) içinde bulunamadı Bağımlılık kontrolü yapılyor... Kuruluma devam edilsin mi? [E/H] ABS den geri alınıyor... PKGBUILD yapıcı yı yetkili kullanıcı hakları ile çalıştırmak sisteminizi bozabilir! Mantık hatası : {0} (via {1}) Arama sorgusu çok kısa Tam eşleşme için taranıyor... Tam sistem  yükseltmesi başlatılıyor... Başarıyla çekildi: Paket veritabanları eşleştiriliyor... Hedefler ({0}): İnşa işlemi uygun bir inşa bildirdi. Şu paketler önce yükseltilecek: ABS paketi ile utils.print_package_info kullanılmaya çalışılıyor Yükleme durumu hesaplanıyor... DİKKAT: [Günü geçmiş] ve bu paketler şimdi yükseltilsin mi? [E/H] İnşa işleminden sonra çalışma dosyalarını temizle Hata iletilerini göster İnşa işleminden sonra paketleri yükleme Bağımlılıkları kontrol etme (makepkg işlemini kırabilir) Paketler inşa işleminden sonra kurulduysa kontrol etme Çıktı içinde renk kullanma Paket dosyaları çekiliyor bulundu {0} için var olan bir paket bulundu Depolarda bulundu Sistemde bulundu AUR da bulundu makepkg (veya biri) durduruldu ve geri döndü {0} {0} makepkg geri döndü. hayır Bulunamadı Bulunamadı İşlemler seçimli argümanlar Seçenekler pacman-like modu PKGBUILD yapıcı için güvenli yükseltme yapın pozisyonel argümanlar {0} geri alınıyor Eşleşmeler için AUR u tara yardım mesajını göster ve çık Sürüm numarasını göster ve çık. Yapılacak bir şey yok Bütün VCS/tarih-sürümlü paketleri yükselt Yüklenmiş AUR paketlerini yükselt kullanım kullanım: {0} <işlem> [...]⏎
⏎
PBWrapper, PKGBUIL yapıcı ve pacman için örtü.⏎
⏎
{1}⏎
⏎
Pacman and PKGBUILDer syntaxes apply. Consult their manpages/help⏎
commands for more details.⏎
⏎
Additional options:⏎
-L, --pacman veri tabanı kilidini aç Paket bilgisini göster oylar uyarı: tablo görünümü için yetersiz sütunlar var evet {0} (Paket: {1}) {0}: dosya açıldı {0}: kb indirildi {0}: KURULMADI {0}: KUurulan {1} {0}: yerel ({1}) aur daki ({2}) den daha yeni {0}: AUR paketi değil {0}: Günü geçmiş {1} 