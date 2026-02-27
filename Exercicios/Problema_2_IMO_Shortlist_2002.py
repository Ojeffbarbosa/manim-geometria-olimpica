"""
APLICAÇÃO PONTO DE FERMAT IMO SHORTLIST 2002

Data: 01/12/2025
"""

from manim import *
import numpy as np

# latex personalizado pra reta <->
tpl = TexTemplate()
tpl.add_to_preamble(r"\newcommand{\reta}[1]{\overleftrightarrow{#1}}")
Tex.set_default(tex_template=tpl)
MathTex.set_default(tex_template=tpl)


def rot(origin, pt, ang_deg): #rotaciona ponto em torno de origem
    ox, oy = origin
    px, py = pt
    rad = np.radians(ang_deg)
    qx = ox + np.cos(rad) * (px - ox) - np.sin(rad) * (py - oy)
    qy = oy + np.sin(rad) * (px - ox) + np.cos(rad) * (py - oy)
    return np.array([qx, qy])


def inter_linhas(p1, p2, p3, p4): #intersecao de duas retas
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return None
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    return np.array([x1 + ua * (x2 - x1), y1 + ua * (y2 - y1)])


def proj_pt(p, a, b): #projecao de p na reta ab 
    ap = p - a
    ab = b - a
    return a + np.dot(ap, ab) / np.dot(ab, ab) * ab


#coordenadas tikz
def get_geo():
    B = np.array([0.0, 0.0])
    C = np.array([7.0, 0.0])
    A = np.array([3.5, 10.5])

    P = rot(A, C, 60)
    Q = rot(A, B, -60)
    F = inter_linhas(B, P, C, Q)
    D = inter_linhas(B, P, A, C)
    E = inter_linhas(C, Q, A, B)
    M = (A + C) / 2
    P1 = proj_pt(F, A, C)
    O_APC = (A + P + C) / 3
    R_APC = np.linalg.norm(A - O_APC)
    O_AQB = (A + Q + B) / 3
    R_AQB = np.linalg.norm(A - O_AQB)
    P2 = 2 * O_APC - P

    return {
        "A": A, "B": B, "C": C, "P": P, "Q": Q, "F": F, "D": D, "E": E,
        "M": M, "P1": P1, "P2": P2, "OAPC": O_APC, "OAQB": O_AQB,
        "R_APC": R_APC, "R_AQB": R_AQB,
    }

