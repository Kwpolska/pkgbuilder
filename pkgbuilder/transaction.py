# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.18
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""
Package installation transactions.

.. versionadded:: 4.1.0

:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import os
import os.path
import time
import json
import enum
import pkgbuilder.utils
import pyalpm
from . import DS, _, __version__

__all__ = ('generate_filename', 'Transaction', 'TransactionStatus')


def generate_filename(absolute=True):
    """Generate a filename for the transaction."""
    fn = "pkgbuilder-{0}.tx".format(int(time.time()))
    if absolute:
        return os.path.abspath(fn)
    else:
        return fn


class TransactionStatus(enum.Enum):
    """Transaction status."""

    # validate, move, install, success
    undefined = 0
    moved = 0b11
    move_failed = 0b10
    installed = 0b111
    install_failed = 0b110
    validated = 0b1111
    validation_failed = 0b1110


class Transaction(object):
    """A package transaction."""

    def __init__(self, pkgnames, pkgpaths, sigpaths, asdeps=True, uopt='',
                 filename=None, delete=False, status=None, pacmanreturn=-1,
                 invalid=-1):
        """Initialize a transaction.

        :param list pkgnames: package names to install
        :param list pkgpaths: absolute paths to packages to install
        :param list sigpaths: absolute paths to signatures for packages
        :param bool asdeps: Install with ``--asdeps`` option
        :param str uopt: additional options to ``pacman -U``
        :param str filename: transaction file
        :param bool delete: delete transaction file if run successful
        :param TransactionStatus status: transaction status
        :param int pacmanreturn: Return code from ``pacman -U``
        :param int invalid: number of invalid packages
        """
        # all lists are deduplicated
        self.pkgnames = list(set(pkgnames))
        self.pkgpaths = list(set(pkgpaths))
        self.sigpaths = list(set(sigpaths))
        self.asdeps = asdeps
        self.uopt = uopt
        self.filename = filename
        self.delete = delete
        if status is not None:
            self.status = status
        else:
            self.status = TransactionStatus.undefined
        self.pacmanreturn = pacmanreturn
        self.invalid = invalid

        if self.filename:
            self.save()

    def __repr__(self):
        """Return the representation of a transaction."""
        s = "<Transaction {0} ({1})>"
        if self.filename:
            return s.format(self.filename, self.status)
        else:
            return s.format(hex(id(self)), self.status)

    @classmethod
    def load(cls, filename):
        """Load a transaction file."""
        with open(filename, 'r') as fh:
            jsondata = fh.read()
        tx = cls.fromjson(jsondata)
        tx.filename = filename
        DS.log.info("Transaction loaded: {0}".format(tx.filename))
        return tx

    def save(self, filename=None):
        """Save a transaction file."""
        if filename is not None:
            self.filename = filename
        if self.filename:
            with open(self.filename, 'w+') as fh:
                fh.write(self.tojson())
            DS.log.info("Transaction saved: {0}".format(self.filename))

    @classmethod
    def fromjson(cls, jsondata):
        """Create a transaction from JSON data.

        The following fields exist:

        * ``__PBTX__`` — PKGBUILDer version
        * ``pkgnames`` — names of packages to install
        * ``pkgpaths`` — paths to packages to install
        * ``sigpaths`` — paths to attached signature files
        * ``asdeps`` — whether or not this is a dependency install
        * ``uopt`` — special (local) options to ``pacman -U``
        * ``status`` — status code of the transaction
        * ``pacmanreturn`` — pacman return code
        * ``invalid`` — number of invalid packages
        """
        txdata = json.loads(jsondata)
        return cls(
            pkgnames=txdata['pkgnames'],
            pkgpaths=txdata['pkgpaths'],
            sigpaths=txdata['sigpaths'],
            asdeps=txdata['asdeps'],
            uopt=txdata['uopt'],
            status=TransactionStatus(txdata['status']),
            pacmanreturn=txdata['pacmanreturn'],
            invalid=txdata['invalid']
        )

    def tojson(self):
        """Serialize a transaction to JSON."""
        return json.dumps({
            '__PBTX__': __version__,
            'pkgnames': self.pkgnames,
            'pkgpaths': self.pkgpaths,
            'sigpaths': self.sigpaths,
            'asdeps': self.asdeps,
            'uopt': self.uopt,
            'status': self.status.value,
            'pacmanreturn': self.pacmanreturn,
            'invalid': self.invalid,
        }, sort_keys=True, indent=4)

    @property
    def exitcode(self):
        """Provide the most appropriate exit code."""
        if self.invalid > -1:
            return self.invalid
        elif self.pacmanreturn > -1:
            return self.pacmanreturn
        else:
            return 1

    def run(self, standalone=True, quiet=False, validate=True):
        """Run a transaction."""
        if not quiet:
            if not standalone:
                DS.fancy_msg(_('Installing built packages...'))
            if self.filename:
                DS.fancy_msg(_('Running transaction from file {0}...').format(
                    self.filename))
            else:
                DS.fancy_msg(_('Running transaction...'))

        DS.log.info("Running transaction {0!r}".format(self))

        self._test_sudo()

        ret = self.move(True, quiet)
        if ret != 0:
            self._print_txfail('move', quiet)
            return False
        ret = self.install(True, quiet)
        if ret != 0:
            self._print_txfail('install', quiet)
            return False
        if validate:
            ret = self.validate(quiet)
            if ret != 0:
                self._print_txfail('validate', quiet)
                return False
        DS.log.info("Transaction {0!r} succeeded".format(self))
        if not quiet:
            DS.fancy_msg(_("Transaction succeeded."))
        if self.delete and self.filename:
            os.remove(self.filename)
            if not quiet:
                DS.fancy_msg2(_("Deleted transaction file {0}").format(
                    self.filename))
            self.filename = None
        return True

    def _print_txfail(self, stage, quiet):
        """Print transaction failure message."""
        if not quiet:
            DS.log.error("Transaction {0!r} failed (stage {1})".format(
                self, stage))
            if self.pacmanreturn == 0 and self.invalid > 0:
                # special case: retrying the transaction is not helpful, as it
                # won't help fix the validation status.  The user should
                # investigate by reading the build logs and acting accordingly.
                DS.fancy_error(_("Some packages failed to build."))
            else:
                DS.fancy_error(_("Transaction failed!"))
                if self.filename:
                    c = 'c' if self.delete else ''
                    DS.fancy_error2(_("To retry, run:"))
                    DS.fancy_error2("pkgbuilder -X{c} {fn}".format(
                        c=c, fn=self.filename))

    def _test_sudo(self):
        """Test if sudo works."""
        trueexit = 256
        while trueexit != 0:
            trueexit = DS.sudo(['true'])

    def _set_status_from_return(self, returncode, success, failure):
        """Set status from return code."""
        if returncode == 0:
            self.status = success
        else:
            self.status = failure
        self.save()

    def _pacman_pkgpath(self, pkgpath):
        """Return package path in pacman cache."""
        return os.path.join('/var/cache/pacman/pkg/',
                            os.path.basename(pkgpath))

    @property
    def pacman_pkgpaths(self):
        """Return package paths, augmented for pacman."""
        return [self._pacman_pkgpath(i) for i in self.pkgpaths]

    def move(self, sudo_tested=False, quiet=False):
        """Move package and signature files to pacman cache.

        :param bool sudo_tested: if sudo was tested (password prompt)
        :param bool quiet: suppress messages
        :return: 0 on success, +mv return, -failed files
        :rtype: int
        """
        if not sudo_tested:
            self._test_sudo()
        if not quiet:
            DS.fancy_msg2(_('Moving to /var/cache/pacman/pkg/...'))

        pkgpaths = []
        sigpaths = []
        failed_files = 0
        for p in self.pkgpaths:
            pacp = self._pacman_pkgpath(p)
            if p == pacp:
                DS.log.warning("Not moving package file {0} -- "
                               "already in pacman cache".format(p))
            elif os.path.exists(p):
                pkgpaths.append(p)
            elif os.path.exists(pacp):
                DS.log.warning("Not moving package file {0} -- "
                               "found in pacman cache".format(p))
            else:
                DS.log.error("Not moving package file {0} -- "
                             "not found".format(p))
                if not quiet:
                    DS.fancy_warning2(_("Package file {0} not found").format(
                        p))
                failed_files += 1

        for s in self.sigpaths:
            pacs = self._pacman_pkgpath(p)
            if s == pacs:
                DS.log.warning("Not moving signature file {0} -- "
                               "already in pacman cache".format(s))
            elif os.path.exists(s):
                sigpaths.append(s)
            elif os.path.exists(pacs):
                DS.log.warning("Not moving signature file {0} -- "
                               "found in pacman cache".format(s))
            else:
                DS.log.error("Not moving signature file {0} -- "
                             "not found".format(s))
                if not quiet:
                    DS.fancy_warning2(_("Signature file {0} not found").format(
                        s))
                failed_files += 1

        DS.log.debug('mv {0} {1} /var/cache/pacman/pkg/'.format(
            pkgpaths, sigpaths))
        ret = -failed_files
        if pkgpaths or sigpaths:
            ret = DS.sudo(['mv'] + pkgpaths + sigpaths +
                          ['/var/cache/pacman/pkg/'])
        self._set_status_from_return(ret, TransactionStatus.moved,
                                     TransactionStatus.move_failed)
        return ret

    def install(self, sudo_tested=False, quiet=False):
        """Install packages through ``pacman -U``.

        :param bool sudo_tested: if sudo was tested (password prompt)
        :param bool quiet: suppress messages
        :return: pacman return code
        :rtype: int
        """
        if not sudo_tested:
            self._test_sudo()
        if not quiet:
            DS.fancy_msg2(_('Installing with pacman -U...'))

        npkgpaths = self.pacman_pkgpaths
        uopt = self.uopt.strip()

        if self.asdeps:
            uopt = uopt + ' --asdeps'

        if not DS.confirm:
            uopt = uopt + ' --noconfirm'

        uopt = uopt.strip()

        if uopt:
            DS.log.debug('$PACMAN -U {0} {1}'.format(uopt, npkgpaths))
            ret = DS.sudo([DS.paccommand, '-U'] + uopt.split(' ') + npkgpaths)
        else:
            DS.log.debug('$PACMAN -U {0}'.format(npkgpaths))
            ret = DS.sudo([DS.paccommand, '-U'] + npkgpaths)

        self.pacmanreturn = ret
        self._set_status_from_return(ret, TransactionStatus.installed,
                                     TransactionStatus.install_failed)
        return ret

    def validate(self, quiet):
        """Check if packages were installed.

        :param bool quiet: suppress messages
        :return: number of packages that were not installed
        :rtype: int
        """
        if self.pkgnames:
            if not quiet:
                DS.fancy_msg(_('Validating installation status...'))
            DS.log.info('Validating: ' + '; '.join(self.pkgnames))
            DS.pycreload()
            localdb = DS.pyc.get_localdb()

            aurpkgs = {aurpkg.name: aurpkg.version for aurpkg in
                       pkgbuilder.utils.info(self.pkgnames)}

            wrong = len(self.pkgnames)
        else:
            wrong = 0

        for pkgname in self.pkgnames:
            lpkg = localdb.get_pkg(pkgname)
            try:
                aurversion = aurpkgs[pkgname]
            except KeyError:
                if not lpkg:
                    if not quiet:
                        DS.fancy_error2(_('{0}: not an AUR package').format(
                                        pkgname))
                else:
                    wrong -= 1
                    if not quiet:
                        DS.fancy_msg2(_('{0}: installed {1}').format(
                                      pkgname, lpkg.version))
            else:
                if not lpkg:
                    if not quiet:
                        DS.fancy_error2(_('{0}: NOT installed').format(
                            pkgname))
                else:
                    if pyalpm.vercmp(aurversion, lpkg.version) > 0:
                        if not quiet:
                            DS.fancy_error2(_('{0}: outdated {1}').format(
                                pkgname, lpkg.version))
                    else:
                        wrong -= 1
                        if not quiet:
                            DS.fancy_msg2(_('{0}: installed {1}').format(
                                pkgname, lpkg.version))

        self.invalid = wrong
        self._set_status_from_return(wrong, TransactionStatus.validated,
                                     TransactionStatus.validation_failed)
        return wrong
