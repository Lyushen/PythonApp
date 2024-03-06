
import tkinter as tk
import random
from tkinter import messagebox
from typing import Callable 

class Player:
    def __init__(self, player_name : str, target_score : int,  callback_end_dice_game : Callable):
         self.player_name : str = player_name
         self.target_score : int = target_score
         self.callback_end_dice_game : Callable = callback_end_dice_game
         self.current_score : int = 0
         self.number_throws : int = 0
    
    def throw_dice(self):
        dice_value : int = random.randint(1,6)
        self.current_score += dice_value
        self.number_throws +=1
        if self.current_score >= self.target_score:
            self.on_target_reached()

    def on_target_reached(self):
        self.callback_end_dice_game(f"{self.player_name} has scored {self.current_score} in {self.number_throws}")
        

class GameScreen:
    def __init__(self, root : tk.Tk):
        self.root : tk.Tk = root
        self.root.title("Demo of Simple Callback")
        self.root.geometry("500x600")
        self.root.config(bg = "#0FFFFF")
        
        self.score_label : tk.Label = tk.Label(self.root, padx="0", pady="0", relief="ridge", text = f"Score = 0 ",  font=("Arial",24))
        self.score_label.pack()
        
        self.player : Player = Player("Tom", 40, self.end_dice_game)
        
       
    def start_dice_game(self):
        self.game_on : bool = True
        self.play_dice_game()
    
    def end_dice_game(self, end_message : str = ""):
        self.game_on = False
        self.score_label.config(text = f"score: {self.player.current_score}")
        messagebox.showinfo("Game ended", end_message)    
        
    def play_dice_game(self):
        if self.game_on:
            self.player.throw_dice()
            self.score_label.config(text = f"score: {self.player.current_score}")
            self.root.after(1000, self.play_dice_game)
            
        


def main():
    root = tk.Tk()
    game = GameScreen(root)
    game.start_dice_game()
    game.root.mainloop()




if __name__ == "__main__":
 main()

