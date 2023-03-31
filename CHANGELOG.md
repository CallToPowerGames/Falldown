# Falldown

## Changelog

### v1.8.0

* Added controller support
    * Supported controllers:
        * XBox 360
        * Nintendo Pro
    * Controller hot plugging
        * App knows when controllers are added/removed
* Improved quitting the application
* Drawing optimizations
* General bug fixing, cleaning up and refactoring

### v1.7.0

* Added player dying and death animations
* Fixed bug in and cleaned up player AI
* You can now let a specific player AI play
    * Instead of waiting or pressing "k" in the main menu
    * Select a player in the player selection menu and press "k"
* Graphically improved segments
* Improved per-player-sprite animations
* Bug fix: Options overwritten when game config version changed
* General bug fixing, cleaning up and refactoring

### v1.6.0

* New font
* Antialiased texts
* Refined UI
* Refined pause menu
* Refined options menu
* More options:
    * Switch on/off music
    * Switch on/off effects
    * Increase/decrease volume of music
    * Increase/decrease volume of effects
* Indicator in options menu whether the option is currently switched on/off
* General bug fixing, cleaning up and refactoring

### v1.5.0

* Added player AIs
* After 10 seconds of inactivity in the main screen a player AI starts to play the game with a randomly selected player
* Pressing any button returns to the main menu
* When the player AI's game is over, the game returns to the main menu
* Music and background generation hardening
* Improved loading bar
* General bug fixing, cleaning up and refactoring

### v1.4.0

* Added (randomized) cloud background images
* Added parallax scrolling for the background (background image and clouds)
* Added an option to deactivate the background image
* Added a (random) cloud scale factor for cloud variations
* Added a scrolling level as background (when not in-game)
* Added specific loading texts in loading screen
* Added a very (VERY) high limit of steps that the player can fall down. Should never be reached even closeley, but better save than sorry.
* General bug fixing, cleaning up and refactoring

### v1.3.0

* Internationalization (i18n) added
    * Two languages
        * English
        * German
    * New option to switch languages under "Options"
    * Selected language gets saved to configuration and is loaded at startup
* Config file versioning
* General bug fixing, cleaning up and refactoring

### v1.2.0

* New Powers
    * Clear a single segment
    * Clear all segments
* New cache
* General bug fixing, cleaning up and refactoring

### v1.1.0

* Additional player info on pressing Tab in player selection
* Log improvements
    * Logs written to user folder
    * Log file and log level configurable
* Improved stuck prevention
* Press Escape to pause in-game
* Performance improvements
* New installer
* Border-out images to grahically improve the outer border
* General bug fixing, cleaning up and refactoring

### v1.0.0

Initial version