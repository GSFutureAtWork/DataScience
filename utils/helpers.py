import pandas as pd

COLUNAS_ORDENADAS = [
    # Perfil da Vaga (Job Profile)
    "job_title",
    "experience_level",
    "employment_type",
    # Contexto da Empresa (Company Profile)
    "company_location",
    "company_size",
    # Contexto do Empregado (Employee Context)
    "employee_residence",
    "work_models",
    "remote_ratio",
    "work_year",
    # Variável Alvo (Target)
    "salary_in_usd",
]


def format_float(value):
    """Formata números com ponto como separador de milhares e vírgula como decimal"""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_integer(value):
    """Formata inteiros com ponto como separador de milhares"""
    return f"{value:,}".replace(",", ".")


def get_dimensions(df: pd.DataFrame) -> str:
    return f"{format_integer(df.shape[0])} registros, {format_integer(df.shape[1])} colunas"


def generate_unique_values_table(df, max_unique_values=100, show_count=False) -> str:
    colunas_selecionadas = df.select_dtypes(
        include=["object", "bool", "category", "boolean"]
    ).columns

    if colunas_selecionadas.empty:
        return "Nenhuma coluna do tipo object, bool, category ou boolean encontrada."

    data_valores_unicos = []

    for coluna in colunas_selecionadas:
        value_counts = df[coluna].value_counts(dropna=False)

        if len(value_counts) < max_unique_values:
            values_list = [
                "NaN" if pd.isna(val) else str(val) for val in value_counts.index
            ]
            data_valores_unicos.append({"Coluna": coluna, "Valores": values_list})

    if not data_valores_unicos:
        return f"Nenhuma coluna com menos de {max_unique_values} valores únicos encontrada."

    df_valores_unicos = pd.DataFrame(data_valores_unicos)

    if show_count:
        markdown_table = "| Coluna                     | Contagem | Valores |\n"
        markdown_table += "|----------------------------|----------|---------|\n"
        for _, row in df_valores_unicos.iterrows():
            sorted_values = sorted(row["Valores"])
            count = len(sorted_values)
            markdown_table += (
                f"| {row['Coluna']:<28} | {count:^8} | {', '.join(sorted_values)} |\n"
            )
    else:
        markdown_table = "| Coluna                     | Valores |\n"
        markdown_table += "|----------------------------|---------|\n"
        for _, row in df_valores_unicos.iterrows():
            sorted_values = sorted(row["Valores"])
            markdown_table += f"| {row['Coluna']:<28} | {', '.join(sorted_values)} |\n"

    return markdown_table
