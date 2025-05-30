import math
from shiny import App, ui, render, reactive

# Interface
app_ui = ui.page_fluid(
    ui.h2("🧮 Calculadora"),

    ui.input_numeric("num1", "Número 1", value=0),

    # Campo Número 2 renderizado dinamicamente
    ui.output_ui("numero2_dinamico"),
    
    ui.input_select(
        "operacao", 
        "Operação",
        choices={
            "soma": "Adição (+)",
            "subtracao": "Subtração (-)",
            "multiplicacao": "Multiplicação (×)",
            "divisao": "Divisão (÷)",
            "raiz": "Raiz Quadrada (√)"
        }
    ),
    
    ui.hr(),
    ui.output_text_verbatim("resultado", placeholder=True),
)

# Lógica do servidor
def server(input, output, session):
    # Renderizar dinamicamente o campo Número 2
    @output
    @render.ui
    def numero2_dinamico():
        if input.operacao() == "raiz":
            return None  # Oculta o campo
        else:
            return ui.input_numeric("num2", "Número 2", value=0)

    # Resultado da operação
    @output
    @render.text
    def resultado():
        n1 = input.num1()
        op = input.operacao()

        # Para operações que usam num2, verificar se o campo está presente
        n2 = input.num2() if op != "raiz" else None

        try:
            if op == "soma":
                return f"{n1} + {n2} = {n1 + n2}"
            elif op == "subtracao":
                return f"{n1} - {n2} = {n1 - n2}"
            elif op == "multiplicacao":
                return f"{n1} × {n2} = {n1 * n2}"
            elif op == "divisao":
                if n2 == 0:
                    return "Erro: divisão por zero!"
                return f"{n1} ÷ {n2} = {n1 / n2}"
            elif op == "raiz":
                if n1 < 0:
                    return "Erro: não existe raiz quadrada real de número negativo!"
                return f"√{n1} = {math.sqrt(n1)}"
            else:
                return "Operação inválida."
        except Exception as e:
            return f"Erro: {e}"

# App
app = App(app_ui, server)
