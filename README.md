# MRE for textual issues with messages between Screns

## installation
```
uv sync
uv run python main.py
```

## Concept

1 App, 2 screens: 
 - Main
 - Load which is in fact a modal dialog to enter a local path

Idea: screens use messages thru the App to communicate data from one to the other

Process: 
1. The App loads the Main screen, using 'l' the user can select a path
2. The Load screen is displayed and sends back a message to the App to provide the path entered by the user
3. The App gets the message and calls some 3rd party API to so something based on the path value and receive some data
4. The App retrieves the Main Screen to call update_tree with the received data => **this is where it crashes, cannot find the Main Screen**
5. the Main Screen updates its Tree

Looks like the App receiving the mesasge is a different instance?

## How to reproduce the issue:

1. Press "l"
2. Press enter or cick OK
3. Error:

```
NoMatches: No nodes match <class 'screens.main_screen.MainScreen'> on TuiApp(title='TuiApp', classes={'-dark-mode'}, pseudo_classes={'focus', 'dark'})
```
