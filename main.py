"""
Jogo da velha feito com Python e Tkinter
"""
import tkinter as tk
from functools import partial
from PIL import ImageTk, Image


class App:
    """ Classe principal do aplicativo"""
    def __init__(self):
        self.launch()

    def launch(self):
        """Inicialização do aplicativo"""
        self.win = tk.Tk()
        self.win.title("Velha")
        self.win.resizable(False, False)

        main_frame = tk.Frame(self.win, background="black")
        main_frame.pack()

        # Colocando as imagens na memória
        self.img_cross = ImageTk.PhotoImage(Image.open("assets/imgs/cross.png"))
        self.img_circle = ImageTk.PhotoImage(Image.open("assets/imgs/circle.png"))
        self.img_blank = ImageTk.PhotoImage(Image.open("assets/imgs/blank.png"))

        # Inicializando os botões
        self.but_pos = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        ]

        self.buttons = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        for pos in self.but_pos:
            but = tk.Button(
                main_frame,
                border=1,
                command=partial(self.mark, pos),
                image=self.img_blank,
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
        self.reset_button = tk.Button(
            main_frame,
            text="Reset",
            command=self.reset,
        )
        self.reset_button.grid(row=4, column=1, sticky="nsew")

        # Estado(Ainda jogando, X ou O ganhou, empate)
        self.estado = tk.StringVar(main_frame, value="")
        self.win_label = tk.Label(
            main_frame,
            textvariable=self.estado,
            background="black"
        )
        self.win_label.grid(row=4, column=2, sticky="nsew")

        # Placar
        self.placar_o = 0
        self.placar_x = 0
        self.placar_var = tk.StringVar(main_frame, value="X: 0, O: 0")
        placar = tk.Label(
            main_frame,
            textvariable=self.placar_var,
        )
        placar.grid(row=4, column=0, sticky="nsew")


    def pass_turn(self):
        """ Gerencia os turnos"""
        if self.turn:
            self.turn = False
        else:
            self.turn = True


    def mark(self, pos):
        """ Altera a imagem na posição [pos] de acordo com o turno """
        but = self.buttons[pos[0]][pos[1]]


        if self.turn:
            but["image"] = self.img_circle
            but["text"] = True
        else:
            but["image"] = self.img_cross
            but["text"] = False

        but["width"] = 64
        but["height"] = 64
        but["state"] = "disabled"

        self.pass_turn()
        self.check()


    def reset(self):
        """ Reinicia o jogo, mas mantém o placar"""
        for pos in self.but_pos:
            but = self.buttons[pos[0]][pos[1]]
            but["image"] = self.img_blank
            but["text"] = "blank"
            but["width"] = 64
            but["height"] = 64

        self.estado.set("")
        self.win_label["background"] = "black"
        self.won = False

        for pos in self.but_pos:
            but = self.buttons[pos[0]][pos[1]]
            but["state"] = "normal"


    def win_event(self):
        """ Eventos que devem ser executados após qualquer um dos jogadores ganhar"""
        self.won = True
        self.placar_var.set(mount_score(self.placar_o, self.placar_x))
        for pos in self.but_pos:
            but = self.buttons[pos[0]][pos[1]]
            but["state"] = "disabled"


    def win_cross(self):
        """ Eventos que devem ser executados caso X ganhe"""
        self.estado.set("X Ganhou")
        self.win_label["background"] = "white"
        self.placar_x += 1

        self.win_event()


    def win_circle(self):
        """ Eventos que devem ser executados caso O ganhe"""
        self.estado.set("O ganhou")
        self.win_label["background"] = "white"
        self.placar_o += 1

        self.win_event()


    def check(self):
        """ Avalia se algum dos jogadores ganhou ou se empatou"""
        # Possíveis linhas ganhadoras
        lines_to_win = [
            [self.but_pos[0], self.but_pos[1], self.but_pos[2]],
            [self.but_pos[3], self.but_pos[4], self.but_pos[5]],
            [self.but_pos[6], self.but_pos[7], self.but_pos[8]],

            [self.but_pos[0], self.but_pos[3], self.but_pos[6]],
            [self.but_pos[1], self.but_pos[4], self.but_pos[7]],
            [self.but_pos[2], self.but_pos[5], self.but_pos[8]],

            [self.but_pos[0], self.but_pos[4], self.but_pos[8]],
            [self.but_pos[2], self.but_pos[4], self.but_pos[6]],
        ]

        accept = [
            [1, 1, 1],
            [0, 0, 0]
        ]

        for line in lines_to_win:
            values = []
            for pos in line:
                but = self.buttons[pos[0]][pos[1]]
                values.append(but["text"])

            if values == accept[0]:
                print("'O' ganhou")
                self.win_circle()
                break

            if values == accept[1]:
                print("'X' ganhou")
                self.win_cross()
                break

        self.check_draw()


    def check_draw(self):
        """Avalia se há empate"""
        buttons = [self.buttons[pos[0]][pos[1]] for pos in self.but_pos]
        if not self.won and all([(but["state"] == "disabled") for but in buttons]):
            self.estado.set("Empate")
            self.win_label["background"] = "white"
            print("Empate")


def mount_score(circle_score, cross_score):
    """ Monta o placar"""
    return f"X: {cross_score}  O: {circle_score}"


def main():
    """ Lógica de execução do programa"""
    app = App()
    app.win.mainloop()


if __name__ == "__main__":
    main()
