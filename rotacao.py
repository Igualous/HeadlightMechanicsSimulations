from manim import *
from numpy import *

# CENA 3: Focada na Álgebra Linear - Rotação (MODIFICADA)
class RotacaoMatricial(Scene):
    def construct(self):
        # --- Configuração Inicial ---
        eixos = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 5, 1], # Ajustado o y_range para a parábola
            axis_config={"include_tip": False}
        ).add_coordinates()
        
        titulo_rotacao = Text("Adaptive Frontlight System (AFS) Simulation", font_size=34).to_edge(UP)
        self.play(Create(eixos))
        self.play(Write(titulo_rotacao))
        self.wait(1)

        # --- Matriz de Rotação ---
        ANGULO = 30

        template_string = (
            "R_{VALOR^\\circ} = "
            "\\begin{bmatrix} "
            "\\cos{VALOR^\\circ} & -\\sin{VALOR^\\circ} \\\\ "
            "\\sin{VALOR^\\circ} &  \\cos{VALOR^\\circ} "
            "\\end{bmatrix}"
        )

        # 2. Substitua o marcador "VALOR" pelo conteúdo da sua variável ANGULO.
        string_final = template_string.replace("VALOR", str(ANGULO))

        # 3. Use MathTex para renderizar a string LaTeX.
        matriz_tex = MathTex(string_final).to_corner(UL).shift(DOWN * 0.8)

        # Animação para exibir a matriz na tela
        self.play(Write(matriz_tex))

        # --- Objeto a ser Rotacionado: Parábola ---

        angulo_rotacao = ANGULO * DEGREES
        
        # --- ALTERAÇÃO: Substituindo o Vetor por uma Parábola ---
        parabola = eixos.plot(
            lambda x: 0.9 * x**2, # Equação da parábola y = 0.3x^2
            x_range=[-1.5, 1.5],
            color=PURPLE
        )
        # O rótulo 'v' e o arco do vetor foram removidos pois não se aplicam diretamente a uma função
        
        self.play(Create(parabola))
        self.wait(1)

        # --- Animação do Volante ---
        raio_circulo = 0.8
        circulo = Circle(radius=raio_circulo, color=WHITE)
        ponto = Dot(radius=0.07, color=YELLOW)
        ponto.move_to(circulo.point_at_angle(0))
        linha_raio = Line(circulo.get_center(), ponto.get_center(), color=BLUE)
        
        arco_volante = Arc(
            radius=raio_circulo * 0.4,
            start_angle=ponto.get_angle(),
            angle=angulo_rotacao,
            color=ORANGE
        )
        rotulo_theta_volante = MathTex("\\theta", color=ORANGE).scale(0.7).next_to(arco_volante, RIGHT, buff=0.1)

        grupo_volante = VGroup(circulo, ponto, linha_raio)
        grupo_angulo_volante = VGroup(arco_volante, rotulo_theta_volante)
        VGroup(grupo_volante, grupo_angulo_volante).to_corner(DL, buff=0.7)

        # --- Animação da seta para esquerda
        arrow_left = Arrow([-3, -3, 0], [-4, -3, 0], buff=0, color=YELLOW)    
        self.add(arrow_left)
        self.play(GrowArrow(arrow_left))
        self.wait(1)
        self.add(grupo_volante)
        self.wait(1)
        
        # --- ANIMAÇÃO SINCRONIZADA ---
        self.play(
            # 1. Rotação da PARÁBOLA
            Rotate(parabola, angle=angulo_rotacao, about_point=parabola.get_bottom()),
            # 2. Rotação do volante
            Rotate(grupo_volante, angle=angulo_rotacao, about_point=circulo.get_center()),
            # 3. Criação do arco e rótulo do volante
            Create(grupo_angulo_volante),
            run_time=2
        )
        
        self.wait(3)
