from manim import *
import numpy as np

class ReflexaoMatricial(Scene):
    def construct(self):
        eixos = Axes(
            x_range=[-5, 5, 2],
            y_range=[-4, 4, 1],
            axis_config={"include_tip": False}
        ).add_coordinates()
        
        titulo_matriz = Text("Reflexão através do eixo X", font_size=32).to_edge(UP)
        self.play(Create(eixos))
        self.play(Write(titulo_matriz))
        self.wait(1)

        matriz_tex = MathTex(
            "M = \\begin{bmatrix} 1 & 0 \\\\ 0 & -1 \\end{bmatrix}"
        ).to_corner(UL).shift(DOWN*0.8) # Afasta do título
        self.play(Write(matriz_tex))

        # Matriz de reflexão
        M = np.array([
            [1, 0],
            [0, -1]
        ])

        vetor_original = Vector([3, 2], color=PURPLE)
        rotulo_original = MathTex("v").next_to(vetor_original.get_end(), UR)

        vetor_transformado = Vector(M @ np.array([3, 2]), color=TEAL)
        rotulo_transformado = MathTex("Mv").next_to(vetor_transformado.get_end(), DR)

        self.play(
            GrowArrow(vetor_original),
            Write(rotulo_original)
        )
        self.wait(1)
        self.play(
            Transform(vetor_original.copy(), vetor_transformado),
            Write(rotulo_transformado)
        )
        self.wait(2)

        explicacao = Text(
            "Um vetor no eixo x não muda de direção.\nEle é um autovetor!",
            font_size=28
        ).to_corner(DL)
        
        autovetor = Vector([4, 0], color=ORANGE)
        rotulo_autovetor = MathTex("v_1", color=ORANGE).next_to(autovetor.get_end(), UP)
      
        autovetor_transformado = Vector(M @ np.array([4, 0]), color="RED")
        rotulo_autovetor_transformado = MathTex("Mv_1", color=RED).next_to(autovetor_transformado.get_end(), DR)
        
        self.play(Write(explicacao))
        self.play(GrowArrow(autovetor), Write(rotulo_autovetor))
        self.wait(1)
        self.play(GrowArrow(autovetor_transformado), Write(rotulo_autovetor_transformado))
        self.wait(3)
