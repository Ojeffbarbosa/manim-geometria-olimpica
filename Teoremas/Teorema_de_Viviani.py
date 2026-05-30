"""
TEOREMA DE VIVIANI

O Teorema de Viviani afirma que:
Para qualquer ponto P no interior de um triângulo equilátero, a soma das 
distâncias perpendiculares desse ponto até os três lados é igual à altura 
do triângulo

em outras palavras: PX + PY + PZ = h

Onde:
- P é um ponto qualquer dentro do triângulo equilátero ABC
- PX, PY, PZ são as distâncias perpendiculares de P até os lados BC, AC e AB
- h é a altura do triângulo equilátero

Esta animação demonstra visualmente este teorema, mostrando que independente
de onde P esteja localizado dentro do triângulo, a soma das três alturas
permanece constante e igual à altura total do triângulo.

v2 usando funcoes nativas do manim (get_projection, RightAngle, normalize)

Data: 11/11/2025
"""

from manim import *
import numpy as np


class VivianiTheorem(Scene):
    
    def construct(self):
        self.camera.background_color = WHITE #fundo branco
        


        # DEFINIÇÃO DAS CORES
        #cada perpendicular tem uma cor distinta para facilitar a visualização
        
        COR_PZ = GREEN          # Perpendicular ao lado AB (verde)
        COR_PX = YELLOW         # Perpendicular ao lado BC (amarelo)
        COR_PY = BLUE           # Perpendicular ao lado AC (azul)
        COR_ALTURA = GREY_B     
        
        ESPESSURA_ALTURA = 8    
        ESPESSURA_BARRA = 12    # Espessura das barras do gráfico


        #PAR6AMETROS DO TRIANGULO EQUILATERO
        lado = 4.5 
        
        #altura total do triangulo equilatero
        altura_total = lado * np.sqrt(3) / 2
        
        #DEFINICAO DOS VERTICES DO TRIANGULO
        
        vert_A = UP * altura_total / 2                      # Vértice superior
        vert_B = DOWN * altura_total / 2 + LEFT * lado / 2   # Vértice inferior esquerdo
        vert_C = DOWN * altura_total / 2 + RIGHT * lado / 2  # Vértice inferior direito
        
        #CRIAÇÃO DO POLIGONO TRIANGULO
        triangulo = Polygon(
            vert_A,
            vert_B,
            vert_C,
            color=BLACK,           # Cor da borda
            stroke_width=4,        # Espessura da borda
            fill_color=GRAY,       # Cor de preenchimento
            fill_opacity=0.4,      # Transparência do preenchimento
        ).shift(LEFT * 2.9)  # Desloca o triângulo para a esquerda
        
        triangulo.set_z_index(1)  # elementos com maior z_index aparecem na frente
        
        # Atualiza as coordenadas dos vértices após o deslocamento
        vert_A, vert_B, vert_C = triangulo.get_vertices()[[0, 1, 2]]
        centro = triangulo.get_center_of_mass()
        
        #CRIAÇÃO DOS PONTOS NOS VERTICES
        pts_vertices = VGroup(
            *[Dot(ponto, color=BLACK, radius=0.06) for ponto in (vert_A, vert_B, vert_C)]
        )
        # Define a ordem de renderização para cada ponto
        pts_vertices[0].set_z_index(5)  # Vértice A aparece acima dos outros
        pts_vertices[1].set_z_index(3)
        pts_vertices[2].set_z_index(3)
        
        #RÓTULOS DOS VÉRTICES (A, B, C)
        rotulos = VGroup(
            MathTex("A", color=BLACK).next_to(vert_A, UP, buff=0.1),
            MathTex("B", color=BLACK).next_to(vert_B, DOWN, buff=0.1),
            MathTex("C", color=BLACK).next_to(vert_C, DOWN, buff=0.1),
        )
        
        #LINHAS DE REFERENCIA HORIZONTAIS (TRACEJADAS)
        
        ext_esq = lado * 0.7 #extensão horizontal esq
        ext_dir = lado * 1.4 
        
        # Linha de referência passando pelo vértice A
        ref_topo = DashedLine(
            vert_A + LEFT * ext_esq,
            vert_A + RIGHT * ext_dir,
            color=GREY_B,
            stroke_width=2
        ).set_z_index(-1)  # Aparece atrás do triângulo
        
        # Linha de referência passando pela base (ponto médio de BC)
        pt_medio_base = (vert_B + vert_C) / 2
        ref_base = DashedLine(
            pt_medio_base + LEFT * ext_esq,
            pt_medio_base + RIGHT * ext_dir,
            color=GREY_B,
            stroke_width=2
        ).set_z_index(-1)
        
        #PONTO P - O PONTO INTERNO DO TEOREMA
        
        ponto_P = Dot(centro, color=BLACK, radius=0.07, z_index=3)
        
        
        rot_P = MathTex("P", color=BLACK).scale(0.8).next_to(ponto_P, UP, buff=0.1)
        rot_P.add_updater(lambda m: m.next_to(ponto_P, UP, buff=0.1)) #acompanha o movimento do ponto
        

        #Precisamos desses objetos para calcular as perpendiculares
        lado_AB = Line(vert_A, vert_B)  #lado esquerdo
        lado_BC = Line(vert_B, vert_C)  #base
        lado_AC = Line(vert_A, vert_C)  #lado direito
        

        #FUNCOES PRA OBTER PÉS DAS PERPENDICULARES
        #usando get_projection do manim ao inves de calcular na mao
        
        get_X = lambda: lado_BC.get_projection(ponto_P.get_center())
        get_Y = lambda: lado_AC.get_projection(ponto_P.get_center())
        get_Z = lambda: lado_AB.get_projection(ponto_P.get_center())

        #Estas são as linhas que representam PX, PY e PZ
        #Linha PX: perpendicular de P até o lado BC (base)
        linha_PX = Line(
            ponto_P.get_center(),
            get_X(),
            color=COR_PX,
            stroke_width=ESPESSURA_ALTURA
        ).set_z_index(2)
        
        # Linha PY: perpendicular de P até o lado AC (lado direito)
        linha_PY = Line(
            ponto_P.get_center(),
            get_Y(),
            color=COR_PY,
            stroke_width=ESPESSURA_ALTURA
        ).set_z_index(2)
        
        # Linha PZ: perpendicular de P até o lado AB (lado esquerdo)
        linha_PZ = Line(
            ponto_P.get_center(),
            get_Z(),
            color=COR_PZ,
            stroke_width=ESPESSURA_ALTURA
        ).set_z_index(2)
        

        #Criação dos pontos X, Y, Z com seus rótulos
        # X: pé da perpendicular no lado BC
        # Y: pé da perpendicular no lado AC
        # Z: pé da perpendicular no lado AB
        
        def criar_pt_rotulado(fn_pt, txt, dir): #cria um ponto com rótulo que se atualiza automaticamente.
            pt = Dot(fn_pt(), color=BLACK, radius=0.045, z_index=3)
            pt.add_updater(lambda m: m.move_to(fn_pt()))
            
            rot = MathTex(txt, color=BLACK).scale(0.8)
            rot.add_updater(lambda m: m.next_to(pt, dir, buff=0.1))
            
            return pt, rot
        
        ponto_X, rot_X = criar_pt_rotulado(get_X, "X", DOWN)
        ponto_Y, rot_Y = criar_pt_rotulado(get_Y, "Y", RIGHT)
        ponto_Z, rot_Z = criar_pt_rotulado(get_Z, "Z", LEFT)
        
        # Agrupa os pontos e rótulos dos pés das perpendiculares
        grupo_pes = VGroup(ponto_X, ponto_Y, ponto_Z, rot_X, rot_Y, rot_Z)
        

        #criação dos símbolos de ângulo reto
        # agora usando RightAngle do manim ao inves de fazer um quadradinho na mao
        
        def criar_ang_reto(fn_pt, linha): #cria símbolo de ângulo reto que atualiza qnd P se move
            def construtor():
                pe = fn_pt()
                # direçao do lado do triangulo
                dir_lado = normalize(linha.get_end() - linha.get_start())
                l1 = Line(pe, pe + dir_lado * 0.3)
                l2 = Line(pe, ponto_P.get_center())
                
                return RightAngle(l1, l2, length=0.2, color=BLACK, stroke_width=2).set_z_index(1)
            return always_redraw(construtor)
        
        ang_reto_X = criar_ang_reto(get_X, lado_BC)
        ang_reto_Y = criar_ang_reto(get_Y, lado_AC)
        ang_reto_Z = criar_ang_reto(get_Z, lado_AB)
        
        grupo_ang_retos = VGroup(ang_reto_X, ang_reto_Y, ang_reto_Z)
        

        #estas posições são usadas para demonstrar que o teorema vale
        #para qualquer posição de P dentro do triângulo
        
        def pt_baricentrico(pesos): #calcula um ponto usando coordenadas baricêntricas
            wa, wb, wc = pesos
            return wa * vert_A + wb * vert_B + wc * vert_C
        
        #Lista de posições para onde P será movido durante a demonstração
        posicoes = [
            pt_baricentrico((0.45, 0.4, 0.15)),   #Posição próxima ao centro-esquerdo
            vert_B,                                #Vértice B 
            pt_baricentrico((0.2, 0.35, 0.45)),   #Posição próxima ao lado direito
            pt_baricentrico((0.6, 0.15, 0.25)),   #Posição próxima ao vértice A
            pt_baricentrico((0.35, 0.55, 0.1)),   #Posição próxima ao lado esquerdo
            pt_baricentrico((0.18, 0.22, 0.6)),   #Posição próxima ao vértice C
        ]
        
        #INÍCIO DA ANIMAÇÃO
        

        titulo = Tex("Teorema de Viviani", color=BLACK).scale(1.4)
        self.play(Write(titulo))
        self.wait(1)
        self.play(titulo.animate.scale(0.7).to_edge(UP))
        self.wait(0.5)
        
        texto_equilatero = Tex("Seja um triângulo equilátero:", color=BLACK).scale(0.8).next_to(titulo, DOWN, buff=0.5)
        self.play(Write(texto_equilatero))
        self.wait(1.5)
        self.play(FadeOut(texto_equilatero))

        #ONSTRUÇÃO DO TRIÂNGULO 
        self.play(
            Create(triangulo),
            Create(ref_topo),
            Create(ref_base),
            FadeIn(pts_vertices),
            FadeIn(rotulos)
        )
        
        #PONTO P
        self.play(FadeIn(ponto_P), FadeIn(rot_P))
        self.wait(0.5)
        
        #PERPENDICULARES E PONTOS X, Y, Z
        self.play(
            Create(linha_PX),
            Create(linha_PY),
            Create(linha_PZ),
            FadeIn(grupo_pes)
        )
        self.play(FadeIn(grupo_ang_retos))
        self.wait(1)
        
        #ADIÇÃO DE UPDATERS ÀS PERPENDICULARES
        
        linha_PX.add_updater(
            lambda m: m.become(
                Line(
                    ponto_P.get_center(),
                    get_X(),
                    color=COR_PX,
                    stroke_width=ESPESSURA_ALTURA,
                ).set_z_index(2)
            )
        )
        
        linha_PY.add_updater(
            lambda m: m.become(
                Line(
                    ponto_P.get_center(),
                    get_Y(),
                    color=COR_PY,
                    stroke_width=ESPESSURA_ALTURA,
                ).set_z_index(2)
            )
        )
        
        linha_PZ.add_updater(
            lambda m: m.become(
                Line(
                    ponto_P.get_center(),
                    get_Z(),
                    color=COR_PZ,
                    stroke_width=ESPESSURA_ALTURA,
                ).set_z_index(2)
            )
        )
        
        #Adiciona as linhas a cena para garantir que os updaters funcionem
        self.add(linha_PX, linha_PY, linha_PZ, grupo_ang_retos)
        
        
        #LINHA DA ALTURA DO TRIÂNGULO (h)
        #a altura vai do vértice A até o ponto médio da base BC
        pt_ini_alt = vert_A
        pt_fim_alt = (vert_B + vert_C) / 2
        
        linha_alt = DashedLine(
            pt_ini_alt,
            pt_fim_alt,
            color=COR_ALTURA,
            stroke_width=4
        )
        rot_alt = MathTex("h", color=BLACK).next_to(linha_alt, LEFT, buff=0.2).shift(UP * 0.2)
        
        self.play(Create(linha_alt), Write(rot_alt))
        self.wait(1)
        

        #Criam barras verticais que representam os comprimentos das perpendiculares

        base_barras = RIGHT * 2.3 + DOWN * altura_total / 2
        
        #Barra representando a altura total
        barra_alt = Line(
            base_barras,
            base_barras + UP * altura_total,
            color=COR_ALTURA,
            stroke_width=ESPESSURA_BARRA
        )
        
        #Barras representando as perpendiculares 
        barra_PX = Line(
            base_barras,
            base_barras + UP * linha_PX.get_length(),
            color=COR_PX,
            stroke_width=ESPESSURA_BARRA
        )
        
        barra_PY = Line(
            barra_PX.get_end(),
            barra_PX.get_end() + UP * linha_PY.get_length(),
            color=COR_PY,
            stroke_width=ESPESSURA_BARRA
        )
        
        barra_PZ = Line(
            barra_PY.get_end(),
            barra_PY.get_end() + UP * linha_PZ.get_length(),
            color=COR_PZ,
            stroke_width=ESPESSURA_BARRA
        )
        
        #Anima a cópia da altura para a barra
        self.play(TransformFromCopy(linha_alt, barra_alt))
        
        #Chave e rótulo para a altura total
        chave_alt = Brace(barra_alt, LEFT).set_color(BLACK)
        rot_chave_alt = MathTex("h", color=BLACK).next_to(chave_alt, LEFT)
        
        self.play(GrowFromCenter(chave_alt), Write(rot_chave_alt))
        self.wait(1)
        self.play(FadeOut(chave_alt), FadeOut(rot_chave_alt))
        
        #Anima as cópias das perpendiculares para as barras
        self.play(
            ReplacementTransform(linha_PX.copy(), barra_PX),
            ReplacementTransform(linha_PY.copy(), barra_PY),
            ReplacementTransform(linha_PZ.copy(), barra_PZ),
        )
        
        #Chave e rótulo para a soma das perpendiculares
        grupo_soma = VGroup(barra_PX, barra_PY, barra_PZ)
        chave_soma = Brace(grupo_soma, RIGHT).set_color(BLACK)
        
        #Rótulo colorido: PZ + PX + PY
        rot_soma = MathTex("PZ", "+", "PX", "+", "PY").set_color(BLACK)
        rot_soma[0].set_color(COR_PZ)  # PZ em verde
        rot_soma[2].set_color(COR_PX)  # PX em amarelo
        rot_soma[4].set_color(COR_PY)  # PY em azul
        rot_soma.next_to(chave_soma, RIGHT)
        rot_soma.add_updater(lambda l: l.next_to(chave_soma, RIGHT))
        
        self.play(GrowFromCenter(chave_soma), Write(rot_soma))
        self.wait(1)
        

        #a barras também precisam acompanhar o movimento do ponto P
        
        barra_PX.add_updater(
            lambda m: m.become(
                Line(
                    base_barras,
                    base_barras + UP * linha_PX.get_length(),
                    color=COR_PX,
                    stroke_width=ESPESSURA_BARRA,
                )
            )
        )
        
        barra_PY.add_updater(
            lambda m: m.become(
                Line(
                    barra_PX.get_end(),
                    barra_PX.get_end() + UP * linha_PY.get_length(),
                    color=COR_PY,
                    stroke_width=ESPESSURA_BARRA,
                )
            )
        )
        
        barra_PZ.add_updater(
            lambda m: m.become(
                Line(
                    barra_PY.get_end(),
                    barra_PY.get_end() + UP * linha_PZ.get_length(),
                    color=COR_PZ,
                    stroke_width=ESPESSURA_BARRA,
                )
            )
        )
        
        # updater para a chave acompanhar as barras
        chave_soma.add_updater(
            lambda b: b.become(Brace(VGroup(barra_PX, barra_PY, barra_PZ), RIGHT).set_color(BLACK))
        )
        
        #Adiciona os elementos a cena para garantir funcionamento dos updaters
        self.add(barra_PX, barra_PY, barra_PZ, chave_soma, rot_soma)
        
   # tava muito poluido entao removi os angulos retos
        for ang in grupo_ang_retos:
            ang.clear_updaters()
        self.play(FadeOut(grupo_ang_retos), run_time=0.4)       
        
        # Move P por varias posicoes para demonstrar que a soma é sempre igual a h
        for pos in posicoes:
            self.play(ponto_P.animate.move_to(pos), run_time=1.8)
            self.wait(0.25)
        
        self.wait(2)
        

        #Remove todos os updaters antes de finalizar
        
        objs_updaters = [
            linha_PX,
            linha_PY,
            linha_PZ,
            barra_PX,
            barra_PY,
            barra_PZ,
            chave_soma,
            rot_soma,
            ponto_X,
            ponto_Y,
            ponto_Z,
            rot_X,
            rot_Y,
            rot_Z,
            rot_P,
            ang_reto_X,
            ang_reto_Y,
            ang_reto_Z,
        ]
        
        for obj in objs_updaters:
            obj.clear_updaters()
        
        #esconde todos os elemento
        self.play(FadeOut(*self.mobjects))
        self.wait()
