#!/usr/bin/env python3

import pyautogui
import sys
import time


class DuckEnv:
    def __init__(self, default_delay: int):
        self.default_delay = default_delay

def execute(path: str) -> None:
    env = DuckEnv(5)

    with open(path) as file:
        history = []
        for line in file:
            time.sleep(env.default_delay / 1000)
            _execute_line(line, history, env)
            history.append(line)


def _execute_line(line: str, history: list[str], env: DuckEnv) -> None:
    line = line.strip()

    if line == '':
        return

    cmd, _, args = line.partition(' ')

    if cmd in ['REM']:
        print(args)
    elif cmd in ['DEFAULT_DELAY', 'DEFAULTDELAY']:
        env.default_delay = int(args)
    elif cmd in ['DELAY']:
        time.sleep(int(args) / 1000)
    elif cmd in ['STRING']:
        pyautogui.typewrite(args, interval=0.005)
    elif cmd in ['BREAK', 'PAUSE']:
        pyautogui.hotkey('ctrl', 'break')
    elif cmd in ['REPEAT']:
        for i in range(int(args)):
            _execute_line(history[-1], history[:-1], env)

    # Flipper Zero additional syntax
    elif cmd in ['ALTCHAR']: # TODO: Windows only
        with pyautogui.hold('alt'):
            pyautogui.press(list(args))
    elif cmd in ['ALTSTRING', 'ALTCODE']: # TODO
        pyautogui.typewrite(args, interval=0.005)
    elif cmd in ['SYSRQ']: # TODO
        raise NotImplementedError

    # Just key sequence
    else:
        replacements = {
            'WINDOWS': 'WIN',
            'GUI': 'WIN',
            'MENU': 'OPTIONLEFT',
            'APP': 'OPTIONLEFT',
            'CONTROL': 'CTRL',
            'DOWNARROW': 'DOWN',
            'LEFTARROW': 'LEFT',
            'RIGHTARROW': 'RIGHT',
            'UPARROW': 'UP',
            'ESCAPE': 'ESC',

            'CTRL-ALT': 'CTRL ALT',
            'CTRL-SHIFT': 'CTRL SHIFT',
            'ALT-SHIFT': 'ALT SHIFT',
            'ALT-GUI': 'ALT GUI',
            'GUI-SHIFT': 'GUI SHIFT',
        }

        for key, replacement in replacements.items():
            line = line.replace(key, replacement)

        keys = line.lower().split(' ')
        for key in keys:
            if key not in pyautogui.KEY_NAMES:
                print(f'Unknown key {key}')

        pyautogui.hotkey(*keys)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage:\n\t{sys.argv[0]} path')
        exit(1)

    execute(sys.argv[1])