#animacao 
class IMO2002Inequality(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.TXT = BLACK
        self.AUX = GRAY_D
        self.MAIN = BLUE_D
        self.HL = RED_B
        self.narr = VGroup()

        self.show_enunc()

        txt_res = Tex(r"Vamos à resolução", color=self.TXT, font_size=48)
        self.play(Write(txt_res))
        self.wait(2)
        self.play(FadeOut(txt_res))

        self.intro_contexto()
        self.prova_lema()
        self.aplica_lema()

    def fala(self, txt, fs=32, shift_v=DOWN * 0.2):
        new = Tex(txt, color=self.TXT, font_size=fs).to_corner(UL).shift(shift_v)
        self.play(FadeOut(self.narr, shift=UP * 0.1, run_time=0.2))
        self.narr = new
        self.play(Write(self.narr), run_time=1.2)

    def show_enunc(self):
        enunc = r"""
        \begin{minipage}{12cm}
        \textbf{Problema 2 (IMO Shortlist 2002).}\\[0.2cm]
        Seja $ABC$ um triângulo para o qual existe um ponto interior $F$ tal que
        $\angle A\hat{F}B = \angle B\hat{F}C = \angle C\hat{F}A$. Sejam as retas $\reta{BF}$ e $\reta{CF}$
        interceptando os lados $\overline{AC}$ e $\overline{AB}$ em $D$ e $E$, respectivamente.
        Prove que
        \[ \overline{AB} + \overline{AC} \ge 4\overline{DE}. \]
        \end{minipage}
        """
        txt = Tex(enunc, color=self.TXT).scale(0.8)
        self.play(Write(txt, run_time=4))
        self.wait(3)
        self.play(FadeOut(txt, shift=UP))

    def intro_contexto(self):
        ctx = Tex(
            r"\begin{minipage}{11cm}"
            r"Perceba que o ponto $F$ é o \textit{ponto de Fermat}, pois a condição "
            r"$\angle A\hat{F}B = \angle B\hat{F}C = \angle C\hat{F}A$ implica que cada um desses "
            r"ângulos mede $120^\circ$, pois sua soma é $360^\circ$. Então podemos usar as "
            r"propriedades desse ponto. Antes de continuar a resolução desse problema, "
            r"vamos provar um lema que precisaremos."
            r"\end{minipage}",
            color=self.TXT,
        ).scale(0.75).to_edge(LEFT)
        self.play(Write(ctx))
        self.wait(4)
        self.play(FadeOut(ctx))

    def prova_lema(self):
        self.fala(r"Provamos o lema auxiliar.")
        self.play(FadeOut(self.narr, run_time=0.2))
        self.narr = VGroup()

        lema = Tex(
            r"\begin{minipage}{10cm}"
            r"\textbf{Lema.}\; Dado um triângulo $DEF$, sejam $P$ e $Q$ pontos sobre as retas "
            r"$\reta{FD}$ e $\reta{FE}$, respectivamente, tais que "
            r"$\overline{PF} \ge \lambda \overline{DF}$ e $\overline{QF} \ge \lambda \overline{EF}$, "
            r"em que $\lambda > 0$. Se $\angle P\hat{F}Q \ge 90^\circ$, então $\overline{PQ} \ge \lambda \overline{DE}$."
            r"\end{minipage}",
            color=self.TXT,
        ).scale(0.7).to_corner(UL)
        self.play(Write(lema))
        self.wait(2)

        #visualizacao
        sc = 0.55
        sh = RIGHT * 3 + DOWN * 0.4
        base_F = np.array([0.0, 0.0, 0.0])
        ang = -8
        base_D = np.array([3.5 * np.cos(np.radians(ang)), 3.5 * np.sin(np.radians(ang)), 0.0])
        base_E = np.array([0.0, 2.8, 0.0])
        base_P = base_F + 1.8 * (base_D - base_F)
        base_Q = base_F + 1.4 * (base_E - base_F)

        def lp(v):
            return v * sc + sh

        F = lp(base_F)
        D = lp(base_D)
        E = lp(base_E)
        P = lp(base_P)
        Q = lp(base_Q)

        dots = {
            "F": Dot(F, color=self.TXT),
            "D": Dot(D, color=self.TXT),
            "E": Dot(E, color=self.TXT),
            "P": Dot(P, color=self.TXT),
            "Q": Dot(Q, color=self.TXT),
        }

        def lbl(mob, t, d, buff=0.15):
            return MathTex(t, color=self.TXT).scale(0.6).next_to(mob, d, buff=buff)

        lbls = VGroup(
            lbl(dots["F"], "F", DOWN),
            lbl(dots["D"], "D", DOWN),
            lbl(dots["E"], "E", LEFT),
            lbl(dots["P"], "P", DOWN),
            lbl(dots["Q"], "Q", LEFT),
        )

        tri_fill = Polygon(D, E, F, color=self.MAIN, stroke_width=2, fill_opacity=0.15)
        lines = VGroup(
            Line(D, F, color=self.MAIN),
            Line(F, E, color=self.MAIN),
            Line(D, E, color=self.MAIN),
            Line(F, P, color=self.AUX),
            Line(F, Q, color=self.AUX),
        )
        line_PQ = Line(P, Q, color=self.HL, stroke_width=4)
        angle = Angle(Line(F, Q), Line(F, P), radius=0.35, other_angle=True, color=self.HL)
        theta_lbl = MathTex(r"\theta", color=self.HL).scale(0.6).next_to(angle, RIGHT, buff=0.2)

        self.fala(r"Visualização do Lema.", shift_v=DOWN * 2.2)
        self.play(Create(tri_fill), Create(lines), FadeIn(VGroup(*dots.values())), Write(lbls), run_time=1.0)
        self.play(Create(line_PQ))
        self.play(Create(angle), Write(theta_lbl))
        self.wait(1)

        self.play(FadeOut(lema))
        
        proof_t = Tex(r"\textbf{Demonstração do Lema:}", color=self.TXT).to_corner(UL).shift(DOWN * 0.2)
        self.play(Write(proof_t))
        
        # lei dos cossenos
        s1 = MathTex(
            r"\overline{PQ}^2 = \overline{PF}^2 + \overline{QF}^2 - 2 \overline{PF} \cdot \overline{QF} \cos \theta",
            color=self.TXT
        ).scale(0.65).to_corner(UL).shift(DOWN * 2.5)
        
        self.fala(r"Pela Lei dos Cossenos no $\triangle PFQ$:", shift_v=DOWN * 0.8)
        tri_pfq = Polygon(dots["P"].get_center(), dots["F"].get_center(), dots["Q"].get_center(), color=self.HL, fill_opacity=0.2, stroke_width=0)
        self.play(Indicate(tri_pfq, color=self.HL))
        self.remove(tri_pfq)
        self.play(Write(s1))
        self.wait(2)

        s2 = MathTex(
            r"\theta \ge 90^\circ \implies \cos \theta \le 0 \implies -\cos \theta \ge 0",
            color=self.TXT
        ).scale(0.65).next_to(s1, DOWN, aligned_edge=LEFT)
        self.fala(r"Como $\theta \ge 90^\circ$, temos $-\cos \theta \ge 0$.", shift_v=DOWN * 0.8)
        self.play(Write(s2))
        self.wait(2)

        s3 = MathTex(
            r"\overline{PF} \ge \lambda \overline{DF}, \quad \overline{QF} \ge \lambda \overline{EF}",
            color=self.TXT
        ).scale(0.65).next_to(s2, DOWN, aligned_edge=LEFT)
        self.fala(r"Substituindo as desigualdades dadas:", shift_v=DOWN * 0.8)
        self.play(Write(s3))
        
        s4 = MathTex(
            r"\overline{PQ}^2 \ge (\lambda \overline{DF})^2 + (\lambda \overline{EF})^2 + 2 (\lambda \overline{DF})(\lambda \overline{EF}) (-\cos \theta)",
            color=self.TXT
        ).scale(0.6).next_to(s3, DOWN, aligned_edge=LEFT)
        self.play(Write(s4))
        self.wait(3)

        s5 = MathTex(
            r"= \lambda^2 (\overline{DF}^2 + \overline{EF}^2 - 2 \overline{DF} \cdot \overline{EF} \cos \theta)",
            color=self.TXT
        ).scale(0.6).next_to(s4, DOWN, aligned_edge=LEFT)
        self.play(Write(s5))
        self.wait(2)

        s6 = MathTex(
            r"= \lambda^2 \overline{DE}^2 \implies \overline{PQ} \ge \lambda \overline{DE}",
            color=self.TXT
        ).scale(0.7).next_to(s5, DOWN, aligned_edge=LEFT)
        self.fala(r"O termo entre parênteses é exatamente $\overline{DE}^2$ (pela Lei dos Cossenos no $\triangle DEF$). Logo:", shift_v=DOWN * 0.8)
        self.play(Indicate(tri_fill, color=self.HL, scale_factor=1.1))
        self.play(Write(s6))
        
        self.play(Indicate(s6, color=self.HL))
        self.wait(3)

        self.play(FadeOut(VGroup(
            tri_fill, lines, line_PQ, angle, theta_lbl, *dots.values(), lbls,
            s1, s2, s3, s4, s5, s6, proof_t
        )))

    def aplica_lema(self): #bug chamada em cima da classe  retornar dps
        geo = get_geo()
        eq_anchor = VectorizedPoint(LEFT * 4.8 + DOWN * 0.5)
        self.add(eq_anchor)
        sc = 0.25
        base_names = ["A", "B", "C", "P", "Q"]
        ctr = np.mean([geo[n] for n in base_names], axis=0)
        sh = RIGHT * 2 + DOWN * 0.2

        def pt(n):
            x, y = geo[n] - ctr
            return np.array([x, y, 0]) * sc + sh

        pts = {n: pt(n) for n in ["A", "B", "C", "D", "E", "F", "P", "Q", "M", "P1", "P2", "OAPC", "OAQB"]}
        r_apc = geo["R_APC"] * sc
        r_aqb = geo["R_AQB"] * sc

        dot_kw = {"color": self.TXT, "radius": 0.06}
        dots = {n: Dot(pts[n], **dot_kw) for n in ["A", "B", "C", "D", "E", "F", "P", "Q"]}
        dots["P1"] = Dot(pts["P1"], color=RED, radius=0.045)
        dots["P2"] = Dot(pts["P2"], color=RED, radius=0.045)
        dots["M"] = Dot(pts["M"], color=self.TXT, radius=0.04)
        dots["O"] = Dot(pts["OAPC"], color=self.TXT, radius=0.04)

        def lbl_pt(n, d):
            return MathTex(n, color=self.TXT).scale(0.55).next_to(dots[n], d, buff=0.08)

        lbl_map = {
            "A": lbl_pt("A", UP), "B": lbl_pt("B", DOWN), "C": lbl_pt("C", DOWN),
            "F": lbl_pt("F", DOWN), "D": lbl_pt("D", UP), "E": lbl_pt("E", LEFT),
            "P": MathTex("P", color=self.TXT).scale(0.55).next_to(dots["P"], RIGHT, buff=0.08),
            "Q": MathTex("Q", color=self.TXT).scale(0.55).next_to(dots["Q"], LEFT, buff=0.08),
            "P_1": MathTex("P_1", color=RED).scale(0.6).next_to(dots["P1"], RIGHT, buff=0.1),
            "P_2": MathTex("P_2", color=RED).scale(0.6).next_to(dots["P2"], LEFT, buff=0.1),
            "M": MathTex("M", color=self.TXT).scale(0.55).next_to(dots["M"], UP, buff=0.1),
            "O": MathTex("O", color=self.TXT).scale(0.55).next_to(dots["O"], UP, buff=0.08),
        }

        circ_apc = Circle(radius=r_apc, color=self.TXT, stroke_width=2).move_to(pts["OAPC"])
        circ_aqb = Circle(radius=r_aqb, color=self.TXT, stroke_width=2).move_to(pts["OAQB"])

        tri_fill = Polygon(pts["A"], pts["B"], pts["C"], fill_color=self.MAIN, fill_opacity=0.15, stroke_width=0)
        l_AB = Line(pts["A"], pts["B"], color=self.TXT)
        l_BC = Line(pts["B"], pts["C"], color=self.TXT)
        l_CA = Line(pts["C"], pts["A"], color=self.TXT)
        l_BF = Line(pts["B"], pts["F"], color=self.AUX)
        l_CF = Line(pts["C"], pts["F"], color=self.AUX)
        l_AF = Line(pts["A"], pts["F"], color=self.AUX)
        l_AP = Line(pts["A"], pts["P"], color=self.TXT)
        l_PC = Line(pts["P"], pts["C"], color=self.TXT)
        l_AQ = Line(pts["A"], pts["Q"], color=self.TXT)
        l_QB = Line(pts["Q"], pts["B"], color=self.TXT)
        l_BP = Line(pts["B"], pts["P"], color=self.TXT)
        l_CQ = Line(pts["C"], pts["Q"], color=self.TXT)
        tri_pca = Polygon(pts["A"], pts["P"], pts["C"], color=self.TXT, stroke_width=2, fill_opacity=0)
        tri_aqb = Polygon(pts["A"], pts["Q"], pts["B"], color=self.TXT, stroke_width=2, fill_opacity=0)

        self.fala(r"Voltando para a prova principal, começamos com o triângulo $ABC$.")
        self.play(Create(l_AB))
        self.play(Create(l_BC))
        self.play(Create(l_CA))
        self.play(FadeIn(tri_fill))
        for n in ["A", "B", "C"]:
            self.play(FadeIn(dots[n]), Write(lbl_map[n]))

        self.fala(r"Marcamos o ponto interior $F$ e ligamos $F$ aos vértices.")
        self.play(FadeIn(dots["F"]), Write(lbl_map["F"]))
        self.play(Create(l_BF), Create(l_CF), Create(l_AF))

        self.fala(r"Sejam $P$ e $Q$ as interseções das retas $\reta{BF}$ e $\reta{CF}$ com os circuncírculos de $CFA$ e $AFB$.")
        
        self.play(Create(circ_apc), Create(circ_aqb), FadeIn(dots["O"]), Write(lbl_map["O"]))
        self.play(Create(l_BP), Create(l_CQ))
        self.play(FadeIn(dots["P"]), Write(lbl_map["P"]), FadeIn(dots["Q"]), Write(lbl_map["Q"]))
        self.play(Create(l_AP), Create(l_PC), Create(l_AQ), Create(l_QB))
        self.wait(1)

        self.fala(r"As interseções determinam $D$ em $\overline{AC}$ e $E$ em $\overline{AB}$.")
        self.play(FadeIn(dots["D"]), Write(lbl_map["D"]))
        self.play(FadeIn(dots["E"]), Write(lbl_map["E"]))

        # ciclico -> P vertice -> equilatero
        quad_afcp = Polygon(pts["A"], pts["F"], pts["C"], pts["P"], color=YELLOW, fill_opacity=0.2, stroke_width=0)
        self.fala(r"Observe que o quadrilátero $AFCP$ é cíclico, pois $P$ está no circuncírculo de $CFA$.")
        self.play(FadeIn(quad_afcp))
        self.wait(1.5)
        self.play(FadeOut(quad_afcp))

        self.fala(r"Sabemos que o circuncírculo de $CFA$ também passa pelo vértice do equilátero construído externamente sobre $\overline{AC}$.")
        self.wait(2)
        
        self.fala(r"Além disso, a reta $\reta{BF}$ passa por esse mesmo vértice (propriedade do Ponto de Fermat).")
        self.play(Indicate(l_BF, color=YELLOW, scale_factor=1.2))
        self.wait(2)

        self.fala(r"Como $P$ é a interseção de $\reta{BF}$ com esse círculo, conclui-se que $P$ é o próprio vértice do triângulo equilátero externo.")
        self.play(Indicate(dots["P"], color=YELLOW, scale_factor=1.5))
        self.wait(1.5)

        self.fala(r"Portanto, $\triangle CPA$ é equilátero.")
        tri_cpa_hl = Polygon(pts["C"], pts["P"], pts["A"], color=ORANGE, fill_opacity=0.2, stroke_width=0)
        self.play(Create(tri_pca), FadeIn(tri_cpa_hl))
        self.play(Indicate(tri_pca, color=self.TXT))
        self.wait(1)
        self.play(FadeOut(tri_cpa_hl))

        self.fala(r"Analogamente, $Q$ é o vértice do equilátero $AQB$.")
        tri_aqb_hl = Polygon(pts["A"], pts["Q"], pts["B"], color=GREEN, fill_opacity=0.2, stroke_width=0)
        self.play(Create(tri_aqb), FadeIn(tri_aqb_hl))
        self.play(Indicate(tri_aqb, color=self.TXT))
        self.wait(1)
        self.play(FadeOut(tri_aqb_hl))

        geo_grp = VGroup(
            tri_fill, l_AB, l_BC, l_CA, l_BF, l_CF,
            l_AP, l_PC, l_AQ, l_QB, l_BP, l_CQ,
            tri_pca, tri_aqb, circ_apc, circ_aqb,
            *dots.values(), *lbl_map.values(),
        )

        self.fala(r"Para aplicar o lema com $\lambda = 4$, precisamos verificar o \^angulo e as desigualdades.")
        self.fala(r"Como $C, F, E$ são colineares, $\angle A\hat{F}E = 180^\circ - \angle A\hat{F}C = 60^\circ$.")

        def get_setor(ctr, s_pt, e_pt, r, cor):
            v_s = s_pt - ctr
            v_e = e_pt - ctr
            s_ang = np.arctan2(v_s[1], v_s[0])
            e_ang = np.arctan2(v_e[1], v_e[0])
            diff = (e_ang - s_ang + np.pi) % (2 * np.pi) - np.pi
            return Sector(radius=r, start_angle=s_ang, angle=diff, arc_center=ctr, color=cor, fill_opacity=0.2, stroke_width=0)

        arc_AFE = Angle(Line(pts["F"], pts["A"]), Line(pts["F"], pts["E"]), radius=0.4, color=RED)
        sect_AFE = get_setor(pts["F"], pts["A"], pts["E"], 0.4, RED)
        ang_AFE = VGroup(arc_AFE, sect_AFE)

        arc_AFD = Angle(Line(pts["F"], pts["D"]), Line(pts["F"], pts["A"]), radius=0.45, color=RED)
        sect_AFD = get_setor(pts["F"], pts["A"], pts["D"], 0.45, RED)
        ang_AFD = VGroup(arc_AFD, sect_AFD)
        
        t_angs = MathTex(r"\angle A\hat{F}E = 180^\circ - \angle A\hat{F}C = 60^\circ", color=RED).scale(0.7).to_edge(LEFT).shift(UP * 1.2)
        t_angs2 = MathTex(r"\text{Analogamente, } \angle A\hat{F}D = 60^\circ", color=self.HL).scale(0.7).next_to(t_angs, DOWN, aligned_edge=LEFT)

        self.play(Create(ang_AFE), Write(t_angs))
        self.play(Create(ang_AFD), Write(t_angs2))
        
        dfe = MathTex(r"\Longrightarrow \angle D\hat{F}E = 60^\circ + 60^\circ = 120^\circ", color=self.HL).scale(0.8).next_to(t_angs2, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(dfe))
        self.wait(2)
        self.play(FadeOut(VGroup(ang_AFE, ang_AFD, t_angs, t_angs2, dfe)))

        # prova PF >= 4 DF
        self.fala(r"Agora provamos $\overline{PF} \ge 4\,\overline{DF}$.")
        self.wait(1)

        l_PM = Line(pts["P"], pts["M"], color=BLACK)
        l_MP2 = Line(pts["M"], pts["P2"], color=BLACK)
        l_P2P = Line(pts["P2"], pts["P"], color=self.AUX)
        l_PO = Line(pts["P"], pts["OAPC"], color=PURPLE)
        l_OM = Line(pts["OAPC"], pts["M"], color=PURPLE)
        l_P2O = Line(pts["P2"], pts["OAPC"], color=PURPLE)
        l_FP1 = Line(pts["F"], pts["P1"], color=ORANGE)

        self.fala(r"Seja $M$ o ponto médio de $\overline{AC}$.")
        self.play(FadeIn(dots["M"]), Write(lbl_map["M"]))
        self.play(Create(l_PM))

        self.fala(r"Seja $P_2$ o ponto diametralmente oposto a $P$ no circuncírculo.")
        self.play(FadeIn(dots["P2"]), Write(lbl_map["P_2"]))
        self.play(Create(l_P2O), Create(l_P2P))

        self.fala(r"Observe que $\overline{PM}$ é a altura do triângulo equilátero (raio + apótema).")
        self.play(Create(l_PO), Create(l_OM))
        
        self.fala(r"E $\overline{MP_2}$ é a flecha do arco (raio - apótema).")
        self.play(Create(l_MP2))

        t_pm = MathTex(r"\overline{PM} = R + \frac{R}{2} = \frac{3R}{2}", color=BLACK).scale(0.65).to_edge(LEFT).shift(UP * 1.2)
        t_mp2 = MathTex(r"\overline{MP_2} = R - \frac{R}{2} = \frac{R}{2}", color=BLACK).scale(0.65).next_to(t_pm, DOWN, aligned_edge=LEFT)
        t_ratio = MathTex(r"\Longrightarrow \overline{PM} = 3\,\overline{MP_2}", color=BLACK).scale(0.7).next_to(t_mp2, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(t_pm))
        self.play(Write(t_mp2))
        self.play(Write(t_ratio))
        self.wait(2)

        self.fala(r"Seja $P_1$ o pé da perpendicular de $F$ em $\overline{AC}$.")
        self.play(FadeIn(dots["P1"]), Write(lbl_map["P_1"]))
        self.play(Create(l_FP1))
        
        self.fala(r"Como $F$ está no arco, sua distância até a corda é máxima em $P_2$, logo $\overline{FP_1} \le \overline{MP_2}$.")
        ineq_fp1 = MathTex(r"\overline{FP_1} \le \overline{MP_2}", color=ORANGE).scale(0.7).next_to(t_ratio, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(ineq_fp1))

        self.fala(r"Como $\overline{PM} \parallel \overline{FP_1}$ e $P,D,F$ são colineares, obtemos $\triangle FP_1D \sim \triangle PMD$.")
        tri_sm = Polygon(pts["F"], pts["P1"], pts["D"], color=ORANGE, fill_opacity=0.15, stroke_width=0)
        tri_lg = Polygon(pts["P"], pts["M"], pts["D"], color=BLACK, fill_opacity=0.15, stroke_width=0)
        sim = MathTex(r"\triangle FP_1D \sim \triangle PMD", color=self.TXT).scale(0.7).next_to(ineq_fp1, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(tri_sm), FadeIn(tri_lg))
        self.play(Indicate(tri_sm, color=ORANGE), Indicate(tri_lg, color=BLACK))
        self.play(Write(sim))

        ratio_pd = MathTex(r"\frac{\overline{PD}}{\overline{DF}} = \frac{\overline{PM}}{\overline{FP_1}} \ge 3", color=self.HL).scale(0.7).next_to(sim, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(ratio_pd))

        self.fala(r"Isso implica $\overline{PD} \ge 3 \overline{DF}$. Somando $\overline{DF}$ em ambos os lados:", shift_v=DOWN * 0.5)

        pf_fin = MathTex(
            r"\implies \overline{PF} = \overline{PD} + \overline{DF} \ge 3\overline{DF} + \overline{DF} = 4\overline{DF}",
            color=self.HL
        ).scale(0.65).next_to(ratio_pd, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(pf_fin))

        self.fala(r"De modo análogo obtemos $\overline{QF} \ge 4\,\overline{EF}$.")
        qf_fin = MathTex(r"\overline{QF} \ge 4\,\overline{EF}", color=self.HL).scale(0.75).next_to(pf_fin, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(qf_fin))
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(t_pm, t_mp2, t_ratio, ineq_fp1, sim, ratio_pd, pf_fin, qf_fin)),
            FadeOut(VGroup(l_PM, l_MP2, l_P2P, l_PO, l_P2O, l_OM, l_FP1, tri_sm, tri_lg)),
        )

        self.fala(r"O lema aplica-se com $\lambda = 4$, logo $\overline{PQ} \ge 4\,\overline{DE}$.")
        l_PQ = Line(pts["P"], pts["Q"], color=self.HL, stroke_width=5)
        l_PQ.set_z_index(10)
        l_DE = Line(pts["D"], pts["E"], color=self.HL, stroke_width=5)
        
        lema_res = MathTex(r"\overline{PQ} \ge 4\,\overline{DE}", color=self.HL).scale(0.8).move_to(LEFT * 4.8 + UP * 2.5)
        
        self.play(Create(l_PQ), l_DE.animate.set_stroke(width=5, color=self.HL))
        self.play(Write(lema_res))
        self.wait(0.5)
        self.play(FadeOut(geo_grp, run_time=0.6))
        self.play(FadeIn(geo_grp, run_time=0.6))

        self.fala(r"Por fim, aplicamos a desigualdade triangular em $APQ$ com $\overline{AP} = \overline{AC}$ e $\overline{AQ} = \overline{AB}$.")
        tri_apq = Polygon(pts["A"], pts["P"], pts["Q"], color=self.AUX, fill_opacity=0.05, stroke_width=2)
        eq_ap = MathTex(r"\overline{AP} = \overline{AC}", color=self.TXT).scale(0.75)
        eq_ap.next_to(lema_res, DOWN, aligned_edge=LEFT, buff=0.4)
        eq_aq = MathTex(r"\overline{AQ} = \overline{AB}", color=self.TXT).scale(0.75).next_to(eq_ap, DOWN, aligned_edge=LEFT, buff=0.3)
        tri_ineq = MathTex(r"\overline{AP} + \overline{AQ} \ge \overline{PQ}", color=self.TXT).scale(0.8).next_to(eq_aq, DOWN, aligned_edge=LEFT, buff=0.3)
        concl = MathTex(r"\overline{AB} + \overline{AC} \ge 4\,\overline{DE}", color=BLACK).scale(1.1).next_to(tri_ineq, DOWN, aligned_edge=LEFT, buff=0.4)

        self.play(Create(tri_apq))
        self.play(Write(eq_ap))
        self.play(Write(eq_aq))
        self.play(Write(tri_ineq))
        self.wait(1)
        
        self.play(ReplacementTransform(VGroup(eq_ap, eq_aq, tri_ineq, lema_res), concl))

        box = SurroundingRectangle(concl, color=BLACK, buff=0.2)
        self.play(Create(box))
        self.wait(3)
        #final
        self.play(FadeOut(VGroup(
            geo_grp, lema_res, tri_apq, eq_ap, eq_aq, tri_ineq,
            l_PQ, l_DE, concl, box, self.narr,
        )))
