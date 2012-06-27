# A very simple todo command line script

This is a very basic command line script that lets you create, edit and delete a simple todo list in the terminal.

A todo list item consists of a description, an urgency level and a completed flag, that indicates whether you are done with the todo item or not.

To setup the todo script you need to create a symbolic link, in one of the directories that is in your $PATH variable. In the examples it is assumed that a symbolic link with the name 'todo' is in one of the folders.


## Adding a todo

To add a new todo list item, you simply write

    $ todo add "Description of todo list item"

This creates a new todo list item with normal urgency level. 

There are three possible urgency levels:
* Chill
* Normal
* Urgent

To create a todo list item with a specific urgency level, use one of the three flags: '-c', '-n', '-u'. E.g. calling

    $ todo add -u "Description of urgent todo item"

creates an 'urgent' todo list item.


## Showing the todo list

To see all your todo list items you simply invoke the script without any arguments

    $ todo

This is a shortcut for the 'list' command, so the above command is equal to

    $ todo list

To show all items, including completed items, use the '-a' flag

    $ todo -a
