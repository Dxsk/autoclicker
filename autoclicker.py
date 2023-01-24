

class AutoClicker:
    """  |------------------------------------------------------------------------------------------|
  |[AutoClicker v0.1]                                                                        |
  | Keys mapping :                                                                           |
  |    - Authorized Autoclick                  : ctrl_left + shift_left + L                  |
  |    - Exectue autoclick with C press        : ctrl_left + C                               |
  |    - Execute autoclick without keypress    : L + P                                       |
  |    - Exit program                          : ctrl_left + c OR ctrl_left + shift_left + Q |
  |------------------------------------------------------------------------------------------|
    """
    def __init__(self) -> None:
        self.is_debug = False
        self.trigger_autoclick = False
        self.authorized_autoclick = False
        
        self.keys = ''
        self.hex_left_ctrl = int('0xa2', 16)
        self.hex_left_shift = int('0xa0', 16)
        
        self.mouse_x = ''
        self.mouse_y = ''

        self.humain_sleep = 0.041

    def helper(self):
        print(self.helper.__doc__)

    def status(self):
        """
        Function used to display the status of the current program.
        """
        authorized_response = 'Yes' if self.authorized_autoclick else 'No '
        authorized_message = f"[ Autoclick Authorized -> {authorized_response}]"
        
        running_response = 'Yes' if self.trigger_autoclick else 'No '
        running_message = f"[ Autoclick Running => {running_response}]"

        style_lines = '=' * (10 + len(authorized_message))
        style_space = ' ' * (5 - len(authorized_response))

        os.system('cls')
        print(style_lines)
        print(f"={style_space}{authorized_message}{style_space}=")
        print(f"={style_space}{running_message}{style_space}=")
        print(style_lines)  
        print(self.__doc__)
        sleep(0.5)

    def update_keys(self):
        """
        Function called to update the status of the keys.
        """
        self.keys = {
            "press_c": win32api.GetAsyncKeyState(ord('C')),
            "press_l": win32api.GetAsyncKeyState(ord('L')),
            "press_q": win32api.GetAsyncKeyState(ord('Q')),
            "press_p": win32api.GetAsyncKeyState(ord('P')),
            "press_h": win32api.GetAsyncKeyState(ord('H')),
            "press_left_ctrl": win32api.GetAsyncKeyState(self.hex_left_ctrl),
            "press_left_shift": win32api.GetAsyncKeyState(self.hex_left_shift),
        }

    def update_mouse_position(self):
        """
        Function called to update the coordinates of the mouse.
        """
        self.mouse_x, self.mouse_y = win32api.GetCursorPos()

    def click(self):
        win32api.SetCursorPos((
            self.mouse_x,
            self.mouse_y
        ))
        win32api.mouse_event(
            win32con.MOUSEEVENTF_LEFTDOWN,
            self.mouse_x,
            self.mouse_y,
            0,0
        )
        win32api.mouse_event(
            win32con.MOUSEEVENTF_LEFTUP,
            self.mouse_x,
            self.mouse_y,
            0,0
        )
        sleep(self.humain_sleep)

    @staticmethod
    def toggle(value: bool) -> bool:
        return not value

    @staticmethod
    def give_up():
        os.system('cls')
        sys.exit(0)

    def running(self):
        while True:
            self.update_keys()
            self.update_mouse_position()

            # The autoclick is executed automatically when both conditions are met
            if (self.authorized_autoclick and self.trigger_autoclick):
                self.click()

            # The autoclick is run with the C key pressed
            if (self.authorized_autoclick and self.keys.get('press_c')):
                self.click()

            # Switching the authorisation of the autoclicker
            if (
                self.keys.get('press_left_ctrl')
                and self.keys.get('press_left_shift')
                and self.keys.get('press_l')
            ):
                self.authorized_autoclick = self.toggle(self.authorized_autoclick)
                self.status()

            # Switching the authorisation of the automatic execution
            if self.authorized_autoclick and (
                self.keys.get('press_p') and self.keys.get('press_l')
            ):
                self.trigger_autoclick = self.toggle(self.trigger_autoclick)
                self.status()

            # Exit the program
            if (
                self.keys.get('press_left_ctrl')
                and self.keys.get('press_left_shift')
                and self.keys.get('press_q')
            ):
                self.give_up()


def main():
    ac = AutoClicker()
    print(ac.__doc__)

    if len(sys.argv) >= 2 and sys.argv[2] == 'debug':
        ac.is_debug = True

    ac.running()


if __name__ == "__main__":
    import os
    import sys
    from time import sleep
    try:
        import win32api, win32con
    except ModuleNotFoundError:
        print('Autoclicker is only for Windows (win32api & win32con are used)')
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        os.system('cls')
        sys.exit(0)
