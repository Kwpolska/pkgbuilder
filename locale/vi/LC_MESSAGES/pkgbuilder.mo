��    h      \  �   �      �  �  �    �
     �     �     �     �     �  "     "   1     T     c     }     �  (   �  '   �       *        B     [     {     �     �     �     �  5   �  '        @     `  �   y     n     �     �  &   �     �  �   
  �   �  (   �     �     �     �     �     �            R   "      u      �  !   �     �     �          $     A     a  "   x     �  +   �  :   �  !        4     =     K     k  ,   �  2   �     �     �       !        9     H     X  2   i     �     �  
   �  	   �  
   �     �     �     �            #   %     I     i     �  +   �     �     �  �   �     �       9        A     E     X     l     ~     �  (   �     �     �  �  �  S  �  �       �     �     �              0   /   1   `      �   *   �   4   �   $   !  H   &!  9   o!     �!  *   �!  &   �!  '   "  -   <"  *   j"     �"  .   �"     �"  b   �"  -   B#  5   p#     �#  S  �#  %   %  (   @%  *   i%  >   �%     �%  `  �%    T'  ;   b(  &   �(     �(  *   �(     �(  '   )     0)     A)  j   R)  B   �)  5    *     6*     V*  ,   o*  "   �*  '   �*  :   �*     "+  @   @+     �+  X   �+  J   �+  -   9,     g,     t,  1   �,  "   �,  B   �,  Q   -  L   p-  %   �-     �-  B   �-  %   7.  ,   ].  #   �.  P   �.     �.     /     /     1/     D/     R/     j/     v/     �/     �/  )   �/  2   �/  )   0  0   <0  ?   m0  /   �0     �0  T  �0     >2     ^2  ]   k2     �2     �2     �2     3     3     ?3  ,   Y3  .   �3     �3     c   I           `              S       8       g       _   +   ^   &   T          G      C       h   Y       \   <          B       a   K      P   U      6   7   1      0   [              M         	   -         /   A   '             5   L   >                  W   "      e       .   J       3   ?       ]   $         H          Z   9   D       O       
             V              d           *   ,   #       f   b             !      Q       X      4   @   F       (   ;   )      R   N   E      =   :   2       %            

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
  [installed: {0}]  [installed] %(prog)s <operation> [...] (dummy) 0 bytes downloaded :: Retrieving packages from abs... :: Retrieving packages from aur... AUR Error: {0} AUR/ABS packages to build Aborted by user! Exiting... Also accepting ABS packages. An AUR helper (and library) in Python 3. Building more AUR packages is required. Building {0}... Cannot create the configuration directory. Checking dependencies... Connection error: {0} (via {1}) Didn’t pass any packages. Downloading the tarball... ERROR: Extracting AUR packages... Extracting... Failed to fulfill package dependency requirement: {0} Failed to retieve {0} (from ABS/rsync). Fetching package information... HTTP Error {0} (via {1}) Hello!

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
script again. LANG locale by AUTHOR <MAIL@IF.YOU.WANT> Logs will not be created. Name Network error: {0} (via {1}) New Version No files extracted. Old Version PACKAGE PKGBUILDer (or the requests library) had problems with fulfilling an HTTP request. Package {0} not found. (via {1}) Performing a dependency check... Proceed with installation? [Y/n]  Retrieving from ABS... Sanity error!  {0} (via {1}) Search query too short Searching for exact match... Starting full system upgrade... Successfully fetched:  Synchronizing package databases... Targets ({0}):  The build function reported a proper build. Trying to use utils.print_package_info with an ABS package Validating installation status... WARNING: [out of date] clean up work files after build display debug messages don't check dependencies (may break makepkg) don't check if packages were installed after build don't use colors in output fetch package files found found an existing package for {0} found in repos found in system found in the AUR makepkg (or someone else) failed and returned {0}. makepkg returned {0}. no none found not found operations optional arguments options pacman-like mode positional arguments retrieving {0} search the AUR for matching strings show this help message and exit show version number and quit there is nothing to do upgrade all the VCS/date-versioned packages upgrade installed AUR packages usage usage:  {0} <operation> [...]

PBWrapper, a wrapper for pacman and PKGBUILDer.

{1}

Pacman and PKGBUILDer syntaxes apply.  Consult their manpages/help
commands for more details.

Additional options:
  -L, --unlock         unlock the pacman database view package information votes warning: insufficient columns available for table display yes {0} (Package: {1}) {0} files extracted {0} kB downloaded {0}: NOT installed {0}: installed {1} {0}: local ({1}) is newer than aur ({2}) {0}: not an AUR package {0}: outdated {1} Project-Id-Version: 3.4.0
Report-Msgid-Bugs-To: Chris Warrick <chris@chriswarrick.com>
POT-Creation-Date: 2015-01-01 11:49+0100
PO-Revision-Date: 2014-12-26 19:51+0000
Last-Translator: Chris Warrick <kwpolska@gmail.com>
Language-Team: Vietnamese (http://www.transifex.com/projects/p/pkgbuilder/language/vi/)
Language: vi
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
 

Đọc phần dữ liệu được xuất ra bên trên.  Nếu các đoạn mã lệnh gặp vấn đề, hãy chạy lại các đoạn mã lệnh này một lần nữa.  Bạn cũng có thể tự mình sửa phần gỡ rối này.
Tất cả các tập tin mà đoạn mã lệnh này tác động tới được đặt ở
    {0}
(con số này là ngẫu nhiên).

INếu như lỗi này thuộc về nhà phát triển, bạn hãy liên hệ với chúng tôi!  Bạn hiện giờ đã có thể sử dụng
PKGBUILDer.  Đối với kiểu dùng theo dạng tập tin tự chay, gõ `pkgbuilder` vào trong cửa sổ mã lệnh
(người dùng zsh: hash -r, các shell khác sẽ cần thêm một dòng lệnh nữa).  Đối với cách sử dụng module Python, gõ `import pkgbuilder` vào trong cửa sổ mã lệnh của python.
 

Đã xảy ra lỗi.  Vùi lòng đọc dữ liệu xuất ra của makepkg và thử lại lần nữa.
Bạn cũng có thể tự mình sửa các gỡ rối dựa vào đoạn mã lênh này theo ý bạn.
Tất cả các tập tin mà đoạn mã lệnh này tác động tới được đặt ở
    {0}
(con số này là ngẫu nhiên).

Nếu như lỗi này thuộc về nhà phát triển, bạn hãy liên hệ với chúng tôi!
  [đã cài đặt: {0}]  [đã cài đặt] %(prog)s <operation> [...] (dummy) 0 byte đã tải về :: Đang nhận các gói cài đặt từ abs.. :: Đang nhận các gói cài đặt từ aur... Lỗi AUR: {0} Gói cài đặt AUR/ABS để xây dựng Được hủy bởi người dùng! Đang thoát... Chấp nhaạn gói cài đặt ABS. Tập tin trợ giúp AUR (và thư viện) ở định dạng Pythong 3 Yêu cầu việc xây dựng thêm nhiều gói tin AUR. Đang xây dựng {0}... Không thể tạo thư mục cấu hình. Đang kiểm tra tính độc lập... Lỗi kết nối: {0} (thông qua {1}) Vẫn chưa thông qua gói cài đặt nào. Đang tải về các tập tin tarball... LỖI: Đang giải nén các gói cài đặt AUR... Đang giải nén.. Thất bại trong việc điền vào các yêu cầu về sự phụ thuộc của gói tin: {0} Thất bại khi nhận {0} (từ ABS/rsync). Đang tải về thông tin của gói cài đặt... Lỗi HTTP {0} (thông qua {1}) Xin chào!

PKGBUILDer hiện là gói cài đặt AUR. Đây hiện là cách cài đặt
được khuyên dùng đối với PKGBUILDer.  Phần mã lệnh này sẽ tải về gói tin AUR
và tiến hành cài đặt.  Nếu gặp phải trục trặc, xin vui lòng tải về
và biên dịch các gói tin một cách tuần tự.

 Ấn Enter/Return để tiếp tục. Đang thiết lập truy cập pacman... Đang cài đặt các gói dữ liệu... Đang cài đặt các phần AUR độc lập còn thiếu... Đã nhận tín hiệu ngắt
 Có vẻ như bạn đang muốn thoát.  Nếu vậy, xin chào tạm biệt.
Tất cả các tập tin mà đoạn mã lệnh này tác động tới được đặt ở
    {0}
(con số này là ngẫu nhiên).

Nếu đó là điều bạn muốn thao tác, cứ tiếp tục.  Nếu không phải, chạy lại
đoạn mã này một lần nữa. Có vẻ như bạn muốn thoát. Nếu thế thì, chào tạm biệt.
Hiện các công việc vẫn chưa được thực hiện.

Nếu đây là điều bạn muốn, xin cứ tiếp tục. Nếu không phải, hãy thực thi
đoạn mã lệnh này lần nữa. Được chuyển ngữ bởi tác giả <MAIL@IF.YOU.WANT> Nhật ký sẽ không được tạo. Tên Lỗi mạng lưới: {0} (thông qua {1}) Phiên bản mới Vẫn chưa giải nén tập tin nào. Phiên bản cũ GÓI CÀI ĐẶT PKGBUILDer (hoặc thư viện xử lý yêu cầu) gặp trục trặc khi xử lý các yêu cầu HTTP. Gói cài đặt {0} không được tìm thấy. (thông qua {1}) Đang thực hiện việc kiểm tra độc lập... Tiếp tục cài đặt? [Y/n] Đang nhận từ ABS... Lỗi nghiêm trọng!  {0} (thông qua {1}) Truy vấn tìm kiếm quá ngắn Đang tìm kiếm dữ liệu khớp... Đang bắt đầu cập nhật toàn bộ hệ thống... Đã tải về thành công: Đang đồng bộ hóa cơ sở dữ liệu gói cài đặt... Mục tiêu ({0}):  Hàm phát triển dữ liệu đã gửi báo cáo phần phát triển cấp cao hơn. Đang cố sử dụng utils.print_package_info với gói cài đặt ABS Đang kiểm tra trạng thái cài đặt... CẢNH BÁO: [đã quá hạn] xóa các tập tin sau khi đã xây dựng xong hiển thị thông tin gỡ rối không kiểm tra tính độc lập (có thể phá bỏ makepkg) không kiểm tra nếu gói cài đặt được cài đặt sau khi xây dựng không sử dụng chế độ hiển thị màu với dữ liệu xuất ra tải các tập tin gói cài đặt đã tìm thấy đã tìm thấy gói cài đặt hiện đang tồn tại cho {0} đã được tìm thấy trong repos đã được tìm thấy trong hệ thống đã được tìm thấy trong AUR makepkg (hoặc đối tượng nào đó) đã thất bại và trả về {0}. makepkg trả về {0}. không không tìm thấy không tìm thấy tiến trình tùy chọn đối số tùy chọn chế độ pacman-like vị trí đối số đang nhận {0} tìm kiếm các chuỗi khớp với AUR hiển thị thông điệp trợ giúp và thoát hiển thị số phiên bản và thoát không có thao tác nào được thực hiện nâng cấp tất cả các gói cài đặt VCS/date-versioned nâng cấp các gói cài đặt AUR đã cài cách dùng cách dùng:  {0} <tiến trình> [...]

PBWrapper, là wrapper dành cho pacman và PKGBUILDer.

{1}

Chỉ áp dụng cho cú pháp thuộc Pacman và PKGBUILDer.  Tra cứu các văn bản/lệnh
trợ giúp để biết thêm chi tiết.

Tùy chọn bổ sung:
  -L, --unlock         mở khóa phần cơ sở dữ liệu của pacman xem thông tin gói cài đặt bình chọn cảnh báo: các cột hiển thị cho thông tin về bảng dữ liệu hiện bị lỗi có {0} (Gói cài đặt: {1}) {0} tập tin đã giải nén {0} kB đã tải về {0}: CHƯA được cài đặt {0}: đã cài đặt {1} {0}: hiện tại ({1}) mới hơn aur ({2}) {0}: không phải gói cài đặt dạng AUR {0}: quá hạn {1} 