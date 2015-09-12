To install PKGBUILDer, you can add the pkgbuilder unofficial repo:
https://wiki.archlinux.org/index.php/Unofficial_user_repositories#pkgbuilder

After adding the repository, you need to run::

    # sudo pacman-key -r 5EAAEA16
    # pacman-key --lsign 5EAAEA16
    # pacman -Syyu
