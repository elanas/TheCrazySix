[ ]Update fuzzy graphics for Player/Enemy - *HANSONG*
[ ]Add enemies to Game
    - should be very easy given that it's code that the Player already has being done to it
    - they already are animated (note this in README)
    - Can handle map collisions (walls/objects) in the same way the Player does
[ ]Intermediate GameState to get Player's name - *MICHAEL*
    - likely will use keyboard input for now (later has to support gamepad, but not yet)
    - this will either be saved in Globals or sent along to the Player
[ ]Player changes
    - check for enemy collisions and take damage (use health bar)
        * calls function in HealthBar to decrease health
    - maybe fix outrunning camera and/or speed? not super important
    - maybe fix stair collision (happens too suddenly atm) - not super important
        * scale player's rect before checking for collision to make it more accurate visually
    - Make HealthBar class
        * makes changing the way it's draw much easier
        - handles drawing health bar in top (left?) of screen
        - have a health in range [0, 100]
        - have a function "isDead" --> Boolean
        - incrHealth, decrHealth functions
    - Make Score class
        * makes changing the way it's drawn much easier
        - handles drawing score in top (center? right?) of screen
    - Handle collisions with new special tiles - *MICHAEL*
        - call function in Score class to increase health
[ ]End Game States - *HANSONG*
    - Die Screen
    - Win Screen
        * these are very related but will likely have different text and/or graphics
    - both are sent Player's name (this is in Globals), Score class instance, HealthBar class instance
    - gives points based off of current score and remaining health if any
[ ]HighScore screen
    - optionally receives current Player's name and score
    - has to display high scores or a placeholder (ex: N/A or a dash) if not enough exist
    - maybe highlight the current player's name?
    [x] HighScoreManager - *MICHAEL*
        - has to load and save from text file
        - addPlayer(PlayerName, Score)
            - adds the current player to the correct position in the highscores if they belong there
        - getHighScores() --> list of name/score pairs
            - if not enough exist, some might be None
