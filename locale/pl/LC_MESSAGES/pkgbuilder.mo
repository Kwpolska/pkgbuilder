��    w      �  �   �      
  �  
         	          (     C     K  "   ^  "   �     �     �     �     �  (     '   /     W  *   g     �     �     �     �          !     (     H     c  5   q  '   �     �     �  �        �          :  &   W     ~     �  �   �  �   �  (   5     ^  #   x     �     �     �     �     �     �  R   �      E      f  ,   �  !   �  �  �     �  R   �     "     ?     V     s     �  "   �     �  +   �  :   	     D  !   I     k     t     �  3   �     �  &   �  ,     2   A     t  "   �  "   �     �     �  !   �                0  2   A     t     �  
   �  	   �  
   �     �     �     �     �     �  #   �     !     A     ^  +   u     �     �  �   �     �     �  9   �  9     1   S     �     �     �     �     �  0   �       (        B     Z  �  l    i   	  y"     �#     �#     �#     �#     �#      �#      $     '$  !   7$  +   Y$  "   �$  )   �$  .   �$     %  +   %  6   >%     u%  "   �%     �%     �%     �%  %   �%      &     9&  >   J&  *   �&  #   �&     �&  �   �&  !   �'  &   (  %   ((  /   N(  #   ~(     �(  �   �(  �   �)  E   �*     �*  )   �*     +     +     3+     ?+     S+     e+  S   l+  %   �+     �+  A   ,      D,  �  e,     c.  _   w.  $   �.  '   �.  #   $/  -   H/     v/  *   �/     �/  @   �/  8   0     <0     H0     h0     o0      }0  7   �0      �0  %   �0  1   1  =   O1     �1  $   �1  .   �1     2  
   2  !   $2     F2     a2     w2  V   �2     �2     �2     �2      3     3     3     -3     33  	   K3     U3  ,   d3     �3     �3     �3  ?   �3  &   &4     M4  -  ]4  !   �5     �5  J   �5  ?   6  9   A6     {6     6     �6     �6     �6  1   �6      7  +   7     C7     Y7     <   :          /   ^   [       H   4   ?          _   e   X                  a   -   "          L       R      E   p          d   	           h           >   m       U   u   5          Z   q              c       3                 i          V       r   \      g   0   G       1       Q   W   ;   M      O   f         2   %   l   D   P   
       S   +   j   `   C   b         F   w       &   T             n      9               o           ,       7   )   s               N   =       v   A       k      #       .   $          6      I   K      8               B   ]      J         t       *       Y   '      !   @   (    

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
  [installed: {0}]  [installed] %(prog)s <operation> [...] (dummy) 0 bytes downloaded :: Retrieving packages from abs... :: Retrieving packages from aur... AUR Error: {0} AUR/ABS packages to build Aborted by user! Exiting... Also accepting ABS packages. An AUR helper (and library) in Python 3. Building more AUR packages is required. Building {0}... Cannot create the configuration directory. Cannot run as root.  Aborting. Checking dependencies... Connection error: {0} (via {1}) Didn’t pass any packages. Downloading the tarball... ERROR: Error while processing {0}: {1} Extracting AUR packages... Extracting... Failed to fulfill package dependency requirement: {0} Failed to retieve {0} (from ABS/rsync). Fetching package information... HTTP Error {0} (via {1}) Hello!

PKGBUILDer is now available as an AUR package.  It is the suggested
way of installing PKGBUILDer.  This script will download the AUR
package and install it.  If you will have problems, please download
and compile the package manually.

 Hit Enter/Return to continue.  Initializing pacman access... Installing built packages... Installing missing AUR dependencies... Installing with pacman -U... Interrupt signal received
 It looks like you want to quit.  Okay then, goodbye.
All the files this script was working on are placed in
    {0}
(the number is random).

If that's what you want to do, go for it.  If it isn't, run this
script again. It looks like you want to quit.  Okay then, goodbye.
No work has been started yet.

If that's what you want to do, go for it.  If it isn't, run this
script again. LANG locale by AUTHOR <MAIL@IF.YOU.WANT> Logs will not be created. Moving to /var/cache/pacman/pkg/... Name Network error: {0} (via {1}) New Version No files extracted. Old Version PACKAGE PKGBUILDer (or the requests library) had problems with fulfilling an HTTP request. Package {0} not found. (via {1}) Performing a dependency check... Please restart PKGBUILDer as a regular user. Proceed with installation? [Y/n]  Repository     : aur
Category       : {cat}
Name           : {nme}
Package Base   : {bse}
Version        : {ver}
URL            : {url}
Licenses       : {lic}
Groups         : {grp}
Provides       : {prv}
Depends On     : {dep}
Make Deps      : {mkd}
Check Deps     : {ckd}
Optional Deps  : {opt}
Conflicts With : {cnf}
Replaces       : {rpl}
Votes          : {cmv}
Out of Date    : {ood}
Maintainer     : {mnt}
First Submitted: {fsb}
Last Updated   : {upd}
Description    : {dsc}
 Retrieving from ABS... Running as root is not allowed as it can cause catastrophic damage to your system! Sanity error!  {0} (via {1}) Search query too short Searching for exact match... Starting full system upgrade... Successfully fetched:  Synchronizing package databases... Targets ({0}):  The build function reported a proper build. Trying to use utils.print_package_info with an ABS package USER Validating installation status... WARNING: [out of date] clean up work files after build copy package files to pacman cache and install them display debug messages don't  install packages after building don't check dependencies (may break makepkg) don't check if packages were installed after build don't use colors in output error: package '{0}' was not found fetch all package files of an user fetch package files found found an existing package for {0} found in repos found in system found in the AUR makepkg (or someone else) failed and returned {0}. makepkg returned {0}. no none found not found operations optional arguments options pacman-like mode positional arguments retrieving {0} search the AUR for matching strings show this help message and exit show version number and quit there is nothing to do upgrade all the VCS/date-versioned packages upgrade installed AUR packages usage usage:  {0} <operation> [...]

PBWrapper, a wrapper for pacman and PKGBUILDer.

{1}

Pacman and PKGBUILDer syntaxes apply.  Consult their manpages/help
commands for more details.

Additional options:
  -L, --unlock         unlock the pacman database view package information votes warning: insufficient columns available for table display warning: {0}: downgrading from version {1} to version {2} warning: {0}: local ({1}) is newer than aur ({2}) yes {0} (Package: {1}) {0} files extracted {0} kB downloaded {0}: NOT installed {0}: downgrading from version {1} to version {2} {0}: installed {1} {0}: local ({1}) is newer than aur ({2}) {0}: not an AUR package {0}: outdated {1} Project-Id-Version: 3.4.0
Report-Msgid-Bugs-To: Chris Warrick <chris@chriswarrick.com>
POT-Creation-Date: 2015-01-01 11:49+0100
PO-Revision-Date: 2014-12-27 10:56+0000
Last-Translator: Chris Warrick <kwpolska@gmail.com>
Language-Team: Polish (http://www.transifex.com/projects/p/pkgbuilder/language/pl/)
Language: pl
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
 

Przeczytaj powyższe wyjście.  Jeśli skrypt miał problemy, spróbuj
jeszcze raz.  Możesz też spróbować samodzielnie debugować pracę skryptu.
Wszystkie pliki, nad którymi ten skrypt pracował, znajdują się w
    {0}
(liczba jest losowa).

Jeśli wszystko się udało, gratulacje!  Teraz możesz używać PKGBUILDer-a.
Dla użycia samodzielnego, wpisz `pkgbuilder` do terminala (zsh: hash -r,
inne powłoki mogą wymagać innej komendy).  Dla użycia jako moduł
Pythona, wpisz `import pkgbuilder` do interpretera.
 

Coś poszło źle.  Przeczytaj wyjście makepkg i spróbuj ponownie.
Możesz też próbować debugować pracę tego skryptu samemu.
Wszystkie pliki, nad którymi ten skrypt pracował, znajdują się w
    {0}
(liczba jest losowa).

Jeśli się mylę, gratulacje!
  [zainstalowano: {0}]  [zainstalowano] %(prog)s <operacja> [...] (nic nie robi) pobrano 0 bajtów :: Pobieranie pakietów z abs... :: Pobieranie pakietów z aur... Błąd AUR: {0} pakiety do zbudowania z AUR i ABS Przerwane przez użytkownika! Kończenie... Również akceptuje pakiety z ABS. Pomocnik AUR (i biblioteka) w Pythonie 3. Należy zainstalować więcej pakietów z AUR. Budowanie {0}... Nie można utworzyć katalogu konfiguracji. Nie można uruchomić jako root.  Przerywanie pracy… Sprawdzanie zależności... Błąd połączenia: {0} (via {1}) Nie podano żadnych pakietów. Pobieranie tarballa... BŁĄD: Błąd podczas przetwarzania {0}: {1} Wypakowywanie pakietów z AUR... Wypakowywanie... Nie udało się wypełnić wymagań zależności pakietu: {0} Nie udało się pobrać {0} (z ABS/rsync). Pobieranie informacji o pakiecie... Błąd HTTP {0} (via {1}) Cześć!

PKGBUILDer jest teraz dostępny jako pakiet w AUR.  Jest to polecany
sposób instalacji PKGBUILDer-a.  Ten skrypt pobierze pakiet z AUR i go
zainstaluje.  Jeśli będziesz miał problemy, pobierz i skompiluj pakiet
ręcznie.

 Wciśnij Enter, aby kontynuować. Inicjalizowanie dostępu do pacmana... Instalowanie zbudowanych pakietów... Instalowanie brakujących zależności z AUR... Instalowanie za pomocą pacman -U.. Interrupt signal received
 Wygląda na to, że chcesz wyjść.  Okej, do widzenia.
Wszystkie pliki, nad którymi ten skrypt pracował, znajdują się w
    {0}
(liczba jest losowa).

Jeśli to jest to, co chcesz zrobić, proszę bardzo.  Jeśli nie,
uruchom ten skrypt jeszcze raz. Wygląda na to, że chcesz wyjść.  Okej, do widzenia.
Żadne prace nie zostały jeszcze rozpoczęte.

Jeśli to jest to, co chcesz zrobić, proszę bardzo.  Jeśli nie,
uruchom ten skrypt jeszcze raz. Polskie tłumaczenie autorstwa Chris Warrick <chris@chriswarrick.com> Logi nie będą tworzone. Przenoszenie do /var/cache/pacman/pkg/... Nazwa Błąd sieci: {0} (via {1}) Nowa wersja Nic nie wypakowano. Poprzednia wersja PAKIET PKGBUILDer (lub bliblioteka requests) miała problemy z wypełniem żądania HTTP. Nie znaleziono pakietu {0}. (via {1}) Sprawdzanie zależności... Proszę uruchomić PKGBUILDera ponownie jako zwykły użytkownik. Kontynuować instalację? [Y/n]  Repozytorium   : aur
Kategoria      : {cat}
Nazwa          : {nme}
Baza pakietu   : {bse}
Wersja         : {ver}
URL            : {url}
Licencje       : {lic}
Grupy          : {grp}
Dostarcza      : {prv}
Zależy od      : {dep}
Zależności budowania: {mkd}
Zależności sprawdzania: {ckd}
Opcjonalne zależności: {opt}
Konfliktuje z  : {cnf}
Zastępuje      : {rpl}
Głosy          : {cmv}
Nieaktualny    : {ood}
Opiekun        : {mnt}
Wysłany        : {fsb}
Ost. aktualiz. : {upd}
Opis           : {dsc}
 Pobieranie z ABS... Uruchamianie jako root nie jest dozwolone, ponieważ może to spowodować katastrofalne szkody! Sanity test nieudany!  {0} (via {1}) zapytanie do wyszukiwarki zbyt krótkie Szukanie dokładnego dopasowania... Rozpoczynanie pełnej aktualizacji systemu... Pomyślnie pobrano:  Synchronizowanie baz danych z pakietami... Cele ({0}): Funkcja budowania paczek powiadomiła o prawidłowym zbudowaniu. Próba użycia utils.print_package_info z pakietem z ABS UŻYTKOWNIK Walidowanie stanu instalacji... UWAGA: [nieaktualny] usuń pliki robocze po wszystkim kopiuje pliki pakietów do cache pacmana i je instaluje pokazuje wiadomości debugowania nie instaluje pakietów po zbudowaniu nie sprawdza zależności (może popsuć makepkg) nie sprawdza czy pakiety zostały zainstalowane po zbudowaniu nie używa kolorów na wyjściu błąd: nie znaleziono pakietu '{0}' pobierz wszystkie pliki pakietów użytkownika pobierz pliki pakietów znaleziono znaleziono istniejący pakiet {0} znaleziono w repozytoriach znaleziono w systemie znaleziono w AUR tworzenie pakietu przez makepkg (lub coś innego) nie powiodło się i zwróciło {0}. makepkg zwrócił {0}. nie brak nie znaleziono operacje argumenty opcjonalne opcje tryb podobny do pacmana argumenty pobieranie {0} przeszukuje AUR według pasujących ciągów pokaż tą wiadomość i wyjdź pokaż numer wersji i wyjdź nie ma nic do zrobienia uaktualnia wszystkie pakiety z VCS/z wersjami będącymi datami uaktualnia zainstalowane pakiety z AUR sposób użycia sposób użycia:  {0} <operacja> [...]

PBWrapper, wrapper dla pacmana i PKGBUILDera.

{1}

Obowiązuje składnia pacmana i PKGBUILDera.  Zajrzyj do ich stron
w podręczniku man lub do komend pomocy, aby dowiedzieć się więcej.

Dodatkowe opcje:
  -L, --unlock         odblokuj bazę danych pacmana wyświetla informację o pakiecie głosów ostrzeżenie: Niewystarczająca szerokość okna, aby wyświetlić tabelę ostrzeżenie: {0}: dezaktualizowanie z wersji {1} do wersji {2} ostrzeżenie: {0}: local ({1}) jest nowsze niż aur ({2}) tak {0} (Pakiet: {1}) wypakowano {0} plików pobrano {0} kB {0}: NIE zainstalowano {0}: dezaktualizowanie z wersji {1} do wersji {2} {0}: zainstalowany {1} {0}: local ({1}) jest nowsze niż aur ({2}) {0}: pakiet spoza AUR {0} nieaktualny {1} 