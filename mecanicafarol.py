from manim import *
import numpy as np

class MecanicaFarol(Scene):
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

        # --- Criação da Parábola Esquerda ---
        parabolaE = eixos.plot_parametric_curve(
            lambda t: np.array([ (t**2) / (4 * distancia_focal), t, 0 ]),
            t_range=np.array([-6, 6]),
            color=BLUE,
            use_smoothing=True
        )
        self.play(Create(parabolaE), run_time=2)
        
        # --- Criação da Parábola Direita
        deslocamento_horizontal = 1.8 * distancia_focal

        parabolaD = eixos.plot_parametric_curve(
            # Equação paramétrica: x(t) = deslocamento - t^2 / (4*f), y(t) = t
            lambda t: np.array([deslocamento_horizontal - (t**2) / (4 * distancia_focal), t, 0]),
            t_range=np.array([-1.3, 1.3]), # O range de 't' controla a altura da parábola
            color=GREEN_C,
            use_smoothing=True,
            stroke_width=6
        )
        self.play(Create(parabolaD), run_time=2)      
        
        # Criação do ponto focal
        foco_ponto = eixos.coords_to_point(distancia_focal, 0)
        foco_marcador = Dot(foco_ponto, color=RED)
        foco_rotulo = MathTex("FC").next_to(foco_marcador, DOWN)
        self.play(FadeIn(foco_marcador), Write(foco_rotulo))
        self.wait(1)

        # --- Preparação e Animação dos Raios ---
        angulos = [-75, -70, -65, -60, -55, -40, 40, 55, 60, 65, 70, 75]
        lista_de_animacoes = [] # Construiremos a lista de animações diretamente

        for angulo in angulos:
            rad = np.radians(angulo)
            if np.abs(np.tan(rad)) > 1e-6:
                if abs(angulo) == 40:
                    # Cálculo para interseção com a parábola Direita
                    f = distancia_focal
                    d = deslocamento_horizontal
                    a_coeff, b_coeff, c_coeff = 1, (4 * f) / np.tan(rad), -2 * f**2
                    discriminante = np.sqrt(b_coeff**2 - 4 * a_coeff * c_coeff)
                    y1, y2 = (-b_coeff + discriminante) / (2 * a_coeff), (-b_coeff - discriminante) / (2 * a_coeff)
                    y_intersecao = y1 if angulo > 0 else y2
                    x_intersecao = d - (y_intersecao**2) / (4 * f)
                else:
                    # Cálculo original para interseção com a parábola Esquerda
                    y_intersecao = (4 * distancia_focal) / np.tan(rad)
                    x_intersecao = (y_intersecao**2) / (4 * distancia_focal)
            else:
                x_intersecao, y_intersecao = 9, 0

            ponto_final_raio = eixos.coords_to_point(x_intersecao, y_intersecao)
            
            # O raio incidente é criado para todos os ângulos
            raio_incidente = Arrow(foco_ponto, ponto_final_raio, buff=0, color=YELLOW)

            # --- INÍCIO DA NOVA LÓGICA DE ANIMAÇÃO ---
            
            # Para os ângulos 40 e -40, a animação é apenas o raio incidente
            if abs(angulo) == 40:
                animacao_do_raio = GrowArrow(raio_incidente)
            # Para os outros, a animação inclui o raio refletido
            else:
                ponto_final_refletido = ponto_final_raio + RIGHT * 4
                raio_refletido = Arrow(ponto_final_raio, ponto_final_refletido, buff=0, color=ORANGE)
                animacao_do_raio = AnimationGroup(
                    GrowArrow(raio_incidente),
                    GrowArrow(raio_refletido)
                )
            
            lista_de_animacoes.append(animacao_do_raio)
            # --- FIM DA NOVA LÓGICA ---

        # Executa a lista de animações que acabamos de construir
        self.play(LaggedStart(*lista_de_animacoes, lag_ratio=0.3, run_time=4))

        # --- Seção dos raios de -80 e 80 (permanece inalterada) ---
        angulos_finais = [-80, 80]
        grupo_raios = VGroup()
        grupo_refletidos = VGroup()

        for angulo in angulos_finais:
            rad = np.radians(angulo)
            if np.abs(np.tan(rad)) > 1e-6:
                y_intersecao = (4 * distancia_focal) / np.tan(rad)
                x_intersecao = (y_intersecao**2) / (4 * distancia_focal)
            else:
                x_intersecao, y_intersecao = 9, 0

            ponto_final_raio = eixos.coords_to_point(x_intersecao, y_intersecao)
            raio_incidente = Arrow(foco_ponto, ponto_final_raio, buff=0, color=BLUE_B)
            ponto_final_refletido = ponto_final_raio + RIGHT * 4
            raio_refletido = Arrow(ponto_final_raio, ponto_final_refletido, buff=0, color=ORANGE)
            
            grupo_raios.add(raio_incidente)
            grupo_refletidos.add(raio_refletido)

        lista_animacoes_finais = []
        for raio_inc, raio_refl in zip(grupo_raios, grupo_refletidos):
            animacao_do_par = AnimationGroup(
                GrowArrow(raio_inc),
                GrowArrow(raio_refl)
            )
            lista_animacoes_finais.append(animacao_do_par)
        
        self.play(LaggedStart(*lista_animacoes_finais, lag_ratio=0.3, run_time=2))
        self.wait(2)
