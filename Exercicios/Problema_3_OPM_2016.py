"""
APLICAÇÃO TEOREMA DE NAPOLEAO OPM 2016

Data: 08/12/2025
"""

from manim.constants import DOWN
from manim.constants import RIGHT
from manim import *
import numpy as np

#coodenadas exportadas do tikz
def get_pts():
    A = np.array([1.20, 3.00, 0])
    B = np.array([0.00, 0.00, 0])
    C = np.array([4.00, 0.00, 0])
    D = np.array([-2.00, 2.54, 0])
    E = np.array([2.00, -3.46, 0])
    F = np.array([5.20, 3.92, 0])
    G = np.array([-1.20, -3.92, 0])
    H = np.array([-4.00, -0.92, 0])
    
    # Centros aproximados do tikz
    O1 = np.array([2.00, -1.15, 0])
    O2 = np.array([3.47, 2.31, 0])
    O3 = np.array([-0.27, 1.85, 0])
    O2p = np.array([-1.73, -1.62, 0])
    
    pts = {
        "A": A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G, "H": H,
        "O1": O1, "O2": O2, "O3": O3, "O2'": O2p
    }
    
    #centralizar
    all_c = np.array(list(pts.values()))
    ctr = np.mean(all_c, axis=0)
    sc = 0.8
    
    return {k: (v - ctr) * sc for k, v in pts.items()}

