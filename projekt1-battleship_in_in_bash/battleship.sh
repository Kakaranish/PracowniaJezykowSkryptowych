#!/bin/bash
#Stanislaw Gruz

# ------------------------------------------------------------------------------
# ---  FUNCTIONS  --------------------------------------------------------------

function show_help()
{
    echo
    echo "Welcome to Battleship game help section."
    echo "The goal of the game is to sink all ships in as few moves as possible."
    echo
    echo "GAMEPLAY"
    echo "Every round you will have to provide the coords of your shot in format (x,y) where:"
    echo "  x - letter in range [a,j]"
    echo "  y - number in range [1,10]"
    echo "If you destroy enemy ship, on your map 'x' mark will appear."
    echo "Unless you will see new 'o' mark on your map."
    echo
    echo "MISC INFO"
    echo "To show help write --help or -h"
    echo "To start game in debug mode use option --DEBUG"
    echo 
}

function check_flags()
{
    for arg in "${@:1}" ; do
        if [ "$arg" == "--help" ] || [ "$arg" == "-h" ] ; then
            show_help
            exit 0
        elif [ "$arg" == "--DEBUG" ] ; then
            is_in_debug_mode=1
        fi
    done   
}

function is_empty()
{
    local arg=$1
    if [ "$arg" == "" ] ; then
        echo 1
    else
        echo 0
    fi
}

function is_destroyed()
{
    local arg=$1
    if [ "$arg" == "x" ] ; then
        echo 1
    else
        echo 0
    fi
}

function is_missed()
{
    local arg=$1
    if [ "$arg" == "0" ] ; then
        echo 1
    else
        echo 0
    fi
}

