"""
PONTO DE FERMAT 

O Ponto de Fermat é o ponto que minimiza a soma das distâncias até os três
vértices de um triângulo

Data: 21/11/2025
"""

from manim import *
import numpy as np


class FermatPoint(Scene):
    def construct(self):
        self.camera.background_color = WHITE  # Fundo branco
        
        #cores
        COR_TXT = BLACK
        COR_BORDA = BLACK
        COR_FILL_BASE = GRAY
        
        #cores dos triângulos equiláteros externos
        COR_ABD = YELLOW  # Triângulo sobre o lado AB
        COR_BCE = BLUE    # Triângulo sobre o lado BC
        COR_CAF = GREEN   # Triângulo sobre o lado CA
        
        #cores do Ponto de Fermat e linhas de conexão
        COR_FERMAT = BLACK
        COR_LINHAS = '#204080'  #azul escuro hexadecimal
        

        titulo = Text("Ponto de Fermat", font_size=48, color=COR_TXT)
        self.play(Write(titulo))
        self.wait()
        
        #reduz o titulo e move para o topo da tela
        titulo_peq = Text("Ponto de Fermat", font_size=28, color=COR_TXT)
        titulo_peq.to_edge(UP, buff=0.3)
        self.play(Transform(titulo, titulo_peq))
        self.wait(0.5)
        
        # FUNÇÕES AUXILIARES 
        def construir_tri_eq_externo(P1, P2, pt_ref): #crl c + crlv do teorema de napoleao
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
        
        def criar_seg_estendido(p1, p2, p3): #ajustes visuais
            pts = [p1, p2, p3]
            dist_max = -1
            melhor_par = (p1, p2)
            
            # Encontra o par de pontos mais distante
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    dist = np.linalg.norm(pts[i] - pts[j])
                    if dist > dist_max:
                        dist_max = dist
                        melhor_par = (pts[i], pts[j])
            
            ini, fim = melhor_par[0], melhor_par[1]
            
            # Se o Ponto de Fermat é um dos extremos, estende um pouco mais
            if np.array_equal(p3, ini) or np.array_equal(p3, fim):
                centro = (ini + fim) / 2
                if np.array_equal(p3, ini):
                    dir = ini - centro
                    ini = ini + dir * 0.2  # Estende 20%
                else:
                    dir = fim - centro
                    fim = fim + dir * 0.2
            
            return Line(ini, fim, color=COR_LINHAS, stroke_width=2)
        
        #ANIMAÇÃO DOS VÉRTICES
        ctrl = ValueTracker(0)
        
        def get_vert_A():
            """
            Retorna a posição do vértice A baseada no estado da animação.
            
            O vértice se move através de posições pré-definidas para demonstrar
            diferentes configurações do triângulo.
            """
            t = ctrl.get_value()
            
            P0 = np.array([-1.5, -0.8, 0])
            P1 = np.array([-1.5, -0.8, 0])
            P2 = np.array([-1.8, -0.6, 0])
            P3 = np.array([-2.0, 0.0, 0])
            P4 = np.array([-2.0, 0.0, 0])
            

            if t < 1: #gambiarra melhor que a funcao feita no teorema de napoleao
                return P0 + (P1 - P0) * t
            elif t < 2:
                return P1 + (P2 - P1) * (t - 1)
            elif t < 3:
                return P2 + (P3 - P2) * (t - 2)
            else:
                return P3 + (P4 - P3) * (t - 3)
        
        def get_vert_B():
            """
            Retorna a posição do vértice B baseada no estado da animação.
            """
            t = ctrl.get_value()
            
            P0 = np.array([1.5, -0.8, 0])
            P1 = np.array([1.5, -0.8, 0])
            P2 = np.array([1.8, -0.6, 0])
            P3 = np.array([2.0, 0.0, 0])
            P4 = np.array([2.0, 0.0, 0])
            
            if t < 1:
                return P0 + (P1 - P0) * t
            elif t < 2:
                return P1 + (P2 - P1) * (t - 1)
            elif t < 3:
                return P2 + (P3 - P2) * (t - 2)
            else:
                return P3 + (P4 - P3) * (t - 3)
        
        def get_vert_C():
            """
            Retorna a posição do vértice C baseada no estado da animação.
            """
            t = ctrl.get_value()
            
            P0 = np.array([0.0, 1.2, 0])       
            P1 = np.array([1.0, 1.5, 0])       
            P2 = np.array([0.5, 1.6, 0])      
            P3 = np.array([0.0, 1.1547, 0])    # angulo C = 120° exatos
            P4 = np.array([0.0, 0.5, 0])       # angulo C > 120° (obtuso)
            
            if t < 1:
                return P0 + (P1 - P0) * t
            elif t < 2:
                return P1 + (P2 - P1) * (t - 1)
            elif t < 3:
                return P2 + (P3 - P2) * (t - 2)
            else:
                return P3 + (P4 - P3) * (t - 3)
        
        # FUNÇÕES PARA CALCULAR OS VÉRTICES EXTERNOS

        
        def get_vert_D():
            """Vértice externo do triângulo equilátero sobre AB"""
            return construir_tri_eq_externo(
                get_vert_A(), get_vert_B(), get_vert_C()
            )
        
        def get_vert_E():
            """Vértice externo do triângulo equilátero sobre BC"""
            return construir_tri_eq_externo(
                get_vert_B(), get_vert_C(), get_vert_A()
            )
        
        def get_vert_F():
            """Vértice externo do triângulo equilátero sobre CA"""
            return construir_tri_eq_externo(
                get_vert_C(), get_vert_A(), get_vert_B()
            )
        

        # CALCULO DO PONTO DE FERMAT 
        def get_fermat():
            """
            Pela construção, as três linhas AD, BE e CF sempre se encontram
            em um único ponto como visto no artigo, que é o ponto de fermat
            """
            # pega os pontos
            p1, p2 = get_vert_A(), get_vert_E()
            p3, p4 = get_vert_C(), get_vert_D()
            
            x1, y1 = p1[0], p1[1]
            x2, y2 = p2[0], p2[1]
            x3, y3 = p3[0], p3[1]
            x4, y4 = p4[0], p4[1]
            
            # Denominador da eq de interseção
            denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            
            if denom == 0:
                # Retas paralelas (não deveria acontecer nesta construção)
                return np.array([0, 0, 0])
            
            # parametro t da primeira reta
            t = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
            
            # Ponto de interseção
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            return np.array([x, y, 0])
        

        # CRIAÇÃO DOS ELEMENTOS VISUAIS
        
        # Triângulo riginal
        tri_ABC = always_redraw(lambda: Polygon(
            get_vert_A(), get_vert_B(), get_vert_C(),
            color=COR_BORDA,
            fill_color=COR_FILL_BASE,
            fill_opacity=0.4,
            stroke_width=4
        ))
        
        # Triângulos equilateros externos
        tri_ABD = always_redraw(lambda: Polygon(
            get_vert_A(), get_vert_B(), get_vert_D(),
            color=COR_BORDA,
            fill_color=COR_ABD,
            fill_opacity=0.25,
            stroke_width=3
        ))
        
        tri_BCE = always_redraw(lambda: Polygon(
            get_vert_B(), get_vert_C(), get_vert_E(),
            color=COR_BORDA,
            fill_color=COR_BCE,
            fill_opacity=0.25,
            stroke_width=3
        ))
        
        tri_CAF = always_redraw(lambda: Polygon(
            get_vert_C(), get_vert_A(), get_vert_F(),
            color=COR_BORDA,
            fill_color=COR_CAF,
            fill_opacity=0.25,
            stroke_width=3
        ))
        
        # Linhas conectando vértices aos vértices opostos dos triângulos externos
        linha_CD = always_redraw(lambda: criar_seg_estendido(
            get_vert_C(), get_vert_D(), get_fermat()
        ))
        
        linha_AE = always_redraw(lambda: criar_seg_estendido(
            get_vert_A(), get_vert_E(), get_fermat()
        ))
        
        linha_BF = always_redraw(lambda: criar_seg_estendido(
            get_vert_B(), get_vert_F(), get_fermat()
        ))
        
        # Ponto de Fermat
        pt_fermat = always_redraw(lambda: Dot(
            get_fermat(), color=COR_FERMAT, radius=0.07
        ))
        
        # VISUALIZAÇÃO DOS ÂNGULOS DE 120°
        
        def get_pos_rot_ang(arco, centro, dist=0.6):
            """
            Calcula a posição do rótulo de um ângulo.
            """
            pt_med = arco.point_from_proportion(0.5)
            v = pt_med - centro
            norma = np.linalg.norm(v)
            if norma == 0:
                return pt_med
            return centro + (v / norma) * dist
        
        def criar_grupo_ang_preenchido(centro, p1, p2, raio, cor):
            # Calcula os vetores dos lados
            v1 = p1 - centro
            v2 = p2 - centro
            n1 = np.linalg.norm(v1)
            n2 = np.linalg.norm(v2)
            
            # Calcula o ângulo usando produto escalar
            if n1 == 0 or n2 == 0:
                ang_graus = 0
            else:
                coss = np.dot(v1, v2) / (n1 * n2)
                coss = np.clip(coss, -1.0, 1.0)
                ang_graus = np.degrees(np.arccos(coss))
            
            txt_ang = f"{int(round(ang_graus))}^\\circ"
            
            # Cria as linhas auxiliares para o objeto Angle
            l1 = Line(centro, p1)
            l2 = Line(centro, p2)
            arco = Angle(l1, l2, radius=raio, color=cor)
            
            # Cria o preenchimento do setor
            preenche = arco.copy()
            preenche.add_line_to(centro)
            preenche.set_fill(cor, opacity=0.2)
            preenche.set_stroke(width=0)
            
            # Rótulo com o valor do ângulo
            rot = MathTex(txt_ang, font_size=16, color=cor).move_to(
                get_pos_rot_ang(arco, centro, dist=raio + 0.2)
            )
            
            return VGroup(preenche, arco, rot)
        
        # Ângulos no Ponto de Fermat todos devem ser ~120° quando válido
        ang_EPF = always_redraw(lambda: criar_grupo_ang_preenchido(
            get_fermat(), get_vert_E(), get_vert_F(), 0.32, ORANGE
        ))
        
        ang_FPD = always_redraw(lambda: criar_grupo_ang_preenchido(
            get_fermat(), get_vert_F(), get_vert_D(), 0.32, BLUE
        ))
        
        ang_DPE = always_redraw(lambda: criar_grupo_ang_preenchido(
            get_fermat(), get_vert_D(), get_vert_E(), 0.32, GREEN
        ))
        
        # RÓTULOS DOS PONTOS

        
        # Rótulos dos vértices do triângulo original
        rot_A = always_redraw(lambda: MathTex(
            "A", font_size=36, color=COR_TXT
        ).next_to(get_vert_A(), DOWN + LEFT, buff=0.1))
        
        rot_B = always_redraw(lambda: MathTex(
            "B", font_size=36, color=COR_TXT
        ).next_to(get_vert_B(), DOWN + RIGHT, buff=0.1))
        
        rot_C = always_redraw(lambda: MathTex(
            "C", font_size=36, color=COR_TXT
        ).next_to(get_vert_C(), UP, buff=0.1))
        
        # Rótulos dos vértices externos
        rot_D = always_redraw(lambda: MathTex(
            "D", font_size=30, color=COR_TXT
        ).next_to(get_vert_D(), DOWN, buff=0.1))
        
        rot_E = always_redraw(lambda: MathTex(
            "E", font_size=30, color=COR_TXT
        ).next_to(get_vert_E(), RIGHT, buff=0.1))
        
        rot_F = always_redraw(lambda: MathTex(
            "F", font_size=30, color=COR_TXT
        ).next_to(get_vert_F(), LEFT, buff=0.1))
        
        # Rótulo do Ponto de Fermat
        rot_fermat = always_redraw(lambda: MathTex(
            "P", font_size=30, color=COR_FERMAT
        ).next_to(get_fermat(), UP + RIGHT, buff=0.25))
        
        # FUNÇÃO PARA CALCULAR O ÂNGULO C DO TRIÂNGULO

        # mostrat o caso  quando ângulo C >= 120°
        
        def calc_ang_C():

            a = get_vert_A()
            b = get_vert_B()
            c = get_vert_C()
            
            # Vetores dos lados que formam o ângulo C
            v_CA = a - c
            v_CB = b - c
            
            n_CA = np.linalg.norm(v_CA)
            n_CB = np.linalg.norm(v_CB)
            
            if n_CA == 0 or n_CB == 0:
                return 0
            
            coss = np.dot(v_CA, v_CB) / (n_CA * n_CB)
            coss = np.clip(coss, -1.0, 1.0)
            
            return np.degrees(np.arccos(coss))
        
        # Texto mostrando o valor do ângulo C
        txt_ang_C = always_redraw(lambda: MathTex(
            f"\\hat{{C}} = {int(round(calc_ang_C()))}^\\circ",
            font_size=36, color=BLACK
        ).to_edge(RIGHT, buff=1))
        

        # SEQUÊNCIA DE ANIMAÇÕES

        
        # --- ETAPA 1: CONSTRUIR O TRIÂNGULO ORIGINAL
        self.play(Create(tri_ABC))
        self.play(FadeIn(rot_A), FadeIn(rot_B), FadeIn(rot_C))
        self.wait()
        
        # --- ETAPA 2: CONSTRUIR OS TRIÂNGULOS EQUILÁTEROS EXTERNOS
        self.play(Create(tri_ABD), FadeIn(rot_D))
        self.wait(0.3)
        self.play(Create(tri_BCE), FadeIn(rot_E))
        self.wait(0.3)
        self.play(Create(tri_CAF), FadeIn(rot_F))
        self.wait()
        
        # --- ETAPA 3: TRAÇAR AS LINHA
        self.play(Create(linha_AE))
        self.play(Create(linha_BF))
        self.play(Create(linha_CD))
        self.wait()
        
        # --- ETAPA 4: MOSTRAR O PONTO DE FERMAT
        self.play(FadeIn(pt_fermat), Write(rot_fermat))
        self.wait()
        
        # --- ETAPA 5: MOSTRAR OS ÂNGULOS DE 120°
        self.play(FadeIn(ang_EPF), FadeIn(ang_FPD), FadeIn(ang_DPE))
        self.wait()
        
        # --- ETAPA 6: VARIAR O TRIÂNGULO (DEMONSTRAÇÃO DINÂMICA)
        self.play(ctrl.animate.set_value(1), run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(ctrl.animate.set_value(2), run_time=2, rate_func=smooth)
        self.wait()
        
        # --- ETAPA 7: TRANSIÇÃO PARA O CASO ESPECIAL
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)
        
        # texto caso especial
        pergunta = Text(
            "E se um dos ângulos internos\nfosse maior ou igual a 120°?",
            font_size=36, color=BLACK
        )
        self.play(Write(pergunta))
        self.wait(3)
        self.play(FadeOut(pergunta))
        self.wait(0.5)
        
        # --- ETAPA 8: REAPARECER A FIGURA
        self.play(
            FadeIn(tri_ABC), FadeIn(rot_A), FadeIn(rot_B), FadeIn(rot_C),
            FadeIn(tri_ABD), FadeIn(rot_D),
            FadeIn(tri_BCE), FadeIn(rot_E),
            FadeIn(tri_CAF), FadeIn(rot_F),
            FadeIn(linha_AE), FadeIn(linha_BF), FadeIn(linha_CD),
            FadeIn(pt_fermat), FadeIn(rot_fermat),
            FadeIn(ang_EPF), FadeIn(ang_FPD), FadeIn(ang_DPE)
        )
        self.wait()
        
        # --- ETAPA 9: MOSTRAR O ÂNGULO C
        def criar_visual_ang_C():
            """Cria a visualização do ângulo C do triângulo."""
            l1 = Line(get_vert_C(), get_vert_A())
            l2 = Line(get_vert_C(), get_vert_B())
            arco = Angle(l1, l2, radius=0.32, color=BLACK, stroke_width=2)
            
            preenche = arco.copy()
            preenche.add_line_to(get_vert_C())
            preenche.set_fill(color=BLACK, opacity=0.1)
            preenche.set_stroke(width=0)
            
            return VGroup(preenche, arco)
        
        ang_C_visual = always_redraw(criar_visual_ang_C)
        ang_C_estatico = criar_visual_ang_C()
        
        self.play(FadeIn(ang_C_estatico), Write(txt_ang_C))
        self.add(ang_C_visual)
        self.remove(ang_C_estatico)
        self.wait()
        
        # --- ETAPA 10: VARIAR PARA ÂNGULO C = 120°
        # Ponto de Fermat coincide com C
        self.play(ctrl.animate.set_value(3), run_time=3, rate_func=smooth)
        self.wait(1)  # Pausa para mostrar que é exatamente 120°
        
        # --- ETAPA 11: VARIAR PARA ÂNGULO C > 120°
        # O Ponto de Fermat agora está no vértice C
        self.play(ctrl.animate.set_value(4), run_time=3, rate_func=smooth)
        self.wait()
        
        # --- LIMPEZA FINAL
        self.play(FadeOut(*self.mobjects))
        self.wait()
