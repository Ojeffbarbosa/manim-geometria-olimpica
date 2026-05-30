"""
TEOREMA DE NAPOLEÃO

O Teorema de Napoleão afirma que:
	Seja $ABC$ um triângulo qualquer. Construam-se externamente sobre os lados $\overline{BC}$, 
    $\overline{CA}$ e $\overline{AB}$ os triângulos equiláteros $\triangle BCA'$, $\triangle CAB'$ e
    $\triangle ABC'$, respectivamente. Sejam $P$, $Q$ e $R$ os centros de $\triangle BCA'$, $\triangle CAB'$ 
    e $\triangle ABC'$, respectivamente. Então o triângulo $PQR$ é equilátero.


Elementos da construção:
- ABC: triângulo original
- A', B', C': vértices externos dos triângulos equiláteros construídos sobre BC, CA e AB
- P, Q, R: centros dos triângulos equiláteros BCA', CAB' e ABC'
- Triângulo PQR: Triângulo de Napoleão

Data: 15/11/2025
"""

from manim import *
import numpy as np


class NapoleonTheorem(Scene):
    def construct(self):
        self.camera.background_color = WHITE  # Fundo branco
        
        # DEFINIÇÃO DAS CORES
        COR_TXT = BLACK
        COR_BORDA = BLACK
        COR_FILL_BASE = GRAY
        
        #cores dos triangulos equiláteros externos
        COR_ABC_EXT = YELLOW  # Triângulo sobre o lado AB (ABC')
        COR_BCA_EXT = BLUE    # Triângulo sobre o lado BC (BCA')
        COR_CAB_EXT = GREEN   # Triângulo sobre o lado CA (CAB')
        
        #cores do triangulo de Napoleão PQR
        COR_BORDA_NAP = BLACK
        COR_FILL_NAP = LIGHT_PINK
        OPAC_NAP = 0.7
        
        titulo = Text("Teorema de Napoleão", font_size=48, color=COR_TXT)
        self.play(Write(titulo))
        self.wait()
        

        titulo_peq = Text("Teorema de Napoleão", font_size=28, color=COR_TXT) #diminui e move pra cima
        titulo_peq.to_edge(UP, buff=0.3)
        self.play(Transform(titulo, titulo_peq))
        self.wait(0.5)
        
        # FUNÇÕES AUXILIARES
        def construir_tri_eq_externo(P1, P2, pt_ref):
            """
            Constrói o terceiro vértice de um triângulo equilátero externo a um lado.
            
            Dados dois pontos P1 e P2 que formam um lado, calcula a 
            posição do terceiro vértice de modo que:
            O triângulo P1-P2-P3 seja equilátero
            P3 esteja do lado oposto ao ponto de referência (construção externa)
            
            Matematica:
                - O vetor do lado é: v = P2 - P1
                - O ponto médio é: M = (P1 + P2) / 2
                - O vetor perpendicular é obtido rotacionando v em 90°
                - A altura do triângulo equilátero é: h = |lado| * √3 / 2
                - P3 = M + perpendicular_normalizado * h
            """
            # Vetor do lado
            v_lado = P2 - P1
            
            # Ponto médio do lado
            pt_med = (P1 + P2) / 2
            
            #vetor perpendicular (rotação de 90 graus no plano XY)
            # Se v = (x, y), então v_perp = (-y, x)
            perp = np.array([-v_lado[1], v_lado[0], 0])
            
            #normaliza o vetor perpendicular
            perp = perp / np.linalg.norm(perp)
            
            #altura do triângulo equilátero
            comp_lado = np.linalg.norm(v_lado)
            alt = comp_lado * np.sqrt(3) / 2
            
            #determina a direção correta (externa ao triângulo original)
            #compara com o vetor do ponto médio até o ponto de referência
            v_para_ref = pt_ref - pt_med
            
            #se o produto escalar é positivo, os vetores apontam para o mesmo lado
            #nesse caso, invertemos a perpendicular para ir para o lado oposto
            if np.dot(perp, v_para_ref) > 0:
                perp = -perp
            
            #terceiro vértice (externo)
            P3 = pt_med + perp * alt
            
            return P3
        

        # Usamos um ValueTracker para controlar a interpolação entre diferentes configurações do triângulo ABC
        
        ctrl = ValueTracker(0)
        
        def get_vert_A():
            t = ctrl.get_value()
            
            if t < 2:
                # Posição inicial e primeira variação
                return np.array([-1.5, -0.8, 0])
            elif t < 3:
                # Interpolação para segunda configuração
                alfa = t - 2  # alfa vai de 0 a 1
                pos_ini = np.array([-1.5, -0.8, 0])
                pos_fim = np.array([-2, -0.5, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
            else:
                # Interpolação para terceira configuração
                alfa = t - 3
                pos_ini = np.array([-2, -0.5, 0])
                pos_fim = np.array([-1, -1.2, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
        
        def get_vert_B(): #crl c + crl v da obter vertice A porem com dados diferentes, daria pra fazer uma funcao so mas para uma abordagem didatica seguimos esse modelo
            t = ctrl.get_value()
            
            if t < 2:
                return np.array([1.5, -0.8, 0])
            elif t < 3:
                alfa = t - 2
                pos_ini = np.array([1.5, -0.8, 0])
                pos_fim = np.array([2, -0.5, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
            else:
                alfa = t - 3
                pos_ini = np.array([2, -0.5, 0])
                pos_fim = np.array([1, -1.2, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
        
        def get_vert_C():
            t = ctrl.get_value()
            
            if t < 1:
                return np.array([0, 1.2, 0])
            elif t < 2:
                alfa = t - 1
                pos_ini = np.array([0, 1.2, 0])
                pos_fim = np.array([1, 1.5, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
            elif t < 3:
                alfa = t - 2
                pos_ini = np.array([1, 1.5, 0])
                pos_fim = np.array([0.3, 0.8, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
            else:
                alfa = t - 3
                pos_ini = np.array([0.3, 0.8, 0])
                pos_fim = np.array([0, 1.5, 0])
                return pos_ini + (pos_fim - pos_ini) * alfa
        
        # CENTROS DOS TRIÂNGULOS EQUILÁTEROS P, Q, R formam o Triângulo de Napoleão
        
        def get_centro(v1, v2, v_oposto):
            v_ext = construir_tri_eq_externo(v1, v2, v_oposto)
            tri_temp = Polygon(v1, v2, v_ext)
            return tri_temp.get_center_of_mass()
        
        # Funções específicas para cada centro
        def get_P():  # Centro oposto ao vértice A visual (sobre a aresta A-B interna do código que liga VisB a VisC)
            return get_centro(get_vert_A(), get_vert_B(), get_vert_C())
        
        def get_Q():  # Centro oposto ao vértice B visual (sobre a aresta B-C interna do código que liga VisC a VisA)
            return get_centro(get_vert_B(), get_vert_C(), get_vert_A())
        
        def get_R():  # Centro oposto ao vértice C visual (sobre a aresta C-A interna do código que liga VisA a VisB)
            return get_centro(get_vert_C(), get_vert_A(), get_vert_B())
        
        # CRIAÇÃO DOS ELEMENTOS VISUAIS COM UPDATERS

        
        # Triângulo ABC original
        tri_ABC = always_redraw(lambda: Polygon(
            get_vert_A(), 
            get_vert_B(), 
            get_vert_C(),
            color=COR_BORDA,
            fill_color=COR_FILL_BASE,
            fill_opacity=0.4,
            stroke_width=4
        ))
        
        # Triângulo equilátero ABC' (sobre o lado AB - amarelo)
        tri_ABC_ext = always_redraw(lambda: Polygon(
            get_vert_A(), 
            get_vert_B(),
            construir_tri_eq_externo(get_vert_A(), get_vert_B(), get_vert_C()),
            color=COR_BORDA,
            fill_color=COR_ABC_EXT,
            fill_opacity=0.25,
            stroke_width=3
        ))
        
        # Triângulo equilátero BCA' (sobre o lado BC - azul)
        tri_BCA_ext = always_redraw(lambda: Polygon(
            get_vert_B(), 
            get_vert_C(),
            construir_tri_eq_externo(get_vert_B(), get_vert_C(), get_vert_A()),
            color=COR_BORDA,
            fill_color=COR_BCA_EXT,
            fill_opacity=0.25,
            stroke_width=3
        ))
        
        # Triângulo equilátero CAB' (sobre o lado CA - verde)
        tri_CAB_ext = always_redraw(lambda: Polygon(
            get_vert_C(), 
            get_vert_A(),
            construir_tri_eq_externo(get_vert_C(), get_vert_A(), get_vert_B()),
            color=COR_BORDA,
            fill_color=COR_CAB_EXT,
            fill_opacity=0.25,
            stroke_width=3
        ))
        

        # PONTOS DOS VÉRTICES E CENTROS

        
        # Pontos nos vértices do triângulo original
        pt_B = always_redraw(lambda: Dot(get_vert_A(), color=COR_TXT, radius=0.06))
        pt_C = always_redraw(lambda: Dot(get_vert_B(), color=COR_TXT, radius=0.06))
        pt_A = always_redraw(lambda: Dot(get_vert_C(), color=COR_TXT, radius=0.06))
        
        # Pontos nos centros dos triângulos equiláteros 
        pt_P = always_redraw(lambda: Dot(get_P(), color=COR_TXT, radius=0.08))
        pt_Q = always_redraw(lambda: Dot(get_Q(), color=COR_TXT, radius=0.08))
        pt_R = always_redraw(lambda: Dot(get_R(), color=COR_TXT, radius=0.08))
        
        # TRIÂNGULO DE NAPOLEÃO 
        tri_nap = always_redraw(lambda: Polygon(
            get_P(), 
            get_Q(), 
            get_R(),
            color=COR_BORDA_NAP,
            fill_color=COR_FILL_NAP,
            fill_opacity=OPAC_NAP,
            stroke_width=4
        ))
        
        # FUNÇÃO PARA MOSTRAR ÂNGULOS DINAMICAMENTE
        
        def criar_grupo_ang(centro, p1, p2, raio=0.3, **kwargs):
            # Calcula os vetores dos lados do ângulo
            v1 = p1 - centro
            v2 = p2 - centro
            
            # Calcula comprimentos dos vetores
            n1 = np.linalg.norm(v1)
            n2 = np.linalg.norm(v2)
            
            # Calcula o ângulo usando o produto escalar
            # cos(θ) = (v1 · v2) / (|v1| * |v2|)
            if n1 == 0 or n2 == 0:
                ang_graus = 0
            else:
                coss = np.dot(v1, v2) / (n1 * n2)
                # Limita o cosseno ao intervalo -1, 1 para evitar erros
                coss = np.clip(coss, -1.0, 1.0)
                ang_graus = np.degrees(np.arccos(coss))
            
            # Texto do ângulo (arredondado para inteiro)
            txt_ang = f"{int(round(ang_graus))}^\\circ"
            
            # arco visual do ang
            arco = Angle(
                Line(centro, p1),
                Line(centro, p2),
                radius=raio,
                color=COR_BORDA,
                **kwargs
            )
            
            # Posiciona o rótulo do  angulo
            pt_med_arco = arco.point_from_proportion(0.5)
            v_rot = pt_med_arco - centro
            norma = np.linalg.norm(v_rot)
            
            if norma == 0:
                pos_rot = pt_med_arco
            else:
                pos_rot = centro + (v_rot / norma) * (raio + 0.2)
            
            rot = MathTex(txt_ang, font_size=20, color=COR_TXT).move_to(pos_rot)
            
            return VGroup(arco, rot)
        
        # Ângulos do Triângulo de Napoleão
        ang_P = always_redraw(lambda: criar_grupo_ang(
            get_P(), get_R(), get_Q(), other_angle=True
        ))
        
        ang_Q = always_redraw(lambda: criar_grupo_ang(
            get_Q(), get_P(), get_R(), other_angle=True
        ))
        
        ang_R = always_redraw(lambda: criar_grupo_ang(
            get_R(), get_Q(), get_P(), other_angle=True
        ))
        
        # Rótulos dos vértices do triângulo original
        rot_B = always_redraw(lambda: MathTex(
            "B", font_size=36, color=COR_TXT
        ).next_to(get_vert_A(), DOWN, buff=0.2))
        
        rot_C = always_redraw(lambda: MathTex(
            "C", font_size=36, color=COR_TXT
        ).next_to(get_vert_B(), DOWN, buff=0.2))
        
        rot_A = always_redraw(lambda: MathTex(
            "A", font_size=36, color=COR_TXT
        ).next_to(get_vert_C(), UP, buff=0.2))
        
        # Rótulos dos centros (vértices do Triângulo de Napoleão)
        rot_P = always_redraw(lambda: MathTex(
            "P", font_size=30, color=COR_TXT
        ).next_to(get_P(), DOWN, buff=0.15))
        
        rot_Q = always_redraw(lambda: MathTex(
            "Q", font_size=30, color=COR_TXT
        ).next_to(get_Q(), RIGHT, buff=0.15))
        
        rot_R = always_redraw(lambda: MathTex(
            "R", font_size=30, color=COR_TXT
        ).next_to(get_R(), LEFT, buff=0.15))
        
  
        # --- ETAPA 1: CONSTRUIR O TRIÂNGULO ORIGINAL ABC 
        self.play(Create(tri_ABC))
        self.play(FadeIn(pt_B), FadeIn(pt_C), FadeIn(pt_A))
        self.add(rot_B, rot_C, rot_A)
        self.play(Write(rot_B), Write(rot_C), Write(rot_A))
        self.wait()
        
        # --- ETAPA 2: CONSTRUIR OS TRIÂNGULOS EQUILÁTEROS EXTERNOS 
        self.play(Create(tri_ABC_ext))
        self.wait(0.3)
        self.play(Create(tri_BCA_ext))
        self.wait(0.3)
        self.play(Create(tri_CAB_ext))
        self.wait()
        
        # --- ETAPA 3: MOSTRAR OS CENTROS P, Q, R 
        self.play(FadeIn(pt_P), FadeIn(pt_Q), FadeIn(pt_R))
        self.add(rot_P, rot_Q, rot_R)
        self.play(Write(rot_P), Write(rot_Q), Write(rot_R))
        self.wait()
        
        # --- ETAPA 4: CONSTRUIR O TRIÂNGULO DE NAPOLEÃO 
        self.play(Create(tri_nap))
        self.wait()
        
        # --- ETAPA 5: MOSTRAR OS ÂNGULOS (TODOS 60°) 
        self.add(ang_P, ang_Q, ang_R)
        self.play(FadeIn(ang_P), FadeIn(ang_Q), FadeIn(ang_R))
        
        # --- ETAPA 6: VARIAR O TRIÂNGULO ORIGINAL 

        
        # 1 variação
        self.play(ctrl.animate.set_value(2), run_time=4, rate_func=smooth)
        self.wait()
        
        # 2variação
        self.play(ctrl.animate.set_value(3), run_time=2, rate_func=smooth)
        self.wait()
        
        # 3 variação
        self.play(ctrl.animate.set_value(4), run_time=2, rate_func=smooth)
        self.wait()
        

        #pisca o Triângulo de Napoleão para enfatizar que ele sempre permanece equilátero
        self.play(tri_nap.animate.set_stroke(width=6, color=COR_BORDA), run_time=0.5)
        self.play(tri_nap.animate.set_stroke(width=4, color=COR_BORDA_NAP), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(*self.mobjects))
        self.wait()
