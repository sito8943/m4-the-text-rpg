# THE TEXT-BASED RPG

## Authors
- Carlos Andrés Mora González

## Description
This is an event-driven, text-based role-playing game (RPG) that runs in the terminal. In it, you create your character and venture into the vast world of the "terminal void"—an environment filled with characters and combat.

## How to run

```
python3 ./main.py
```

## How to run tests
```
python3 -m unittest discover tests -v
```

Note: Why unittest instead of pytest? Because it comes with python :)
Note: Why unit tests with classes? Because unittest force you to use classes :)
Note: Why @patch? Because is for mocking and preventing the real calling of methods which affect files or other external things :)