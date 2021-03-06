.. _keymap:

Customizing the Keymap
======================

The variable :var:`config.keymap` contains a map from event names to lists
of keysyms that cause those events to occur.

.. note::

    Many players have learned the default set of Ren'Py keybindings, and
    expect them to be the same from game to game.

In Ren'Py keysyms are strings representing mouse buttons, joystick buttons,
or keyboard keys.

Mouse buttons use keysyms of the form 'mouseup_#' or 'mousedown_#',
where # is a button number. Ren'Py assumes a five button mouse,
where buttons 1, 2, and 3 are the left, middle, and right buttons, while
buttons 4 and 5 are generated by scrolling the wheel up and down.
For example, "mousedown_1" is generally a press of the left mouse button,
"mouseup_1" is a release of that button, and "mousedown_4" is a turn of the
scroll wheel to the top.

Joystick keysyms begin with joy\_. They are defined in :var:`config.joystick_keys`,
and mapped to actual joystick events by the user.

There are two kinds of keyboard keysyms. The first is a string containing a
character that is generated when a key is pressed. This is useful for
binding alphabetic keys and numbers. Examples of these keysyms include "a", "A", and "7".

Keboard keysyms can also be the symbolic name for the key. This can be any of
the K\_ constants taken from pygame.constants. This type of keysym looks like
"K\_BACKSPACE", "K\_RETURN", and "K\_TAB"; a full list of this kind of keysyms may
be found `here <http://www.pygame.org/docs/ref/key.html>`_.

Keyboard keysyms may be preceded by the prefixes "alt\_", "meta\_", "shift\_",
or "noshift\_". The first three of these require the corresponding modifier
key to be pressed. (Meta is present on Linux keyboards, and corresponds to the
Command key on a Mac.) "noshift\_" requires that the shift key not be pressed.

To change a binding, update the appropriate list in :var:`config.keymap`. The
following code adds the 't' key to the list of keys that dismiss a say
statement, and removes the space key from that list. ::

    init:
        $ config.keymap['dismiss'].append('t')
        $ config.keymap['dismiss'].remove('K_SPACE')

The default keymap is contained inside the python code implementing Ren'Py, and
as of version 6.16 is as follows::

    config.keymap = dict(

        # Bindings present almost everywhere, unless explicitly
        # disabled.
        rollback = [ 'K_PAGEUP', 'mousedown_4', 'joy_rollback' ],
        screenshot = [ 's' ],
        toggle_fullscreen = [ 'f', 'alt_K_RETURN', 'alt_K_KP_ENTER', 'K_F11' ],
        toggle_music = [ 'm' ],
        game_menu = [ 'K_ESCAPE', 'mouseup_3', 'joy_menu' ],
        hide_windows = [ 'mouseup_2', 'h', 'joy_hide' ],
        launch_editor = [ 'E' ],
        dump_styles = [ 'Y' ],
        reload_game = [ 'R' ],
        inspector = [ 'I' ],
        developer = [ 'D' ],
        quit = [ 'meta_q', 'alt_K_F4', 'alt_q' ],
        iconify = [ 'meta_m', 'alt_m' ],
        help = [ 'K_F1', 'meta_shift_/' ],
        choose_renderer = [ 'G' ],

        # Say.
        rollforward = [ 'mousedown_5', 'K_PAGEDOWN' ],
        dismiss = [ 'mouseup_1', 'K_RETURN', 'K_SPACE', 'K_KP_ENTER', 'joy_dismiss' ],

        # Pause.
        dismiss_hard_pause = [ ],

        # Focus.
        focus_left = [ 'K_LEFT', 'joy_left' ],
        focus_right = [ 'K_RIGHT', 'joy_right' ],
        focus_up = [ 'K_UP', 'joy_up' ],
        focus_down = [ 'K_DOWN', 'joy_down' ],

        # Button.
        button_ignore = [ 'mousedown_1' ],
        button_select = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],

        # Input.
        input_backspace = [ 'K_BACKSPACE' ],
        input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],
        input_left = [ 'K_LEFT' ],
        input_right = [ 'K_RIGHT' ],
        input_delete = [ 'K_DELETE' ],

        # Viewport.
        viewport_up = [ 'mousedown_4' ],
        viewport_down = [ 'mousedown_5' ],
        viewport_drag_start = [ 'mousedown_1' ],
        viewport_drag_end = [ 'mouseup_1' ],

        # These keys control skipping.
        skip = [ 'K_LCTRL', 'K_RCTRL', 'joy_holdskip' ],
        toggle_skip = [ 'K_TAB', 'joy_toggleskip' ],
        fast_skip = [ '>' ],

        # Bar.
        bar_activate = [ 'mousedown_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
        bar_deactivate = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
        bar_left = [ 'K_LEFT', 'joy_left' ],
        bar_right = [ 'K_RIGHT', 'joy_right' ],
        bar_up = [ 'K_UP', 'joy_up' ],
        bar_down = [ 'K_DOWN', 'joy_down' ],

        # Delete a save.
        save_delete = [ 'K_DELETE' ],

        # Draggable.
        drag_activate = [ 'mousedown_1' ],
        drag_deactivate = [ 'mouseup_1' ],

        # Debug console.
        console = [ 'shift_O' ],
        console_older = [ 'K_UP' ],
        console_newer = [ 'K_DOWN' ],
        )
