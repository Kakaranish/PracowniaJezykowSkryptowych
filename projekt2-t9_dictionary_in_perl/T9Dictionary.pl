#!/usr/bin/perl
#Stanislaw Gruz

use lib '.';
require "Node.pl";

package T9Dictionary;
sub new 
{
    my $class = shift;
    my $self = {
        root => new Node()
    };
    
    bless $self, $class;
    return $self;
}

sub get_root
{
    my($self) = @_;
    return $self->{root};
}

sub word_to_digits
{
    my($self, $word) = @_;
    chomp($word);
    my $word_lower_case = lc($word);
    my $digits_string = "";
    foreach(split('', $word_lower_case))
    {
        my $char_val = ord($_);
        if($char_val >= ord('a') && $char_val <= ord('c'))
        {
            $digits_string = $digits_string . '2'
        }
        elsif($char_val >= ord('d') && $char_val <= ord('f'))
        {
            $digits_string = $digits_string . '3'
        }
        elsif($char_val >= ord('g') && $char_val <= ord('i'))
        {
            $digits_string = $digits_string . '4'
        }        
        elsif($char_val >= ord('j') && $char_val <= ord('l'))
        {
            $digits_string = $digits_string . '5'
        }
        elsif($char_val >= ord('m') && $char_val <= ord('o'))
        {
            $digits_string = $digits_string . '6'
        }
        elsif($char_val >= ord('p') && $char_val <= ord('s'))
        {
            $digits_string = $digits_string . '7'
        }
        elsif($char_val >= ord('t') && $char_val <= ord('v'))
        {
            $digits_string = $digits_string . '8'
        }
        elsif($char_val >= ord('w') && $char_val <= ord('z'))
        {
            $digits_string = $digits_string . '9'
        }
    }
    return $digits_string;
}

sub insert_word
{
    my($self, $word) = @_;
    my $word_in_digits = $self->word_to_digits($word);
    my $word_in_digits_length = length($word_in_digits);
    my @split_word_digits = split('', $word_in_digits);

    my $word_exists = 1;
    my $current_node = $self->get_root();
    foreach my $i (0 .. $word_in_digits_length - 1)
    {
        my $current_digit = $split_word_digits[$i];
        if($current_node->child_with_key_exists($current_digit) && $word_exists)
        {
            $current_node = $current_node->get_child_by_key($current_digit);
            #TODO: Validate 2nd condition
            if($i == $word_in_digits_length - 1 
                    && $current_node->contains_word($word) == 0)
            {
                $current_node->add_word($word);
            }
            next;
        }

        $word_exists = 0;
        $current_node->add_child($current_digit, new Node());
        if($i == $word_in_digits_length - 1)
        {
            my $current_node_child = $current_node->get_child_by_key($current_digit);
            $current_node_child->add_word($word);
        }
        $current_node = $current_node->get_child_by_key($current_digit);
    }
}

sub prepare
{
    my($self, $words_source_filename) = @_;
    open my $info, $words_source_filename or do
    {
        print STDERR "\nCould not open $words_source_filename: \t$!\n";
        return;
    };

    while(my $word = <$info>)
    {
        chomp($word);
        $self->insert_word($word);
    }
}

sub get_starting_with
{
    my($self, $word_in_digits) = @_;
    my $word_in_digits_length = length($word_in_digits);
    my @words = ();

    my $start_node = $self->get_root();
    my @split_word_digits = split('', $word_in_digits);
    foreach my $i (0 .. $word_in_digits_length - 2)
    {
        my $current_digit = $split_word_digits[$i];
        unless ($start_node->child_with_key_exists($current_digit))
        {
            return @words; # No prompts 
        }
        $start_node = $start_node->get_child_by_key($current_digit);
    }

    my @words_starting_with = ();
    $start_node->get_words_recurrent(\@words_starting_with);

    return @words_starting_with;
}

1;