function get_abs()
{
    local arg=$1
    echo ${arg#-}
}

function get_converted_char_to_number()
{
    local arg=$1
    if [ "$arg" == "a" ] ; then
        echo 1
    elif [ "$arg" == "b" ] ; then
        echo 2
    elif [ "$arg" == "c" ] ; then
        echo 3
    elif [ "$arg" == "d" ] ; then
        echo 4
    elif [ "$arg" == "e" ] ; then
        echo 5
    elif [ "$arg" == "f" ] ; then
        echo 6
    elif [ "$arg" == "g" ] ; then
        echo 7
    elif [ "$arg" == "h" ] ; then
        echo 8
    elif [ "$arg" == "i" ] ; then
        echo 9
    elif [ "$arg" == "j" ] ; then
        echo 10
    fi
}

function opp_get_status()
{
    local x=$1
    local y=$2
    local index=$(( $y * 10 + $x ))
    local status=${opponent_map[$index]}

    echo $status
}

function shots_get_status()
{
    local x=$1
    local y=$2
    local index=$(( $y * 10 + $x ))
    local status=${shots_map[$index]}

    echo $status
}

function opp_set_status()
{
    local x=$1
    local y=$2
    local status=$3
    local index=$(( $y * 10 + $x ))
    opponent_map[$index]=$status
}

function shots_set_status()
{
    local x=$1
    local y=$2
    local status=$3
    local index=$(( $y * 10 + $x ))
    shots_map[$index]=$status
}

function opp_there_is_other_ship_in_neighbourhood()
{
    local tested_x=$1
    local tested_y=$2

    local start_x=$(( $tested_x - 1 ))
    local end_x=$(( $tested_x + 1))
    local start_y=$(( $tested_y - 1 ))
    local end_y=$(( $tested_y + 1))

    for x in $(eval echo "{$start_x..$end_x}") ; do
        for y in $(eval echo "{$start_y..$end_y}") ; do
            local status=`opp_get_status $x $y`
            
            if [ `is_empty $status` == "0" ] ; then
                echo 1
                return
            fi
        done
    done

    echo 0
}

function opp_is_coords_range_legal()
{
    local x1=$1
    local y1=$2
    local x2=$3
    local y2=$4

    if [ "$x1" == "$x2" ] ; then # movement in y-axis
        x=$x1
        if [ $y1 -lt $y2 ] ; then
            start_y=$y1
            end_y=$y2
        else
            start_y=$y2
            end_y=$y1
        fi

        if [ $start_y -lt 1 ] ; then
            echo 0
            return
        fi

        if [ $end_y -gt 10 ] ; then
            echo 0
            return
        fi

        for i in $(eval echo "{$start_y..$end_y}")
        do
            if [ `opp_there_is_other_ship_in_neighbourhood $x $i` == "1" ] ; then
                echo 0
                return
            fi
        done

    elif [ "$y1" == "$y2" ] ; then # movement in x-axis
        y=$y1
        if [ $x1 -lt $x2 ] ; then
            start_x=$x1
            end_x=$x2
        else
            start_x=$x2
            end_x=$x1
        fi

        if [ $start_x -lt 1 ] ; then
            echo 0
            return
        fi

        if [ $end_x -gt 10 ] ; then
            echo 0
            return
        fi

        for i in $(eval echo "{$start_x..$end_x}")
        do
            if [ `opp_there_is_other_ship_in_neighbourhood $i $y` == "1" ] ; then
                echo 0
                return
            fi
        done
    else
        echo 0
        return
    fi
    echo 1
}

function random_ships()
{
    for ships_num in "${ships_to_rand[@]}" ; do

        local x1=0
        local y1=0
        local x2=0
        local y2=0
        local coords_drawn=0

        while [ "$coords_drawn" == "0" ] ; do
            x1=$(( ( RANDOM % 10 )  + 1 ))
            y1=$(( ( RANDOM % 10 )  + 1 ))

            local dir_permutation=`shuf -i 1-4 -n 4`
            IFS=',' read -r -a split_dir_permutation <<< "$dir_permutation"
            
            local cut_ships_num=$(( $ships_num - 1 ))
            for dir in "${split_dir_permutation[@]}" ; do
                
                if [ "$dir" == "1" ] ; then #UP
                    x2=$x1
                    y2=$(( $y1 - $cut_ships_num ))
                elif [ "$dir" == "2" ] ; then #RIGHT
                    x2=$(( $x1 + $cut_ships_num ))
                    y2=$y1
                elif [ "$dir" == "2" ] ; then #DOWN
                    x2=$x1
                    y2=$(( $y1 + $cut_ships_num ))
                elif [ "$dir" == "2" ] ; then #LEFT
                    x2=$(( $x1 - $cut_ships_num ))
                    y2=$y1
                fi
                
                local coords_range_is_legal=`opp_is_coords_range_legal $x1 $y1 $x2 $y2`
                if [ "$coords_range_is_legal" == "1" ] ; then
                    coords_drawn=1
                    break
                fi
            done
        done

        # Filling range
        if [ $x1 -lt $x2 ] ; then
            start_x=$x1
            end_x=$x2
        else
            start_x=$x2
            end_x=$x1
        fi

        if [ $y1 -lt $y2 ] ; then
            start_y=$y1
            end_y=$y2
        else
            start_y=$y2
            end_y=$y1
        fi
        
        for i in $(eval echo "{$start_x..$end_x}") ; do
            for j in $(eval echo "{$start_y..$end_y}") ; do
                opp_set_status $i $j "o"
            done
        done

    done
}

function coords_have_correct_format()
{
    local coords=$1
    local coords_regex="^([a-j],([1-9]{1}|10))$"
    
    if ! [[ $coords =~ $coords_regex ]] ; then
        echo 0
    else
        echo 1
    fi
}

function draw_maps()
{
    if [ "$is_in_debug_mode" == "1" ] ; then
        printf '%s\t\t\t\t\t%s\n' 'Your shots' 'Computer ships'
    else
        echo "Your shots"
    fi
    # FIRST MAP
    printf "  "
    for i in {a..j} ; do
        if [ $i == "a" ] ; then
            printf "   $i "
        else
            printf "  $i "
        fi
    done

    # SECOND MAP
    if [ "$is_in_debug_mode" == "1" ] ; then
        printf "\t"
        printf "  "
        for i in {a..j} ; do
            if [ $i == "a" ] ; then
                printf "   $i "
            else
                printf "  $i "
            fi
        done
    fi

    echo

    # --------------------------------------------------------------------------

    for i in {1..10} ; do
        
        # FIRST MAP
        printf "  "
        for j in {1..10} ; do
            if [ $j -eq 1 ] ; then
                printf '%s' '  --- '
            else
                printf '%s' '--- '
            fi
        done
        
        # SECOND MAP
        if [ "$is_in_debug_mode" == "1" ] ; then
            printf "\t"
            printf "  "

            for j in {1..10} ; do
                if [ $j -eq 1 ] ; then
                    printf '%s' '  --- '
                else
                    printf '%s' '--- '
                fi
            done
        fi
        
        echo
        
        # ----------------------------------------------------------------------
        
        # FIRST MAP
        if [ $i -eq 10 ] ; then
            printf "$i "
        else
            printf "$i  "
        fi
        

        for j in {1..10} ; do
            status=`shots_get_status $j $i`
            if [ "$status" == "" ] ; then
                printf "|   "
            else
                printf "| $status "
            fi
            
            if [ $j -eq 10 ] ; then
                printf "|"
            fi
        done
        
        # SECOND MAP
        if [ "$is_in_debug_mode" == "1" ] ; then
            printf "\t"
            if [ $i -eq 10 ] ; then
                printf "$i "
            else
                printf "$i  "
            fi
            
            for j in {1..10} ; do
                status=`opp_get_status $j $i`
                if [ "$status" == "" ] ; then
                    printf "|   "
                else
                    printf "| $status "
                fi
                
                if [ $j -eq 10 ] ; then
                    printf "|"
                fi
            done
        fi
        
        echo
        
        # ----------------------------------------------------------------------
        
        if [ $i -eq 10 ] ; then
            
            # FIRST MAP
            for j in {1..10} ; do
                if [ $j -eq 1 ] ; then
                    printf "  "
                    printf '%s' '  --- '
                else
                    printf '%s' '--- '
                fi
            done

            # SECOND MAP
            if [ "$is_in_debug_mode" == "1" ] ; then
                printf "\t"
                
                for j in {1..10} ; do
                    if [ $j -eq 1 ] ; then
                        printf "  "
                        printf '%s' '  --- '
                    else
                        printf '%s' '--- '
                    fi
                done
            fi
            
            echo
        fi
        # ----------------------------------------------------------------------
    done
}

# ------------------------------------------------------------------------------
# -- PROGRAM -------------------------------------------------------------------

is_in_debug_mode=0 # If set to 1, map with opponent ships will be shown 
check_flags $@

# This array contains sizes of ships that will be placed on the map
# In this case on the map will be one ship with size=3 and one with size=2
ships_to_rand=(3 2)
total_points_to_hit=0
for ships_num in "${ships_to_rand[@]}" ; do
    total_points_to_hit=$(( $total_points_to_hit + $ships_num ))
done

# INIT SHIPS
for i in {10..110} ; do
    opponent_map[$i]=" "
done

random_ships

for i in {10..110} ; do
    shots_map[$i]=""
done

hits=0
hit_points=0
clear

while [ $(( $total_points_to_hit - $hit_points )) -gt 0 ] ; do
    
    draw_maps
    echo "Remaining points to hit:" $(( $total_points_to_hit - $hit_points ))

    if ! [ "$info" == "" ] ; then
        echo $info
        echo
    fi

    read -p "Enter coords in format 'x,y': " coords
    while [ `coords_have_correct_format $coords` == "0" ] ; do
        read -p "Invalid input! Enter coords one again 'x,y' : " coords
    done

    IFS=',' read -r -a split_coords <<< "$coords"
    x=$(( `get_converted_char_to_number ${split_coords[0]}` ))
    y=${split_coords[1]}

    hits=$(( $hits + 1 ))
    opp_status=`opp_get_status $x $y`
    shots_status=`shots_get_status $x $y`
    
    if [ `is_destroyed $shots_status` == "1" ] || [ `is_missed $shots_status` == "1" ] ; then
        info="You've already shot at these coords!"
    elif [ `is_empty $opp_status` == "0" ] ; then
        shots_set_status $x $y "x"

        hit_points=$(( $hit_points + 1 ))
        info="Ship was hit!"
    else
        shots_set_status $x $y "o"
        
        info="Mishit!"
    fi

    clear
done

clear
draw_maps

echo "Good job! You won in" $hits "hits :)." 