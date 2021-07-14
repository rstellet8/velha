import tkinter as tk
from functools import partial
from PIL import ImageTk, Image


class App:
    def __init__(self):
        self.launch()

    def launch(self):
        self.win = tk.Tk()
        self.win.title("Velha")
        self.win.resizable(False, False)

        mainFrame = tk.Frame(self.win, background="black")
        mainFrame.pack()

        # Colocando as imagens na memória
        self.imgCross = ImageTk.PhotoImage(Image.open("assets/imgs/cross.png"))
        self.imgCircle = ImageTk.PhotoImage(Image.open("assets/imgs/circle.png"))
        self.imgBlank = ImageTk.PhotoImage(Image.open("assets/imgs/blank.png"))

        # Inicializando os botões
        self.butPos = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        ]

        self.buttons = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        for pos in self.butPos:
            but = tk.Button(
                mainFrame,
                border=1, 
                command=partial(self.mark, pos),
                image=self.imgBlank,
                text=None
                )

            but.grid(
                row=pos[0], 
                column=pos[1], 
                padx=1, 
                pady=1, 
                sticky="nsew"
            )

            self.buttons[pos[0]][pos[1]] = but

        # Gerenciador de Turnos
        self.turn = True

        # Indicador que alguem ganhou
        self.won = False

        # Botão de Reset
        self.resetButton = tk.Button(
            mainFrame,
            text="Reset",
            command=self.reset,
        )
        self.resetButton.grid(row=4, column=1, sticky="nsew")

        # Estado
        self.estado = tk.StringVar(mainFrame, value="")
        self.winLabel = tk.Label(
            mainFrame,
            textvariable=self.estado,
            background="black"
        )
        self.winLabel.grid(row=4, column=2, sticky="nsew")

        # Placar
        self.placarO = 0
        self.placarX = 0
        self.placarVar = tk.StringVar(mainFrame, value=f"X: 0, O: 0")
        placar = tk.Label(
            mainFrame,
            textvariable=self.placarVar,
        )
        placar.grid(row=4, column=0, sticky="nsew")


    def passTurn(self):
        if self.turn == True:
            self.turn = False
        else:
            self.turn = True
    
    def _mountScore(self, O, X):
        return f"X: {X}, O: {O}"


    def mark(self, pos):
        but = self.buttons[pos[0]][pos[1]]

        if self.turn:
            but["image"] = self.imgCircle
            but["text"] = True
        else:
            but["image"] = self.imgCross
            but["text"] = False

        but["width"] = 64
        but["height"] = 64
        but["state"] = "disabled"
        
        self.passTurn()
        self.check()


    def reset(self):
        for pos in self.butPos:
            but = self.buttons[pos[0]][pos[1]]
            but["image"] = self.imgBlank
            but["text"] = "blank"
            but["width"] = 64
            but["height"] = 64

        self.estado.set("")
        self.winLabel["background"] = "black"
        self.won = False

        for pos in self.butPos:
            but = self.buttons[pos[0]][pos[1]]
            but["state"] = "normal"


    def winEvent(self):
        self.won = True
        self.placarVar.set(self._mountScore(self.placarO, self.placarX))
        for pos in self.butPos:
            but = self.buttons[pos[0]][pos[1]]
            but["state"] = "disabled"


    def winCross(self):
        self.estado.set("X Ganhou")
        self.winLabel["background"] = "white"
        self.placarX += 1

        self.winEvent()


    def winCircle(self):
        self.estado.set("O ganhou")
        self.winLabel["background"] = "white"
        self.placarO += 1

        self.winEvent()
    

    def check(self):
        # Possíveis linhas ganhadoras
        linesToWin = [
            [self.butPos[0], self.butPos[1], self.butPos[2]],
            [self.butPos[3], self.butPos[4], self.butPos[5]],
            [self.butPos[6], self.butPos[7], self.butPos[8]],

            [self.butPos[0], self.butPos[3], self.butPos[6]],
            [self.butPos[1], self.butPos[4], self.butPos[7]],
            [self.butPos[2], self.butPos[5], self.butPos[8]],

            [self.butPos[0], self.butPos[4], self.butPos[8]],
            [self.butPos[2], self.butPos[4], self.butPos[6]],
        ]

        accept = [
            [1, 1, 1],
            [0, 0, 0]
        ]

        for line in linesToWin:
            values = []
            for pos in line:
                but = self.buttons[pos[0]][pos[1]]
                values.append(but["text"])
            
            if values == accept[0]:
                print("'O' ganhou")
                self.winCircle()
                break
            
            elif values == accept[1]:
                print("'X' ganhou")
                self.winCross()
                break

        self._checkDraw()

    def _checkDraw(self):
        buttons = [self.buttons[pos[0]][pos[1]] for pos in self.butPos]
        if not self.won and all([(but["state"] == "disabled") for but in buttons]) :
            self.estado.set("Empate")
            self.winLabel["background"] = "white"
            print("Empate")

def main():
    app = App()
    app.win.mainloop()

main()