class OPMAnimation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.pts = get_pts()
        
        self.COR_ABC = BLACK
        self.COR_EXT = BLACK
        self.COR_NAP = YELLOW
        self.COR_AUX = GRAY
        self.TXT = BLACK
        
        self.narr = VGroup()
        
        self.show_enunc()
        
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(1)
        
        txt_res = Tex(r"Vamos à resolução", color=BLACK, font_size=48)
        self.play(Write(txt_res))
        self.wait(2)
        self.play(FadeOut(txt_res))
        
        self.desenha_fig()
        
        self.prova_cong()
        self.prova_angs()
        self.conclui_nap()

    def fala(self, txt, fs=32, pos=UP*3.5):
        new = Tex(txt, color=self.TXT, font_size=fs).move_to(pos)
        if self.narr:
            self.play(FadeOut(self.narr, run_time=0.5))
        self.narr = new
        self.play(Write(self.narr, run_time=1.5))
        self.wait(1)

    def get_dot(self, n, color=BLACK, r=0.06):
        return Dot(self.pts[n], color=color, radius=r)

    def get_lbl(self, n, d=UP):
        dirs = {
            "A": UP, "B": DL, "C": DR, "D": UP+LEFT, 
            "E": DOWN+RIGHT, "F": UP+RIGHT, "G": DOWN, "H": LEFT,
            "O1": DOWN, "O2": RIGHT, "O3": LEFT, "O2'": LEFT
        }
        use_d = dirs.get(n, d)
        tex_map = {"O1": "O_1", "O2": "O_2", "O3": "O_3", "O2'": "O_2'"}
        tx = tex_map.get(n, n)
        return MathTex(tx, color=self.TXT, font_size=24).next_to(self.pts[n], use_d, buff=0.1)

    def show_enunc(self):
        enunc = (
            r"\begin{minipage}{12cm}"
            r"\textbf{Problema 3 (OPM 2016)}\\"
            r"Considere um triângulo $ABC$ e triângulos equiláteros $ABD$, $BCE$ e $CAF$ construídos externamente. "
            r"Sejam $O_1, O_2, O_3$ os seus centros. Construímos sobre $\overline{BE}$ o triângulo $GEB \cong ABC$ e sobre $\overline{BG}$ "
            r"o equilátero $BGH$ de centro $O_2'$. Prove que:\\"
            r"a) $\triangle O_2 A O_3 \cong \triangle O_2' B O_3$ e $\triangle O_2 C O_1 \cong \triangle O_2' B O_1$\\"
            r"b) $\angle O_2 \hat{O_1} O_2' = \angle O_2 \hat{O_3} O_2' = 120^\circ$\\"
            r"c) $\triangle O_1 O_2 O_3$ é equilátero."
            r"\end{minipage}"
        )
        
        txt = Tex(enunc, color=BLACK, font_size=34).to_edge(UP)
        self.play(Write(txt, run_time=4))
        self.wait(6)
        
    def desenha_fig(self):
        p = self.pts
        
        # tri ABC
        self.fala("Considere um triângulo $ABC$.")
        self.tri_abc = Polygon(p["A"], p["B"], p["C"], color=self.COR_ABC, fill_opacity=0.1)
        lbls_abc = VGroup(self.get_lbl("A"), self.get_lbl("B"), self.get_lbl("C"))
        dots_abc = VGroup(self.get_dot("A"), self.get_dot("B"), self.get_dot("C"))
        
        self.play(Create(self.tri_abc), FadeIn(dots_abc), Write(lbls_abc))
        self.wait(1)
        
        #equilateros externos
        self.fala("Construímos triângulos equiláteros $ABD$, $BCE$ e $CAF$ externamente.")
        self.tri_abd = Polygon(p["A"], p["B"], p["D"], color=self.COR_EXT)
        self.tri_bce = Polygon(p["B"], p["C"], p["E"], color=self.COR_EXT)
        self.tri_caf = Polygon(p["C"], p["A"], p["F"], color=self.COR_EXT)
        
        lbls_def = VGroup(self.get_lbl("D"), self.get_lbl("E"), self.get_lbl("F"))
        dots_def = VGroup(self.get_dot("D"), self.get_dot("E"), self.get_dot("F"))
        
        self.play(
            Create(self.tri_abd), Create(self.tri_bce), Create(self.tri_caf),
            FadeIn(dots_def), Write(lbls_def)
        )
        self.wait(1)
        
        # centros
        self.fala("Sejam $O_1, O_2, O_3$ os seus centros.")
        dot_o1 = self.get_dot("O1", color=BLACK)
        dot_o2 = self.get_dot("O2", color=BLACK)
        dot_o3 = self.get_dot("O3", color=BLACK)
        lbls_o = VGroup(self.get_lbl("O1"), self.get_lbl("O2"), self.get_lbl("O3"))
        
        self.play(FadeIn(dot_o1), FadeIn(dot_o2), FadeIn(dot_o3), Write(lbls_o))
        self.wait(1)
        
        # triangulo napoleao
        self.fala("Destacamos o triângulo $O_1 O_2 O_3$.")
        self.tri_nap = Polygon(p["O1"], p["O2"], p["O3"], color=BLACK, fill_color=YELLOW, fill_opacity=0.4)
        self.play(Create(self.tri_nap))
        self.wait(1)
        
        # construcoes auxiliares GEB e BGH
        self.fala("Construímos sobre $\\overline{BE}$ o triângulo $GEB \\cong ABC$")
        self.tri_geb = Polygon(p["G"], p["E"], p["B"], color=BLACK, fill_opacity=0.1)
        dot_g = self.get_dot("G")
        lbl_g = self.get_lbl("G")
        
        self.play(Create(self.tri_geb), FadeIn(dot_g), Write(lbl_g))
        self.wait(1)
        
        self.fala("e sobre $\\overline{BG}$ o equilátero $BGH$ de centro $O_2'$.")
        self.tri_bgh = Polygon(p["B"], p["G"], p["H"], color=BLACK)
        dot_h = self.get_dot("H")
        lbl_h = self.get_lbl("H")
        dot_o2p = self.get_dot("O2'", color=BLACK)
        lbl_o2p = self.get_lbl("O2'")
        
        self.play(Create(self.tri_bgh), FadeIn(dot_h), Write(lbl_h))
        self.play(FadeIn(dot_o2p), Write(lbl_o2p))
        self.wait(1)

    def prova_cong(self):
        p = self.pts
        
        # a) provar O2 A O3 ~= O2' B O3
        self.fala(r"a) Vamos provar que $\triangle O_2 A O_3 \cong \triangle O_2' B O_3$.")
        
        t1 = Polygon(p["O2"], p["A"], p["O3"], color=BLACK, fill_color=ORANGE, fill_opacity=0.3)
        t2 = Polygon(p["O2'"], p["B"], p["O3"], color=BLACK, fill_color=ORANGE, fill_opacity=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(1)

        # 1. lado O3A = O3B
        self.fala(r"$O_3$ é centro de $\triangle ABD$ equilátero $\Rightarrow \overline{O_3A} = \overline{O_3B}$.")
        s1 = Line(p["O3"], p["A"], color=RED, stroke_width=6)
        s2 = Line(p["O3"], p["B"], color=RED, stroke_width=6)
        self.play(Create(s1), Create(s2))
        self.wait(1)
        self.play(FadeOut(s1), FadeOut(s2))
        
        # 2. lado O2A = O2'B
        self.fala(r"$\triangle GEB \cong \triangle ABC \Rightarrow \overline{BG} = \overline{AC}$.")
        s_bg = Line(p["B"], p["G"], color=RED, stroke_width=6)
        s_ac = Line(p["A"], p["C"], color=RED, stroke_width=6)
        self.play(Create(s_bg), Create(s_ac))
        self.wait(1)
        
        self.fala(r"Como $\triangle BGH$ e $\triangle CAF$ são equiláteros sobre lados iguais, eles são congruentes.")
        self.play(Indicate(self.tri_bgh, color=YELLOW), Indicate(self.tri_caf, color=YELLOW))
        self.wait(1)
        
        self.fala(r"Logo, seus circunraios são iguais: $\overline{O_2A} = \overline{O_2'B}$.")
        self.play(FadeOut(s_bg), FadeOut(s_ac))
        
        s3 = Line(p["O2"], p["A"], color=RED, stroke_width=6)
        s4 = Line(p["O2'"], p["B"], color=RED, stroke_width=6)
        self.play(Create(s3), Create(s4))
        self.wait(1)
        self.play(FadeOut(s3), FadeOut(s4))
        
        # ngulo em A
        self.fala(r"Em $A$: $\overline{O_2 A}$ e $\overline{O_3 A}$ são bissetrizes ($30^\circ$).")
        l_ac = Line(p["A"], p["C"])
        l_ao2 = Line(p["A"], p["O2"])
        l_ab = Line(p["A"], p["B"])
        l_ao3 = Line(p["A"], p["O3"])
        
        a1 = Angle(l_ac, l_ao2, radius=0.4, color=GREEN) 
        a2 = Angle(l_ab, l_ac, radius=0.5, color=BLUE) 
        a3 = Angle(l_ao3, l_ab, radius=0.4, color=GREEN)
        
        lbl_a1 = MathTex("30^\\circ", font_size=20, color=GREEN).next_to(a1, RIGHT, buff=0.05)
        lbl_a2 = MathTex("\\hat{A}", font_size=20, color=BLUE).next_to(a2, DOWN, buff=0.1)
        lbl_a3 = MathTex("30^\\circ", font_size=20, color=GREEN).next_to(a3, LEFT, buff=0.05)
        
        self.play(Create(a1), Create(a3), Write(lbl_a1), Write(lbl_a3))
        self.wait(1)
        self.fala(r"Logo $\angle O_2 \hat{A} O_3 = 30^\circ + \hat{A} + 30^\circ = \hat{A} + 60^\circ$.")
        self.play(Create(a2), Write(lbl_a2))
        self.wait(2)
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(a3), FadeOut(lbl_a1), FadeOut(lbl_a2), FadeOut(lbl_a3))
        
        # angulo em B
        self.fala(r"Em $B$, a soma dós ângulos é $360^\circ$.")
        
        self.fala(r"Temos: $\angle A \hat{B} C = \hat{B}$, $\angle C \hat{B} E = 60^\circ$, $\angle E \hat{B} G = \hat{C}$")
        self.wait(2)
        self.fala(r"$\angle G \hat{B} H = 60^\circ$ e $\angle D \hat{B} A = 60^\circ$.")
        self.wait(2)
        
        self.fala(r"O ângulo restante é $\angle H\hat{B}D = 360^\circ - (180^\circ + \hat{B} + \hat{C})$.")
        self.wait(2)
        
        self.fala(r"Como $\hat{B} + \hat{C} = 180^\circ - \hat{A}$, segue que $\angle H\hat{B}D = \hat{A}$.")
        ang_hbd = Angle(Line(p["B"], p["D"]), Line(p["B"], p["H"]), radius=0.4, color=BLUE)
        lbl_hbd = MathTex(r"\hat{A}", font_size=24, color=BLUE).next_to(ang_hbd, LEFT, buff=0.1)
        self.play(Create(ang_hbd), Write(lbl_hbd))
        self.wait(2)
        
        self.fala(r"Como $\overline{BO_2'}$ e $\overline{BO_3}$ são bissetrizes ($30^\circ$).")
        l_bh = Line(p["B"], p["H"])
        l_bo2p = Line(p["B"], p["O2'"])
        l_bd = Line(p["B"], p["D"])
        l_bo3 = Line(p["B"], p["O3"])
        
        a4 = Angle(l_bh, l_bo2p, radius=0.5, color=GREEN)
        a5 = Angle(l_bo3, l_bd, radius=0.5, color=GREEN)
        lbl_30_1 = MathTex(r"30^\circ", font_size=20, color=GREEN).next_to(a4, LEFT, buff=0.05)
        lbl_30_2 = MathTex(r"30^\circ", font_size=20, color=GREEN).next_to(a5, UP, buff=0.05) #bug corrigir dps
        
        self.play(Create(a4), Create(a5), Write(lbl_30_1), Write(lbl_30_2))
        self.wait(2)
        
        self.fala(r"Logo, $\angle O_2' \hat{B} O_3 = 30^\circ + \hat{A} + 30^\circ = \hat{A} + 60^\circ$.")
        self.wait(2)
        self.play(FadeOut(ang_hbd), FadeOut(lbl_hbd), FadeOut(a4), FadeOut(a5), FadeOut(lbl_30_1), FadeOut(lbl_30_2))
        
        #conclusao LAL
        self.fala(r"Portanto, pelo caso LAL, $\triangle O_2 A O_3 \cong \triangle O_2' B O_3$.")
        self.play(Indicate(t1, color=YELLOW), Indicate(t2, color=YELLOW))
        self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2))
        
        # analogamente
        self.fala(r"Analogamente, $\triangle O_2 C O_1 \cong \triangle O_2' B O_1$.")
        t3 = Polygon(p["O2"], p["C"], p["O1"], color=BLACK, fill_color=PURPLE, fill_opacity=0.3)
        t4 = Polygon(p["O2'"], p["B"], p["O1"], color=BLACK, fill_color=PURPLE, fill_opacity=0.3)
        
        self.play(FadeIn(t3), FadeIn(t4))
        self.wait(2)
        self.play(FadeOut(t3), FadeOut(t4))

    def prova_angs(self):
        p = self.pts
        
        self.fala(r"b) Provar que $\angle O_2 \hat{O_1} O_2' = 120^\circ$ e $\angle O_2 \hat{O_3} O_2' = 120^\circ$.")
        
        # parte 1: O3
        l_o3_o2 = Line(p["O3"], p["O2"], color=BLACK)
        l_o3_o2p = Line(p["O3"], p["O2'"], color=BLACK)
        self.play(Create(l_o3_o2), Create(l_o3_o2p))
        
        self.fala(r"Da congruência $\triangle O_2 A O_3 \cong \triangle O_2' B O_3$, temos $\angle A \hat{O_3} O_2 = \angle B \hat{O_3} O_2'$.")
        self.wait(2)
        
        self.fala(r"Como $O_3$ é centro de $ABD$, $\angle A \hat{O_3} B = 120^\circ$ ($180^\circ - 30^\circ - 30^\circ$).")
        l_o3a = Line(p["O3"], p["A"], color=GRAY, stroke_width=3)
        l_o3b = Line(p["O3"], p["B"], color=GRAY, stroke_width=3)
        self.play(Create(l_o3a), Create(l_o3b))
        
        arc_120 = Angle(l_o3b, l_o3a, radius=0.6, color=BLUE)
        lbl_120 = MathTex(r"120^\circ", color=BLUE, font_size=24).next_to(arc_120, UP, buff=0.1)
        self.play(Create(arc_120), Write(lbl_120))
        self.wait(2)
        self.play(FadeOut(arc_120), FadeOut(lbl_120), FadeOut(l_o3a), FadeOut(l_o3b))
        
        self.fala(r"Vemos que $\angle A \hat{O_3} B = \angle A \hat{O_3} O_2 + \angle O_2 \hat{O_3} B$.")
        self.wait(2)
        
        self.fala(r"E o ângulo desejado é $\angle O_2 \hat{O_3} O_2' = \angle O_2 \hat{O_3} B + \angle B \hat{O_3} O_2'$.")
        self.wait(2)
        
        self.fala(r"Substituindo $\angle B \hat{O_3} O_2'$ por $\angle A \hat{O_3} O_2$, temos o resultado:")
        
        self.fala(r"$\angle O_2 \hat{O_3} O_2' = \angle O_2 \hat{O_3} B + \angle A \hat{O_3} O_2 = 120^\circ$.")
        
        arc_o3 = Angle(l_o3_o2p, l_o3_o2, radius=0.4, color=RED)
        lbl_120_o3 = MathTex(r"120^\circ", color=RED).next_to(arc_o3, RIGHT, buff=0.1)
        self.play(Create(arc_o3), Write(lbl_120_o3))
        self.wait(2)
        self.play(FadeOut(arc_o3), FadeOut(lbl_120_o3))
        
        # O1
        l_o1_o2 = Line(p["O1"], p["O2"], color=BLACK)
        l_o1_o2p = Line(p["O1"], p["O2'"], color=BLACK)
        self.play(Create(l_o1_o2), Create(l_o1_o2p))
        
        self.fala(r"Analogamente para $O_1$. Da congruência $\triangle O_2 C O_1 \cong \triangle O_2' B O_1$")
        self.wait(2)
        
        self.fala(r"temos $\angle C \hat{O_1} O_2 = \angle B \hat{O_1} O_2'$. O ângulo central $\angle C \hat{O_1} B = 120^\circ$.")
        l_o1c = Line(p["O1"], p["C"], color=GRAY, stroke_width=3)
        l_o1b = Line(p["O1"], p["B"], color=GRAY, stroke_width=3)
        self.play(Create(l_o1c), Create(l_o1b))
        
        arc_o1 = Angle(l_o1c, l_o1b, radius=0.6, color=BLUE)
        lbl_o1 = MathTex(r"120^\circ", color=BLUE, font_size=24).next_to(arc_o1, DOWN, buff=0.1)
        self.play(Create(arc_o1), Write(lbl_o1))
        self.wait(2)
        self.play(FadeOut(arc_o1), FadeOut(lbl_o1), FadeOut(l_o1c), FadeOut(l_o1b))
        
        self.fala(r"Decompondo: $\angle C \hat{O_1} B = \angle C \hat{O_1} O_2 + \angle O_2 \hat{O_1} B$.")
        self.wait(2)
        
        self.fala(r"O ângulo alvo é $\angle O_2 \hat{O_1} O_2' = \angle O_2 \hat{O_1} B + \angle B \hat{O_1} O_2'$.")
        self.wait(2)
        
        self.fala(r"Substituindo, concluímos: $\angle O_2 \hat{O_1} O_2' = \angle C \hat{O_1} B = 120^\circ$.")
        
        arc_o1_f = Angle(l_o1_o2, l_o1_o2p, radius=0.4, color=RED)
        lbl_120_o1 = MathTex(r"120^\circ", color=RED).next_to(arc_o1_f, UP, buff=0.1)
        self.play(Create(arc_o1_f), Write(lbl_120_o1))
        self.wait(2)
        self.play(FadeOut(arc_o1_f), FadeOut(lbl_120_o1))

    def conclui_nap(self):
        p = self.pts
        
        self.fala(r"c) Para o item c), usamos os resultados anteriores.")
        
        # quadrilatero
        quad = Polygon(p["O1"], p["O2'"], p["O3"], p["O2"], color=GRAY, fill_opacity=0.1)
        self.play(FadeIn(quad))
        
        self.fala(r"Considere o quadrilátero $O_1 O_2' O_3 O_2$.")
        self.wait(2)
        
        # tri O2 O3 O2'
        t1 = Polygon(p["O2"], p["O3"], p["O2'"], color=BLUE, fill_opacity=0.2)
        self.play(FadeIn(t1))
        
        self.fala(r"$\triangle O_2 O_3 O_2'$ é isósceles ($\overline{O_3 O_2} = \overline{O_3 O_2'}$) com ângulo de $120^\circ$.")
        
        l_o2_o3 = Line(p["O2"], p["O3"])
        l_o2_o2p = Line(p["O2"], p["O2'"])
        
        a_b1 = Angle(l_o2_o3, l_o2_o2p, radius=0.6, color=GREEN)
        lbl_30_1 = MathTex(r"30^\circ", font_size=20, color=GREEN).next_to(a_b1, LEFT, buff=0.1)
        
        self.play(Create(a_b1), Write(lbl_30_1))
        self.wait(2)
        self.play(FadeOut(t1))
        
        # tri O2 O1 O2'
        t2 = Polygon(p["O2"], p["O1"], p["O2'"], color=BLUE, fill_opacity=0.2)
        self.play(FadeIn(t2))
        
        self.fala(r"$\triangle O_2 O_1 O_2'$ também é isósceles com ângulo de $120^\circ$.")
        
        l_o2_o1 = Line(p["O2"], p["O1"])
        
        a_b2 = Angle(l_o2_o2p, l_o2_o1, radius=0.6, color=GREEN)
        lbl_30_2 = MathTex(r"30^\circ", font_size=20, color=GREEN).next_to(a_b2, DOWN, buff=0.1)
        
        self.play(Create(a_b2), Write(lbl_30_2))
        self.wait(2)
        self.play(FadeOut(t2))
        
        # soma em O2
        self.fala(r"Somando os ângulos da base em $O_2$: $30^\circ + 30^\circ = 60^\circ$.")
        
        arc_60 = Angle(l_o2_o3, l_o2_o1, radius=0.8, color=BLACK)
        lbl_60 = MathTex(r"60^\circ", font_size=24, color=BLACK).next_to(arc_60, LEFT, buff=0.2)
        
        self.play(
            ReplacementTransform(VGroup(a_b1, a_b2), arc_60),
            ReplacementTransform(VGroup(lbl_30_1, lbl_30_2), lbl_60)
        )
        self.wait(2)
        
        self.fala(r"Aplicando o raciocínio para $O_1$ e $O_3$, todos os ângulos internos são $60^\circ$.")
        
        l_o1_o2 = Line(p["O1"], p["O2"])
        l_o1_o3 = Line(p["O1"], p["O3"])
        l_o3_o1 = Line(p["O3"], p["O1"])
        l_o3_o2 = Line(p["O3"], p["O2"])
        
        arc_o1_60 = Angle(l_o1_o2, l_o1_o3, radius=0.6, color=BLACK)
        lbl_o1_60 = MathTex(r"60^\circ", font_size=24, color=BLACK).next_to(arc_o1_60, UP, buff=0.1)
        
        arc_o3_60 = Angle(l_o3_o1, l_o3_o2, radius=0.6, color=BLACK)
        lbl_o3_60 = MathTex(r"60^\circ", font_size=24, color=BLACK).next_to(arc_o3_60, RIGHT, buff=0.1)
        
        self.play(
            Create(arc_o1_60), Write(lbl_o1_60),
            Create(arc_o3_60), Write(lbl_o3_60)
        )
        self.wait(3)
        
        #final
        self.play(
            FadeOut(arc_60), FadeOut(lbl_60),
            FadeOut(arc_o1_60), FadeOut(lbl_o1_60),
            FadeOut(arc_o3_60), FadeOut(lbl_o3_60),
            FadeOut(quad), FadeOut(self.narr),
            *[FadeOut(m) for m in self.mobjects]
        )
        self.wait(1)
