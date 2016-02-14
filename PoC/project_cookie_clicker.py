"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)
# import matplotlib.pyplot as plt
import math
import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.__total_cookies = 0.0
        self.__current_cookies = 0.0
        self.__current_time = 0.0
        self.__current_cps = 1.0
        self.__history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return ('The Clicker State:\nTotal cookies:\t%.2f\nCurrent time:\t%.2f\nCurrent cookies:\t%.2f\nCurrent CPS:\t%.2f\n' \
                % (self.__total_cookies, self.__current_time, self.__current_cookies, self.__current_cps)) + str(self.__history)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.__current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.__current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.__current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.__history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.__current_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self.__current_cookies) / self.__current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        else:
            self.__total_cookies += self.__current_cps * time
            self.__current_cookies += self.__current_cps * time
            self.__current_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.__current_cookies:
            return
        self.__current_cookies -= cost
        self.__current_cps += additional_cps
        self.__history.append((self.__current_time, item_name, cost, self.__total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(),
                        build)
        if not item:
            break
        time_to_wait = clicker.time_until(build.get_cost(item))
        if clicker.get_time() + time_to_wait > duration:
            break
        clicker.wait(time_to_wait)
        clicker.buy_item(item, build.get_cost(item), build.get_cps(item))
        build.update_item(item)
    if clicker.get_time() < duration:
        clicker.wait(duration - clicker.get_time())
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    available_cookies = cookies + cps * time_left
    items = build_info.build_items()
    available_items = [item for item in items if build_info.get_cost(item) <= available_cookies]
    if not available_items:
        return None
    min_item = ''
    min_cost = float('inf')
    for item in available_items:
        if build_info.get_cost(item) < min_cost:
            min_item = item
            min_cost = build_info.get_cost(item)
    return min_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    available_cookies = cookies + cps * time_left
    items = build_info.build_items()
    available_items = [item for item in items if build_info.get_cost(item) <= available_cookies]
    if not available_items:
        return None
    max_item = ''
    max_cost = float('-inf')
    for item in available_items:
        if build_info.get_cost(item) > max_cost:
            max_item = item
            max_cost = build_info.get_cost(item)
    return max_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    available_cookies = cookies + cps * time_left
    items = build_info.build_items()
    available_items = [item for item in items if build_info.get_cost(item) <= available_cookies]
    if not available_items:
        return None
    max_item = ''
    max_ratio = 0.0
    for item in available_items:
        if (build_info.get_cps(item) / build_info.get_cost(item)) > max_ratio:
            max_item = item
            max_ratio = build_info.get_cps(item) / build_info.get_cost(item)
    return max_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
