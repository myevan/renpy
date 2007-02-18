# Copyright 2004-2006 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# This file contains code fo the main menu, and anything else that
# happens upon initial execution of a Ren'Py program.

init -498:

    python hide:

        config.old_names['Quit'] = 'Quit Game'
        
        # The contents of the main menu.
        config.main_menu = [
            ( u"Start Game", "start", 'True'),
            ( u"Continue Game", _intra_jumps("_load_screen", "main_game_transition"), 'True' ),
            ( u"Preferences", _intra_jumps("_prefs_screen", "main_game_transition"), 'True' ),
            ( u"Quit",  ui.jumps("_quit"), 'True' ),
            ]

        # If not None, this is used to fix the positions of the
        # things in the main menu.
        config.main_menu_positions = None

        # Music to play at the main menu.
        config.main_menu_music = None

        # Callbacks to run at start.
        config.start_callbacks = [ ]
        
# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    python hide:
        for i in config.start_callbacks:
            i()
    
    call _check_module from _call__check_module_1

    call _load_reload_game from _call__load_reload_game_1

    scene black

    if not _restart:
        $ renpy.pause(0)

    $ renpy.block_rollback()

    if renpy.has_label("splashscreen") and not _restart:
        call expression "splashscreen" from _call_splashscreen_1

    $ renpy.block_rollback()

    if config.main_menu_music:
        $ renpy.music.play(config.main_menu_music, if_changed=True)

    # Clean out any residual scene from the splashscreen.
    scene black

    if _restart == None:
        $ renpy.transition(config.end_splash_transition)
    elif _restart == "main_menu":
        $ renpy.transition(config.game_main_transition)
    else:
        $ renpy.transition(config.end_game_transition)
        
    
    $ renpy.call_in_new_context("_enter_main_menu")

    # If the main menu returns, then start the game.
    jump start

# At this point, we've been switched into a new context. So we
# initialize it.
label _enter_main_menu:

    call _enter_menu from _call__enter_menu_1

    $ renpy.context().main_menu = True
    
# This is called to show the main menu to the user.
label _main_menu:    

    # Let the user completely override the main menu. (But please note
    # it still lives in the menu context, rather than the game context.)
    if renpy.has_label("main_menu"):
        jump expression "main_menu"

# This is the default main menu, which we get if the user hasn't
# defined his own, or if that function calls this explicitly.        
label _library_main_menu:

    python hide:

        ui.add(renpy.Keymap(toggle_fullscreen = renpy.toggle_fullscreen))

        ### mm_root default
        # (window) The style used for the root window of the main
        # menu. This is primarily used to set a background for the
        # main menu.

        ui.window(style='mm_root')
        ui.null()

        ### mm_menu_frame default
        # (window) A window that contains the choices in
        # the main menu. Change this to change the placement of
        # these choices on the main menu screen.

        ### mm_menu_frame_vbox thin_vbox
        # (box) The vbox containing the main menu choices.

        if not config.main_menu_positions:
            ui.window(style='mm_menu_frame')
            ui.vbox(style='mm_menu_frame_vbox')

        for text, clicked, enabled in config.main_menu:

            if isinstance(clicked, basestring):
                clicked = ui.jumpsoutofcontext(clicked)

            ### mm_button menu_button
            # (window, hover) The style that is used on buttons that are
            # part of the main menu.

            ### mm_button_text menu_button_text
            # (text, hover) The style that is used for the labels of
            # buttons that are part of the main menu.

            if config.main_menu_positions:
                kwargs = config.main_menu_positions.get(text, { })
            else:
                kwargs = { }

            if not eval(enabled):
                clicked = None
                disabled = True
            else:
                disabled = False

            _button_factory(text, "mm", clicked=clicked, disabled=disabled, properties=kwargs)

        if not config.main_menu_positions:
            ui.close()

        store._result = ui.interact(suppress_overlay = True,
                                    suppress_underlay = True,
                                    mouse="mainmenu")

    # Computed jump to the appropriate label.
    jump _main_menu