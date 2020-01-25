#!/usr/bin/perl
#Stanislaw Gruz

use strict; 
use warnings;
use lib '.';
require "Node.pl";
require "T9Dictionary.pl";

sub show_help
{
    print "\n";
    print "DESCRIPTION\n";
    print "     Program simulates t9 dictionary which in before was used in mobile phones.\n";
    print "     User provides sequence of digits and all possible prompts for the digit sequence are written to output.txt file.\n";
    print "SYNOPSIS\n";
    print "     ./t9_script.pl [OPTION] number_sequence\n";
    print "AVAILABLE OPTIONS\n";
    print "     -h or --help - show help\n";
    print "REMARKS:\n";
    print "     'number_sequence' may only contain from 2-9 digits\n";
    print "\n";
}

foreach my $arg (@ARGV)
{
    if($arg eq "--help" || $arg eq "-h")
    {
        &show_help();
        exit;
    }
}

if($#ARGV + 1 != 1)
{
    print("ERROR: Wrong number of arguments.\n");
    &show_help();
    exit();
}

my $digits = shift;
if ($digits !~ /^([2-9]+)$/)
{
    print("ERROR: Invalid sequence of digits.\n");
    &show_help();
    exit();
}

my $dictionary = new T9Dictionary();
$dictionary->prepare("words.txt");

my @words = $dictionary->get_starting_with($digits);
open(my $file_handler, '>', "output.txt");
foreach(@words)
{
    print $file_handler "$_\n";
}
close $file_handler;