from manim import *
import numpy as np

class EspelhoParabolico(Scene):
     def construct(self):
        # --- Configuração Inicial ---
        distancia_focal = 2
        eixos = Axes(
            x_range=[-2, 10, 2],
            y_range=[-6, 6, 2],
            x_length=10,
            y_length=8,
            axis_config={"color": GREY, "include_tip": False}
        ).add_coordinates()
        self.play(Create(eixos), run_time=1)

        # --- Criação da Parábola e Foco ---
        parabola = eixos.plot_parametric_curve(
            lambda t: np.array([ (t**2) / (4 * distancia_focal), t, 0 ]),
            t_range=np.array([-6, 6]),
            color=BLUE,
            use_smoothing=True
        )
        self.play(Create(parabola), run_time=2)

        foco_ponto = eixos.coords_to_point(distancia_focal, 0)
        foco_marcador = Dot(foco_ponto, color=RED)
        foco_rotulo = MathTex("F").next_to(foco_marcador, DOWN)
        self.play(FadeIn(foco_marcador), Write(foco_rotulo))
        self.wait(1)

        # --- Preparação dos Raios ---
        angulos = [-75, -70, -65, -60, -55, -40, -20, 20, 40, 55, 60, 65, 70, 75]
        grupo_raios = VGroup()
        grupo_refletidos = VGroup()

        for angulo in angulos:
            rad = np.radians(angulo)
            if np.abs(np.tan(rad)) > 1e-6:
                y_intersecao = (4 * distancia_focal) / np.tan(rad)
                x_intersecao = (y_intersecao**2) / (4 * distancia_focal)
            else:
                x_intersecao = 9
                y_intersecao = 0

            ponto_final_raio = eixos.coords_to_point(x_intersecao, y_intersecao)
            raio_incidente = Arrow(foco_ponto, ponto_final_raio, buff=0, color=YELLOW)
            ponto_final_refletido = ponto_final_raio + RIGHT * 4
            raio_refletido = Arrow(ponto_final_raio, ponto_final_refletido, buff=0, color=ORANGE)
            
            grupo_raios.add(raio_incidente)
            grupo_refletidos.add(raio_refletido)

        # --- Animação Corrigida dos Raios ---
        lista_de_animacoes = []
        for raio_inc, raio_refl in zip(grupo_raios, grupo_refletidos):
            animacao_do_par = AnimationGroup(
                GrowArrow(raio_inc),
                GrowArrow(raio_refl)
            )
            lista_de_animacoes.append(animacao_do_par)
        
        self.play(LaggedStart(*lista_de_animacoes, lag_ratio=0.3, run_time=4))
        self.wait(2)

        titulo = Text("Raios do foco refletem paralelamente ao eixo.", font_size=36).to_edge(UP)
        self.play(Write(titulo))
        self.wait(3)