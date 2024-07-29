#!/usr/bin/perl

use strict;
use warnings;
use autodie;

use v5.34;
use Cwd qw/getcwd abs_path/;

my $top = getcwd;
my $chords_file = shift @ARGV or die "No chord names file provided\n";

open(my $ly, ">", "chords.ly");
print $ly <<'EOF';
\version "2.24.3"

$(load (string-append (getenv "HOME") "/ly/scm/jazzchords.scm"))

\header {
  tagline = #f
}

EOF

open(my $chords, "<", $chords_file);
while (<$chords>) {
  chomp;
  print $ly <<"BOOK";
\\book {
\\bookOutputName \"$.\"
  \\markup {
    \\fill-line { \\jazzchord \"$_\" }
  }
}
BOOK
}
close $chords;
close $ly;

mkdir "pdf" unless -d "pdf";
system(qw/lilypond -o pdf chords.ly/);

chdir $top . "/pdf";
opendir my $dir, ".";
my @pdffiles = map { abs_path $_ } grep { -f } readdir $dir;
closedir $dir;

for my $pdf (@pdffiles) {
  system("pdfcrop", $pdf, $pdf);
}
