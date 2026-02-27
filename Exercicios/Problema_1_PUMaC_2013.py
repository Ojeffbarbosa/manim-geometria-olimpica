"""
APLICAÇÃO TEOREMA DE VIVIANI PROBLEMA PUMaC 2013

Data: 28/11/2025
"""


from manim import *
import numpy as np

class PumacProblem(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        TXT = BLACK
        STROKE = BLACK
        
        #mesmas cores do tikz
        COR_D1 = BLUE_D
        COR_D2 = TEAL_E
        COR_D3 = ORANGE
        COR_Q = RED
        COR_X = BLUE_A
        COR_AUX = GRAY
        
        # enunciado
        enunc = r"""
        \begin{minipage}{12cm}
        \textbf{Problema 1 (PUMaC 2013)}\\[0.2cm]
        Dado um triângulo equilátero ABC e um ponto $P \in \Gamma$ em que $\Gamma$ é a circunferência inscrita no triângulo ABC. Se as duas menores distâncias\ desse ponto às laterais do triângulo são 1 e 4, então o lado desse triângulo equilátero pode ser expresso como $ \frac{a\sqrt{b}}{c}$, em que $mdc(a,c)=1$ e $b$ não é divisível pelo quadrado de nenhum inteiro maior que 1. Determine $a+b+c$.
        \end{minipage}
        """
        txt_enunc = Tex(enunc, color=TXT).scale(0.8)
        self.play(Write(txt_enunc))
        self.wait(5)
        self.play(FadeOut(txt_enunc))

        txt_res = Tex(r"Vamos à resolução", color=TXT, font_size=48)
        self.play(Write(txt_res))
        self.wait(2)
        self.play(FadeOut(txt_res))

        # geometria
        SCALE = 0.43
        r_val = 14/3
        h_val = 3 * r_val
        side = h_val * 2 / np.sqrt(3)
        
        SHIFT = RIGHT * 2.5 + UP * 0.5
        
        # vértices
        A = np.array([-side/2, r_val, 0]) * SCALE + SHIFT
        B = np.array([side/2, r_val, 0]) * SCALE + SHIFT
        C = np.array([0, -2*r_val, 0]) * SCALE + SHIFT
        O = ORIGIN + SHIFT
        
        # ponto P
        P_coords = np.array([-5*np.sqrt(3)/3, 11/3, 0])
        P = P_coords * SCALE + SHIFT
        
        # tangencias
        T1 = np.array([0, r_val, 0]) * SCALE + SHIFT
        T2 = np.array([r_val * np.cos(210*DEGREES), r_val * np.sin(210*DEGREES), 0]) * SCALE + SHIFT
        T3 = np.array([r_val * np.cos(330*DEGREES), r_val * np.sin(330*DEGREES), 0]) * SCALE + SHIFT

        # elementos
        tri = Polygon(A, B, C, color=STROKE)
        lbl_A = MathTex("A", color=TXT).next_to(A, UP, buff=0.1).scale(0.7)
        lbl_B = MathTex("B", color=TXT).next_to(B, UP, buff=0.1).scale(0.7)
        lbl_C = MathTex("C", color=TXT).next_to(C, DOWN, buff=0.1).scale(0.7)

        circ = Circle(radius=r_val*SCALE, color=BLACK, stroke_width=2).move_to(O)
        dot_O = Dot(O, color=TXT).scale(0.5)
        dot_O.set_z_index(20)
        lbl_O = MathTex("O", color=TXT).next_to(dot_O, RIGHT, buff=0.1).scale(0.7)
        dot_P = Dot(P, color=TXT).scale(0.5)
        dot_P.set_z_index(20)
        lbl_P = MathTex("P", color=TXT).next_to(dot_P, DL, buff=0.1).shift(RIGHT*0.2).scale(0.7)

        # linhas dos lados pra usar get_projection
        lado_AB = Line(A, B)
        lado_AC = Line(A, C)
        lado_BC = Line(B, C)

        #projeções usando get_projection nativo do manim, tinha feito manual mas tem essa alternativa mais simples
        H1 = lado_AB.get_projection(P)
        H2 = lado_AC.get_projection(P)
        H3 = lado_BC.get_projection(P)
        
        # segmentos das distancias
        seg_d1 = Line(P, H1, color=COR_D1, stroke_width=3)
        seg_d2 = Line(P, H2, color=COR_D2, stroke_width=3)
        seg_d3 = Line(P, H3, color=COR_D3, stroke_width=3)
        
        ra_d1 = RightAngle(Line(H1, A), Line(H1, P), length=0.15, color=COR_D1)
        ra_d2 = RightAngle(Line(H2, A), Line(H2, P), length=0.15, color=COR_D2)
        ra_d3 = RightAngle(Line(H3, B), Line(H3, P), length=0.15, color=COR_D3)
        
        lbl_d1 = MathTex("d_1", color=COR_D1).next_to(seg_d1, RIGHT, buff=0.05).scale(0.6)
        lbl_d2 = MathTex("d_2", color=COR_D2).next_to(seg_d2, UP, buff=0.05).scale(0.6)
        lbl_d3 = MathTex("d_3", color=COR_D3).scale(0.6).move_to(seg_d3.get_center()).shift(UP*0.3 + RIGHT*0.3)

        # narrativa
        narr = VGroup()
        def fala(txt, fs=32):
            nonlocal narr
            self.play(FadeOut(narr))
            narr = Tex(txt, color=TXT, font_size=fs).to_corner(UL).shift(DOWN*0.2)
            self.play(Write(narr))

        # 1. desenho inicial
        fala("Seja uma circunferência de centro $O$ inscrita num triângulo equilátero $ABC$.")
        self.play(Create(tri), Write(lbl_A), Write(lbl_B), Write(lbl_C), run_time=1.5)
        self.play(Create(circ), FadeIn(dot_O), Write(lbl_O))
        
        fala("Considere um ponto $P$ sobre a circunferência.")
        self.play(FadeIn(dot_P), Write(lbl_P))
        self.wait()

        # 2. distancias
        fala("Sejam $d_1, d_2, d_3$ as distâncias de $P$ aos lados, com $d_1 \\le d_2 \\le d_3$.")
        
        self.play(Create(seg_d1), Write(lbl_d1), Create(ra_d1))
        self.play(Create(seg_d2), Write(lbl_d2), Create(ra_d2))
        self.play(Create(seg_d3), Write(lbl_d3), Create(ra_d3))
        self.wait()
        
        fala("Pelo enunciado, as menores são $1$ e $4$.")
        
        self.play(
            Transform(lbl_d1, MathTex("d_1=1", color=COR_D1).next_to(seg_d1, RIGHT, buff=0.05).scale(0.6)),
            Transform(lbl_d2, MathTex("d_2=4", color=COR_D2).next_to(seg_d2, UP, buff=0.01).scale(0.6))
        )
        self.wait()

        # 3. viviani
        fala(r"\begin{minipage}{8cm}Pelo Teorema de Viviani, a soma das distâncias é a altura $h$ do triângulo equilátero.\end{minipage}", fs=32)
        
        eq_viv1 = MathTex("d_1 + d_2 + d_3 = h", color=TXT).scale(0.7).to_edge(LEFT).shift(UP*2)
        self.play(Write(eq_viv1))
        self.wait()

        fala("Em um triângulo equilátero, $h = 3r$.")
        eq_viv2 = MathTex("h = 3r \\Rightarrow d_1 + d_2 + d_3 = 3r", color=TXT).scale(0.7).next_to(eq_viv1, DOWN, aligned_edge=LEFT)
        self.play(Write(eq_viv2))
        self.wait()
        
        fala("Substituindo $d_1=1$ e $d_2=4$")
        eq_viv3 = MathTex("1 + 4 + d_3 = 3r", color=TXT).scale(0.7).next_to(eq_viv2, DOWN, aligned_edge=LEFT)
        self.play(Write(eq_viv3))
        
        d3_res = MathTex("\\Rightarrow d_3 = 3r - 5", color=TXT).scale(0.7).next_to(eq_viv3, DOWN, aligned_edge=LEFT)
        self.play(Write(d3_res))
        self.wait()
        
        self.play(
            FadeOut(lbl_d1), FadeOut(lbl_d2), FadeOut(lbl_d3),
            FadeOut(eq_viv1), FadeOut(eq_viv2), FadeOut(eq_viv3), FadeOut(d3_res)
        )

        
        fala("Analisando a posição de $P$ com ângulos...")
        
        # reta s
        s_start = np.array([A[0] - 0.5, P[1], 0])
        s_end = np.array([B[0] + 0.5, P[1], 0])
        line_s = DashedLine(s_start, s_end, color=GRAY)
        lbl_s = MathTex("s", color=GRAY).next_to(line_s, RIGHT, buff=0.1).scale(0.8)
        
        self.play(Create(line_s), Write(lbl_s))
        
        # raios
        line_OT1 = Line(O, T1, color=BLACK)
        line_OT2 = Line(O, T2, color=BLACK)
        
        dot_T1 = Dot(T1, color=BLACK).scale(0.8)
        dot_T2 = Dot(T2, color=BLACK).scale(0.8)
        lbl_T1 = MathTex("T_1", color=BLACK).next_to(dot_T1, UP, buff=0.1).scale(0.6)
        lbl_T2 = MathTex("T_2", color=BLACK).next_to(dot_T2, LEFT, buff=0.1).scale(0.6)
        
        ra_T1 = RightAngle(Line(T1, A), Line(T1, O), length=0.15, color=BLACK)
        ra_T2 = RightAngle(Line(T2, C), Line(T2, O), length=0.15, color=BLACK)
        
        fala("Sejam $T_1$ e $T_2$ os pontos de tangência.")
        self.play(Create(line_OT1), FadeIn(dot_T1), Write(lbl_T1), Create(ra_T1))
        self.play(Create(line_OT2), FadeIn(dot_T2), Write(lbl_T2), Create(ra_T2))
        
        line_OP = Line(O, P, color=BLACK)
        self.play(Create(line_OP))
        
        # angulo x
        ang_start = 90 * DEGREES
        v_OP = P - O
        ang_end = np.arctan2(v_OP[1], v_OP[0])
        
        setor_x = Sector(radius=0.6, angle=ang_end - ang_start, start_angle=ang_start, color=BLUE, fill_opacity=0.3, stroke_width=0)
        setor_x.shift(O)
        lbl_x = MathTex("x", color=BLACK).move_to(Angle(line_OT1, line_OP, radius=0.8).point_from_proportion(0.5)).scale(0.6)
        
        self.play(FadeIn(setor_x), Write(lbl_x))
        self.wait()
        
        # projeção Q1 em OT1 usando get_projection
        line_OT1_obj = Line(O, T1)
        Q1 = line_OT1_obj.get_projection(P)
        dot_Q1 = Dot(Q1, color=COR_Q).scale(0.8)
        dot_Q1.set_z_index(20)
        lbl_Q1 = MathTex("Q_1", color=COR_Q).next_to(dot_Q1, RIGHT, buff=0.1).scale(0.6)
        
        ra_Q1 = RightAngle(Line(Q1, P), Line(Q1, O), length=0.15, color=GRAY)
        self.play(FadeIn(dot_Q1), Write(lbl_Q1), Create(ra_Q1))
        
        poly_OQ1P = Polygon(O, Q1, P, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        poly_OQ1P.set_z_index(-1)
        self.play(FadeIn(poly_OQ1P))
        
        fala("No triângulo retângulo $OQ_1P$...")
        
        seg_OQ1 = Line(O, Q1, color=PURPLE)
        txt_rcos = MathTex("r \\cos x", color=PURPLE).scale(0.6).next_to(seg_OQ1, RIGHT, buff=0.1).shift(DOWN*0.1)
        
        self.play(Create(seg_OQ1), Write(txt_rcos))
        
        # d1 em P
        lbl_d1_P = MathTex("d_1", color=COR_D1).scale(0.6).next_to(seg_d1, RIGHT, buff=0.05)
        self.play(Indicate(seg_d1, color=COR_D1), Write(lbl_d1_P))
        self.wait(0.5)
        
        # mover pra Q1T1
        seg_Q1T1 = Line(Q1, T1, color=COR_D1, stroke_width=3)
        seg_d1.set_z_index(10)
        seg_Q1T1.set_z_index(10)
        
        ra_d1_f = RightAngle(Line(T1, A), Line(T1, O), length=0.15, color=COR_D1)
        
        brace_d1 = Brace(seg_Q1T1, RIGHT, buff=0.05, color=COR_D1)
        lbl_d1_f = brace_d1.get_text("$d_1$").scale(0.6).set_color(COR_D1)
        
        self.play(
            Transform(seg_d1, seg_Q1T1),
            Transform(ra_d1, ra_d1_f),
            FadeOut(lbl_d1_P),
            FadeIn(brace_d1), FadeIn(lbl_d1_f)
        )
        
        fala("Logo, $d_1 = r - r\\cos x$.")
        
        eq_d1 = MathTex("d_1 = r(1-\\cos x)", color=TXT).scale(0.65)
        eq_d1.to_edge(LEFT).shift(UP*1.5)
        self.play(Write(eq_d1))
        self.wait()
        
        self.play(
            FadeOut(txt_rcos), FadeOut(seg_OQ1),
            FadeOut(brace_d1), FadeOut(lbl_d1_f), FadeOut(seg_d1),
            FadeOut(ra_d1), FadeOut(poly_OQ1P)
        )
        
        # projeção Q2 em OT2 usando get_projection
        line_OT2_obj = Line(O, T2)
        Q2 = line_OT2_obj.get_projection(P)
        dot_Q2 = Dot(Q2, color=COR_Q).scale(0.8)
        dot_Q2.set_z_index(20)
        lbl_Q2 = MathTex("Q_2", color=COR_Q).next_to(dot_Q2, LEFT, buff=0.05).scale(0.6)
        line_PQ2 = DashedLine(P, Q2, color=GRAY)
        
        ra_Q2 = RightAngle(Line(Q2, P), Line(Q2, O), length=0.15, color=GRAY)
        self.play(Create(line_PQ2), FadeIn(dot_Q2), Write(lbl_Q2), Create(ra_Q2))
        
        poly_OQ2P = Polygon(O, Q2, P, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        poly_OQ2P.set_z_index(-1)
        self.play(FadeIn(poly_OQ2P))
        
        fala("No triângulo retângulo $OQ_2P$...")
        
        seg_OQ2 = Line(O, Q2, color=PURPLE)
        txt_rcos2 = MathTex("r \\cos(120^\\circ - x)", color=PURPLE).scale(0.38).next_to(seg_OQ2, LEFT, buff=0.1).shift(RIGHT*0.99 + DOWN*0.3)
        
        self.play(Create(seg_OQ2), Write(txt_rcos2))
        self.wait(0.5)
        
        # d2 em P
        lbl_d2_P = MathTex("d_2", color=COR_D2).scale(0.6).next_to(seg_d2, UP, buff=0.01)
        self.play(Indicate(seg_d2, color=COR_D2), Write(lbl_d2_P))
        self.wait(0.5)
        
        # mover pra Q2T2
        seg_Q2T2 = Line(Q2, T2, color=COR_D2, stroke_width=3)
        seg_d2.set_z_index(10)
        seg_Q2T2.set_z_index(10)
        
        ra_d2_f = RightAngle(Line(T2, C), Line(T2, O), length=0.15, color=COR_D2)
        lbl_d2_f = MathTex("d_2", color=COR_D2).scale(0.6).next_to(seg_Q2T2, LEFT, buff=0.1).shift(RIGHT*0.5)
        
        self.play(
            Transform(seg_d2, seg_Q2T2),
            Transform(ra_d2, ra_d2_f),
            FadeOut(lbl_d2_P),
            FadeIn(lbl_d2_f)
        )
        
        fala("Temos $d_2 = r - \\overline{OQ_2}$, onde $\\overline{OQ_2} = r\\cos(120^\\circ - x)$.")
        
        eq_d2_int = MathTex("d_2 = r - r\\cos(120^\\circ - x)", color=TXT).scale(0.7)
        eq_d2_int.next_to(eq_d1, DOWN, aligned_edge=LEFT)
        self.play(Write(eq_d2_int))
        self.wait()
        
        eq_d2 = MathTex("d_2 = r(1-\\cos(120^\\circ - x))", color=TXT).scale(0.7)
        eq_d2.next_to(eq_d1, DOWN, aligned_edge=LEFT)
        
        self.play(ReplacementTransform(eq_d2_int, eq_d2))
        self.wait()

        # 5. resolução
        fala("Substituindo $d_1=1$ e $d_2=4$...")
        
        # limpar
        self.play(
            FadeOut(tri), FadeOut(circ), FadeOut(dot_O), FadeOut(lbl_O),
            FadeOut(dot_P), FadeOut(lbl_P), FadeOut(line_OT1), FadeOut(line_OT2),
            FadeOut(line_OP), FadeOut(setor_x), FadeOut(lbl_x),
            FadeOut(dot_T1), FadeOut(lbl_T1), FadeOut(dot_T2), FadeOut(lbl_T2),
            FadeOut(dot_Q1), FadeOut(lbl_Q1), FadeOut(ra_Q1),
            FadeOut(dot_Q2), FadeOut(lbl_Q2), FadeOut(line_PQ2), FadeOut(ra_Q2), FadeOut(seg_d2), FadeOut(lbl_d2_f),
            FadeOut(poly_OQ2P), FadeOut(txt_rcos2), FadeOut(seg_OQ2),
            FadeOut(ra_d2),
            FadeOut(line_s), FadeOut(lbl_s),
            FadeOut(seg_d3), FadeOut(ra_d3), FadeOut(ra_d1), FadeOut(ra_T1), FadeOut(ra_T2),
            FadeOut(lbl_A), FadeOut(lbl_B), FadeOut(lbl_C)
        )
        
        eq_grp = VGroup(eq_d1, eq_d2)
        self.play(eq_grp.animate.arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_corner(UL, buff=2.0))
        self.wait()
        
        # sub d1=1
        eq_d1_sub = MathTex("1 = r(1-\\cos x)", color=TXT).scale(0.8)
        eq_d1_sub.move_to(eq_d1, aligned_edge=LEFT)
        self.play(Transform(eq_d1, eq_d1_sub))
        
        step1 = MathTex("\\Rightarrow \\cos x = 1 - \\frac{1}{r}", color=BLUE).scale(0.8)
        step1.next_to(eq_d1, RIGHT, buff=0.5)
        self.play(Write(step1))
        self.wait()
        
        # sub d2=4
        eq_d2_sub = MathTex("4 = r(1-\\cos(120^\\circ - x))", color=TXT).scale(0.8)
        eq_d2_sub.move_to(eq_d2, aligned_edge=LEFT)
        self.play(Transform(eq_d2, eq_d2_sub))
        self.wait()
        
        # expandindo exp
        fala("Lembrando que $\\cos(a-b) = \\cos a \\cos b + \\operatorname{sen} a \\operatorname{sen} b$...")
        
        cos_id = MathTex(
            "\\cos(120^\\circ - x) = \\cos 120^\\circ \\cos x + \\operatorname{sen} 120^\\circ \\operatorname{sen} x",
            color=BLUE
        ).scale(0.7)
        cos_id.next_to(eq_grp, DOWN, buff=0.8, aligned_edge=LEFT).shift(RIGHT * 0.5)
        self.play(Write(cos_id))
        self.wait()
        
        cos_val = MathTex(
            "= -\\frac{1}{2}\\cos x + \\frac{\\sqrt{3}}{2}\\operatorname{sen} x",
            color=BLUE
        ).scale(0.7).next_to(cos_id, DOWN, aligned_edge=LEFT)
        self.play(Write(cos_val))
        self.wait()

        fala("Substituindo na equação de $d_2$...")
        self.play(FadeOut(cos_id), FadeOut(cos_val))

        step2_exp = MathTex(
            "4 = r\\left[1 - \\left(-\\frac{1}{2}\\cos x + \\frac{\\sqrt{3}}{2}\\operatorname{sen} x\\right)\\right]", 
            color=TXT
        ).scale(0.8)
        step2_exp.next_to(eq_d2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2_exp))
        self.wait()
        
        step2 = MathTex("1 - \\frac{4}{r} = -\\frac{1}{2}\\cos x + \\frac{\\sqrt{3}}{2}\\operatorname{sen} x", color=BLUE).scale(0.8)
        step2.next_to(step2_exp, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        
        fala("Substituindo $\\cos x$ e isolando $\\operatorname{sen} x$...")
        step2c = MathTex("\\Rightarrow \\operatorname{sen} x = \\frac{3r - 9}{\\sqrt{3}r}", color=BLUE).scale(0.8)
        step2c.next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2c))
        self.wait()

        res_grp = VGroup(step1, step2c)
        self.play(
            FadeOut(eq_grp), FadeOut(step2_exp), FadeOut(step2),
            res_grp.animate.arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_corner(UL, buff=2.0)
        )
        
        fala("Usando $\\operatorname{sen}^2 x + \\cos^2 x = 1$...")
        
        step3 = MathTex(
            "\\left(\\frac{3r-9}{\\sqrt{3}r}\\right)^2 + \\left(1-\\frac{1}{r}\\right)^2 = 1",
            color=RED
        ).scale(0.8)
        step3.next_to(step2c, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(step3))
        
        step3b = MathTex("\\Rightarrow 3r^2 - 20r + 28 = 0", color=RED).scale(0.8)
        step3b.next_to(step3, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(step3b))
        
        step4 = MathTex("r = \\frac{14}{3} \\quad \\text{ou} \\quad r = 2", color=RED).scale(0.9)
        step4.next_to(step3b, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(step4))
        self.wait()
        
        self.play(
            FadeOut(step1), FadeOut(step2c), FadeOut(step3), FadeOut(step3b),
            step4.animate.to_corner(UL, buff=2.0)
        )
        
        # verificação
        fala("Verificando as raízes em $d_3 = 3r - 5$...")
        
        check_r2 = MathTex("r=2 \\Rightarrow d_3 = 3(2)-5 = 1", color=GRAY).scale(0.8)
        check_r2.next_to(step4, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(check_r2))
        
        txt_contr = Tex(
            "Contradição! Se $r=2$, as menores distâncias seriam $1$ e $1$,\\\\mas o enunciado afirma que são $1$ e $4$.",
            color=RED
        ).scale(0.7)
        txt_contr.next_to(check_r2, DOWN, aligned_edge=LEFT)
        self.play(Write(txt_contr))
        self.wait()
        
        check_r14 = MathTex("r=\\frac{14}{3} \\Rightarrow d_3 = 3\\left(\\frac{14}{3}\\right)-5 = 9", color=GREEN).scale(0.8)
        check_r14.next_to(txt_contr, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(check_r14))
        
        valid = Tex("Portanto, as três distâncias são 1, 4, 9.", color=GREEN).scale(0.8)
        valid.next_to(check_r14, DOWN, aligned_edge=LEFT)
        self.play(Write(valid))
        self.wait()
        
        self.play(
            FadeOut(step4),
            FadeOut(check_r2), FadeOut(txt_contr), FadeOut(check_r14), FadeOut(valid)
        )
        
        fala("Em um triângulo equilátero de lado $l$ e raio $r$, vale $r = \\frac{l\\sqrt{3}}{6}$")
        self.wait(2)
        
        final_calc = MathTex(
            "l = \\frac{6r}{\\sqrt{3}} = \\frac{6 \\cdot 14/3}{\\sqrt{3}} = \\frac{28}{\\sqrt{3}} = \\frac{28\\sqrt{3}}{3}",
            color=TXT
        ).scale(0.9)
        final_calc.to_edge(LEFT).shift(UP)
        self.play(Write(final_calc))
        
        res_abc = MathTex(
            "l = \\frac{a\\sqrt{b}}{c} \\Rightarrow a=28, b=3, c=3",
            color=RED
        ).scale(0.9)
        res_abc.next_to(final_calc, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(res_abc))
        
        final_sum = MathTex("a+b+c = 34", color=RED).scale(1.2)
        final_sum.next_to(res_abc, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(final_sum))
        self.wait()

        self.play(
            FadeOut(final_calc), 
            FadeOut(res_abc), 
            FadeOut(narr),
            final_sum.animate.set_color(BLACK).move_to(ORIGIN)
        )
        #final
        box = SurroundingRectangle(final_sum, color=BLACK, buff=0.2)
        self.play(Create(box))
        self.wait(3)
