import math
import matplotlib.pyplot as plt
import numpy as np
from shiny import App, ui, render, reactive

app_ui = ui.page_fluid(
    ui.h2("🧮 Calculadora"),

    ui.input_action_button("alternar_tema", "🌙 Alternar Tema", class_="mb-3"),

    ui.input_select(
        "operacao", 
        "Operação",
        choices={
            "soma": "Adição (+)",
            "subtracao": "Subtração (-)",
            "multiplicacao": "Multiplicação (×)",
            "divisao": "Divisão (÷)",
            "raiz": "Raiz Quadrada (√)",
            "equacao": "Equação de 2º Grau (ax² + bx + c = 0)",
            "funcao": "Função F(x) = ax² + bx + c"
        }
    ),

    ui.output_ui("inputs_dinamicos"),
    
    # Resultado calculado vai logo após os inputs, exceto no gráfico
    ui.output_ui("resultado_local"),

    # Gráfico só aparece se for função F(x)
    ui.output_plot("grafico_fx"),

    # Tema escuro
    ui.output_ui("estilo_tema")
)


def server(input, output, session):
    tema_escuro = reactive.Value(False)

    @reactive.effect
    @reactive.event(input.alternar_tema)
    def _():
        tema_escuro.set(not tema_escuro())

    @output
    @render.ui
    def estilo_tema():
        if tema_escuro():
            return ui.tags.style("""
                body {
                    background-color: #121212;
                    color: #ffffff;
                }
                .form-control, .form-select, .btn {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border-color: #444;
                }
                pre {
                    background-color: #1e1e1e !important;
                    color: #ffffff !important;
                    border: 1px solid #444;
                    padding: 10px;
                    border-radius: 6px;
                }
            """)
        else:
            return ui.tags.style("""
                body {
                    background-color: #ffffff;
                    color: #000000;
                }
                pre {
                    background-color: #f8f9fa;
                    color: #000000;
                    border: 1px solid #ccc;
                    padding: 10px;
                    border-radius: 6px;
                }
            """)

    @output
    @render.ui
    def inputs_dinamicos():
        op = input.operacao()
        if op == "raiz":
            return ui.input_numeric("num1", "Número", value=0)
        elif op in ["equacao", "funcao"]:
            return ui.div(
                ui.input_numeric("a", "Coeficiente A", value=1),
                ui.input_numeric("b", "Coeficiente B", value=0),
                ui.input_numeric("c", "Coeficiente C", value=0)
            )
        else:
            return ui.div(
                ui.input_numeric("num1", "Número 1", value=0),
                ui.input_numeric("num2", "Número 2", value=0)
            )

    @output
    @render.plot
    def grafico_fx():
        if input.operacao() != "funcao":
            return None
        a = input.a()
        b = input.b()
        c = input.c()
        x = np.linspace(-10, 10, 400)
        y = a * x**2 + b * x + c

        fig, ax = plt.subplots()
        ax.plot(x, y, label=f"f(x) = {a}x² + {b}x + {c}", color="tab:blue")
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        ax.set_title("Gráfico da função f(x)")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        return fig
    
    @output
    @render.ui
    def resultado_local():
        if input.operacao() == "funcao":
        # Para a função F(x), resultado vai acima do gráfico
            return ui.div(
            ui.output_text_verbatim("resultado", placeholder=True),
            class_="mt-3"
        )
        else:
            return ui.div(
            ui.output_text_verbatim("resultado", placeholder=True),
            class_="mt-3"
        )


    @output
    @render.text
    def resultado():
        op = input.operacao()
        try:
            if op == "soma":
                return f"{input.num1()} + {input.num2()} = {input.num1() + input.num2()}"
            elif op == "subtracao":
                return f"{input.num1()} - {input.num2()} = {input.num1() - input.num2()}"
            elif op == "multiplicacao":
                return f"{input.num1()} × {input.num2()} = {input.num1() * input.num2()}"
            elif op == "divisao":
                if input.num2() == 0:
                    return "Erro: divisão por zero!"
                return f"{input.num1()} ÷ {input.num2()} = {input.num1() / input.num2()}"
            elif op == "raiz":
                n = input.num1()
                if n < 0:
                    return "Erro: número negativo não tem raiz real."
                return f"√{n} = {math.sqrt(n)}"
            elif op == "equacao":
                a = input.a()
                b = input.b()
                c = input.c()

                if a == 0:
                    return "Erro: isso não é uma equação de 2º grau (a = 0)."

                delta = b**2 - 4*a*c

                if delta < 0:
                    return f"Δ = {delta}\nSem raízes reais."
                elif delta == 0:
                    x = -b / (2*a)
                    return f"Δ = {delta}\nRaiz única: x = {x}"
                else:
                    x1 = (-b + math.sqrt(delta)) / (2*a)
                    x2 = (-b - math.sqrt(delta)) / (2*a)
                    return f"Δ = {delta}\nDuas raízes reais:\nx₁ = {x1}\nx₂ = {x2}"
            elif op == "funcao":
                a = input.a()
                b = input.b()
                c = input.c()
                return f"f(x) = {a}x² + {b}x + {c}\n(O gráfico está acima)"
            else:
                return "Operação inválida."
        except Exception as e:
            return f"Erro: {e}"
        

app = App(app_ui, server)
