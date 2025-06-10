MRE for textual issues with messages between Screns

# installation
```
uv sync
uv run python main.py
```

# How to reproduce the issue:

1. Press "l"
2. Press enter or cick OK
3. Error:

```
NoMatches: No nodes match <class 'screens.main_screen.MainScreen'> on TuiApp(title='TuiApp', classes={'-dark-mode'}, pseudo_classes={'focus', 'dark'})
```
