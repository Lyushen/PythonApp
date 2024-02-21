import time
def extract_keys(products):
    result = {}
    used_keys = {}
    
    for product in products:
        # Check if the first letter is already used
        first_letter = product[0]
        if first_letter not in used_keys:
            # If not used, add it to the result and mark as used
            result[first_letter] = product
            used_keys[first_letter] = product
        else:
            # If the first letter is used, check for two-letter key
            # to handle duplicates
            two_letters = product[:2]
            if two_letters not in used_keys:
                result[two_letters] = product
                used_keys[two_letters] = product
            else:
                # In case the two-letter key is also used, you can decide on further steps,
                # such as extending the key length or handling the collision differently.
                # This basic implementation does not handle further conflicts.
                print(f"Conflict detected for key '{two_letters}'. Further handling required.")
    return result

def extract_keys_with_numbers(products):
    result = {}
    counter = 1
    for product in products:
        result[str(counter)] = product
        counter += 1
    return result

def ask_in_range(message, range_limits=[1.0, 5.0], input_type=float):
    while True:
        var1 = input(message + " > ")
        try:
            if input_type == int:
                converted = int(var1)  # Convert to integer if input_type is int
            else:
                converted = float(var1)  # Defaults to converting to float
                
            if converted >= min(range_limits) and converted <= max(range_limits):
                return converted
            else:
                print(f"Input is out of range, please enter a number between {min(range_limits)} and {max(range_limits)}.")
        except ValueError:
            print(f"Invalid input: Please enter a valid {'integer' if input_type == int else 'number'}.")

def ask_a_question(message, possible_answers={'Y': 'Yes', 'N': 'No'}):
    options_str = ', '.join([f"({key}) for {value}" for key, value in possible_answers.items()])
    full_message = f"{message} Possible answers are {options_str}."
    possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
    while True:
        print(full_message) 
        user_input = input().lower() 
        possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
        if user_input in possible_answers_lower:
            for original_key in possible_answers:
                if original_key.lower() == user_input:
                    return original_key.lower() #return answers in the lower case always
        else:
            print(f"Incorrect input. Please enter one of the following options: {options_str}")

def style(message, style):
    style_name = style.upper()
    style_attribute = getattr(BCOLORS, style_name, None)
    str_message=str(message)
    if style_attribute is None:
        return  str_message # Return the original message if the style is not found
    return style_attribute + str_message + BCOLORS.ENDC

class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Timer:
    def __init__(self, identifier=None):
        self.identifier = identifier
        self.start_time = None
        self.pause_time = None
        self.elapsed_time_during_pauses = 0

    def start(self):
        if self.start_time is not None:
            print(f"Timer {self._display_id()} is already running. Use .stop() to stop it or .reset() to reset it.")
            return
        self.start_time = time.perf_counter()
        print(f"Timer {self._display_id()} started.")

    def pause(self):
        if self.start_time is None:
            print(f"Timer {self._display_id()} has not been started.")
            return
        if self.pause_time is not None:
            print(f"Timer {self._display_id()} is already paused.")
            return
        self.pause_time = time.perf_counter()
        print(f"Timer {self._display_id()} paused.")

    def resume(self):
        if self.start_time is None:
            print(f"Timer {self._display_id()} has not been started.")
            return
        if self.pause_time is None:
            print(f"Timer {self._display_id()} is not paused.")
            return
        self.elapsed_time_during_pauses += time.perf_counter() - self.pause_time
        self.pause_time = None
        print(f"Timer {self._display_id()} resumed.")

    def stop(self):
        if self.start_time is None:
            print(f"Timer {self._display_id()} has not been started.")
            return
        if self.pause_time is not None:
            self.resume()  # Resume to get accurate elapsed time before stopping
        end_time = time.perf_counter()
        elapsed_time = end_time - self.start_time - self.elapsed_time_during_pauses
        print(f"Timer {self._display_id()} stopped. Elapsed time: {elapsed_time:.4f} seconds.")
        self.reset()

    def reset(self):
        self.start_time = None
        self.pause_time = None
        self.elapsed_time_during_pauses = 0

    def _display_id(self):
        return f'#{self.identifier}' if self.identifier is not None else '(no id)'

    @staticmethod
    def time_function(func, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function '{func.__name__}' executed in: {end_time - start_time:.4f} seconds")
        return result
    
def safe_cast(value, to_type, default=None):
    try:
        return to_type(value)
    except (ValueError, TypeError) as ex:
        print(f'Error during convertation {ex}')