from termcolor import colored, cprint
import termcolor

# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
# print_red_on_cyan('Hello, World!')
# print_red_on_cyan('Hello, Universe!')

# class logger:
def generic_info(context, message, color):
    print(f"[{context:^8}]  : " + colored(f"{message}", color))

class whumpus:
    def info(message):
        generic_info("whumpus", message, "red")
        

class world:
    def info(message):
        generic_info("world", message, "cyan")
        
class agent:
    def info(message):
        generic_info("agent", message, "yellow")
        

