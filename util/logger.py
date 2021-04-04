from termcolor import colored, cprint
import termcolor

# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
# print_red_on_cyan('Hello, World!')
# print_red_on_cyan('Hello, Universe!')

# class logger:
def generic_info(context, message, color):
    print(f"[{context:^8}]  : " + colored(f"{message}", color))

class whumpusLogger:
    def info(message):
        generic_info("🐸", message, "red")
        
class worldLogger:
    def info(message):
        generic_info("⛳", message, "cyan")
        
class agentLogger:
    def info(message):
        generic_info("👨", message, "yellow")
