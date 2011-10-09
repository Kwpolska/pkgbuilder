#!/usr/bin/perl
# PKGBUILDer
# Part of KRU
# Copyright Kwpolska 2010. See LICENSE for details.
# USAGE: ./build pkg1 [pkg2] [pkg3] (and more)

use warnings;
use strict;
use LWP::Simple;
use Archive::Any;
use Term::ANSIColor qw(:constants);

$SIG{'INT' } = 'freset';  $SIG{'QUIT'} = 'freset';
$SIG{'HUP' } = 'freset';  $SIG{'TRAP'} = 'freset';
$SIG{'ABRT'} = 'freset';  $SIG{'STOP'} = 'freset';

sub info {
   print BOLD, GREEN, "==> ", RESET, BOLD, shift."\n", RESET;
}

sub freset {
   print RESET, BOLD, "Okay!\nExiting right now.\n", RESET;
   exit(1);
}

sub generate {
   my $pkg=shift;
   info("Building package ".$pkg."...");
   my $tar=$pkg.".tar.gz";
   my $url="http://aur.archlinux.org/packages/".$pkg."/".$tar;

#let's download the file.
   info("Downloading the tarball...");
   getstore($url, "./".$tar);

#untar it...
   info("Extracting the tarball...");
   my $archive = Archive::Any->new("./".$tar);
   $archive->extract;

#build it.
   system('cd '.$pkg.'; time makepkg -si');
   info("The build finished.");
}

my $argc = $#ARGV + 1;
my $i = 0;
if ($argc eq '0') {
   print "ERROR: No package specified.
      HINT:  ./build.pl pkg [pkg2]\n";
}
while ($i != $argc) {
   my $arg = $ARGV[$i]; #There was no other way.
      generate($arg);
   $i = $i + 1;
}
