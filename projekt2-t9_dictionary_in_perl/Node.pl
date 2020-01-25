#!/usr/bin/perl
#Stanislaw Gruz

package Node;
sub new 
{
    my $class = shift;
    my $self = {
        children    => {},
        words       => []
    };
    
    bless $self, $class;
    return $self;
}

sub child_with_key_exists
{
    my ($self, $key) = @_;
    return exists($self->{children}{$key});
}

sub get_child_by_key
{
    my ($self, $key) = @_;
    return $self->{children}->{$key};
}

sub get_children
{
    my($self) = @_;
    return $self->{children};
}

sub add_child
{
    my ($self, $key, $value) = @_;
    if(exists($self->{children}{$key}))
    {
        return;
    }

    $self->{children}{$key} = $value;
}

sub get_words
{
    my($self) = @_;
    return $self->{words};
}

sub add_word
{
    my ($self, $word) = @_;
    push(@{$self->{words}}, $word)
}

sub contains_word
{
    my ($self, $word) = @_;
    my $words = @{$self->get_words()};
    foreach $current_word (@words)
    {
        if($current_word == $word)
        {
            return 1;
        }
    }
    return 0;
}

sub get_words_recurrent
{
    my($self, $words) = @_;
    my $child = $self->get_children();
    foreach my $child (values %{$self->get_children()})
    {
        my @words_in_child = @{$child->get_words()};
        push(@$words, @words_in_child);
    }
    
    foreach my $child (values %{$self->get_children()})
    {
        $child->get_words_recurrent(\@$words);
    }
}

1;