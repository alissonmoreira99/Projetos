import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from util import arredondar_numericos, cleaning_dataset, faixa_etaria, filter_columns, transform_column, treat_columns
import os
import shap

current_dir = os.path.dirname(os.path.abspath(__file__))

## CARREGAR O DATAFRAME
url = 'https://raw.githubusercontent.com/alissonmoreira99/Projetos/main/projeto-ong-passos-magicos/PEDE_PASSOS_DATASET_FIAP.csv'
pd.set_option('display.max_columns', None)
df_pm = pd.read_csv(url, delimiter=';')

if 'page' not in st.session_state:
    st.session_state.page = 'Introdução'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Menu de navegação na barra lateral
st.sidebar.header("Navegação")
menu_items = ["Introdução", "Análise de Indicadores", "Qual é o IPV do aluno?", "Impacto dos Indicadores"]
page = st.sidebar.selectbox("Selecione a Página", menu_items, index=menu_items.index(st.session_state.page))
st.sidebar.write('***Fonte:***')
st.sidebar.write('https://passosmagicos.org.br/')
 
# Atualizar a página atual no estado da sessão apenas se for diferente da atual
if page != st.session_state.page:
    navigate_to(page)


# Importando modelo
model_path = os.path.join(current_dir, 'model_passos_magicos.pkl')
try:
    model_regressor = joblib.load(model_path)
except FileNotFoundError as e:
    st.write(f"Erro ao carregar o modelo: {e}")

# Funções para cada página
def show_intro():
    st.header("A ONG Passos Mágicos")
    st.write("A Associação Passos Mágicos tem uma trajetória de 30 anos de atuação, "+
            "trabalhando na transformação da vida de"+ 
            "crianças e jovens de baixa renda, os levando a melhores oportunidades de vida."+
            " A instituição oferece um programa de educação de qualidade para crianças e "+
            "jovens do município de "+ 
            "Embu-Guaçu. Tem como sua missão transformar a vida de jovens e crianças, "+
            "oferecendo ferramentas"+
            "para levá-los a melhores oportunidades de vida, e visa viver em um Brasil "+
            "no qual todas as crianças"+
            "e jovens têm iguais oportunidades para realizarem seu sonhos e são "+
            "agentes transformadores de suas"+
            "próprias vidas.")
    st.subheader("Proposta")
    st.write("O aluno da instituição passa por um programa de aceleração de conhecimento, "+
             "onde suas maiores dificuldades "+
"acadêmicas, sociais e psicológicas são trabalhadas. É notório que a metodologia, "+
"impulsionada por fatores "+
"como empatia e cuidado, mune o aluno com as ferramentas necessárias "+
"para que ele veja a importância da educação "+
"e a use como um instrumento de transformação da sua vida.")
    st.write("Certamente, medir o desempenho do aluno no processo é um desafio, mas a passos "+
             "mágicos foi capaz de desenvolver "+
"indicadores que provém uma boa imagem do cenário. Os resultados dos "+
"alunos são avaliados por alguns pontos de perspectiva:")
    st.markdown("<h5>Dimensão Acadêmica</h5>", unsafe_allow_html=True)
    st.write("**IAN - Indicador de Adequação de Nível**")
    st.write("Capta a correspondência entre a fase do programa de aceleração do conhecimento a "+
             "qual o aluno está com o ano escolar equivalente e adequado a sua idade")
    st.write("**IDA - Indicador de Desempenho Acadêmico**")
    st.write("Expressa a proficiência dos alunos da Fase 0 (alfabetização), até a "+
             "Fase 7 (3° ano do ensino médio), nas provas aplicadas pela Associação.")
    st.write("**IEG - Indicador de Engajamento**")
    st.write("Expressa as entregas das atividades solicitadas para realização nos contraturnos "+
             "das aulas do Programa de Aceleração do Conhecimento.")
    st.markdown("<h5>Dimensão Psicossocial</h5>", unsafe_allow_html=True)
    st.write("**IAA - Indicador de Autoavaliação**")
    st.write("O seu resultado é obtido por meio de um questionário padronizado de seis "+
             "questões sobre sua avaliação de si mesmo, sua relação com os estudos, com a família, "+
             "amigos e comunidade e a sua visão sobre a Associação Passos Mágicos")
    st.write("**IPS - Indicador Psicossocial**")
    st.write("Registra o resultado da avaliação da equipe de psicologia da "+
             "associação sobre os aspectos familiares, emocionais, comportamentais "+
             "e de socialização do aluno")
    st.markdown("<h5>Dimensão Psicopedagógica</h5>", unsafe_allow_html=True)
    st.write("**IPP - Indicador Psicopedagógico**")
    st.write("Registra o resultado da avaliação da equipe de professores, pedagogos e "+
             "psicopedagogos, sobre o desenvolvimento cognitivo, o raciocínio lógico e os "+
             "aspectos comportamentais e emocionais dos alunos em sua participação no Programa "+
             "de Aceleração do Conhecimento.")
    st.write("**IPV - Indicador de Ponto de Virada**")
    st.write("Registra por meio de um questionário padronizado de nove perguntas, a avaliação da "+
             "mesma equipe de professores, pedagogos e psicopedagogos, sobre o desenvolvimento do "+
             "aluno nas aptidões necessárias para iniciar o uso da educação como um instrumento "+
             "da transformação de sua vida")
    st.subheader("O impacto da metodologia na vida das crianças...")
    st.write("O que diferencia a metodologia da Passos Mágicos de outras adotadas em escolas é o "+
             "foco em aspectos fundamentais do desenvolvimento dos alunos. Destacam-se "+
             "especialmente o engajamento, o desenvolvimento emocional, a cognição, o "+
             "comportamento e a preparação psicológica, todos trabalhados de forma integrada "+
             "e cuidadosa.")
    st.write("Relacionando com o objetivo da entidade, **como esses pontos ajudam o aluno a "+
             "perceber a importância da educação como instrumento de transformação de sua vida?**")
    st.markdown("""
    <div style="margin-top: 20px; margin-bottom: 15px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
        <h4>Próximo Conteúdo</h4>
        <p>Análise dos indicadores das dimensões psicossocial e psicopedagógica</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Adicionar botão para navegação
    if st.button("Seguir"):
        navigate_to("Análise de Indicadores")


def show_indicadores():
    st.header("Analisando alguns indicadores")
    #df_cleaned = cleaning_dataset(df_pm)
    df_2020 = filter_columns(df_pm, ['2021', '2022'])
    df_2020 = cleaning_dataset(df_2020)
    df_2021 = filter_columns(df_pm, ['2020', '2022'])
    df_2021 = cleaning_dataset(df_2021)
    df_2022 = filter_columns(df_pm, ['2020', '2021'])
    df_2022 = cleaning_dataset(df_2022)

    ## Limpando dados inconsistêntes
    df_2020 = df_2020[df_2020['IDADE_ALUNO_2020'] != 'D108']
    df_2020['IDADE_ALUNO_2020'] = df_2020['IDADE_ALUNO_2020'].astype(int)

    df_2020['FAIXA_ETARIA'] = df_2020['IDADE_ALUNO_2020'].apply(faixa_etaria)

    lista = ['IAA_2020', 'IPS_2020', 'IPP_2020', 'IEG_2020', 'IDA_2020', 'INDE_2020', 'IPV_2020']

    df_2020[lista] = df_2020[lista].apply(transform_column)
    df_2020['indice'] = 1
    filtro1 = df_2020['FAIXA_ETARIA'] == '10 a 12'
    df_2020.loc[filtro1, 'indice'] = 2
    filtro2 = df_2020['FAIXA_ETARIA'] == '13 a 15'
    df_2020.loc[filtro2, 'indice'] = 3
    filtro2 = df_2020['FAIXA_ETARIA'] == '16 a 18'
    df_2020.loc[filtro2, 'indice'] = 4
    filtro2 = df_2020['FAIXA_ETARIA'] == '19 a 21'
    df_2020.loc[filtro2, 'indice'] = 5

    ### PLOT DE IPV 2020
    df_2020['IPV_2020'] = df_2020.IPV_2020.apply(lambda a: float(a))
    fig, axes = plt.subplots(1, 1, figsize = (10, 4))
    fig.suptitle('Distribuição de notas do IPV de 2020')
    df_2020.columns = df_2020.columns.str.replace('_',' ')
    sns.histplot(df_2020['IPV 2020'].dropna(), kde = True)
    st.pyplot(fig)

    ### PLOT DE IPV 2021
    df_2021['INDE_2021'] = df_2021[df_2021['INDE_2021'] != '#NULO!']['INDE_2021']
    df_2021['PEDRA_2021'] = df_2021[df_2021['PEDRA_2021'] != '#NULO!']['PEDRA_2021']
    lista = ['IAA_2021', 'IPS_2021', 'IPP_2021', 'IEG_2021', 'IDA_2021', 'INDE_2021', 'IPV_2021']
    df_2021[lista] = df_2021[lista].apply(transform_column)
    fig, axes = plt.subplots(1, 1, figsize = (10, 4))
    fig.suptitle('Distribuição de notas do IPV de 2021')
    df_2021.columns = df_2021.columns.str.replace('_',' ')
    sns.histplot(df_2021['IPV 2021'].dropna(), kde = True)
    st.pyplot(fig)


    ### PLOT DE IPV 2022
    lista = ['IAA_2022', 'IPS_2022', 'IPP_2022', 'IEG_2022', 'IDA_2022', 'INDE_2022', 'IPV_2022']
    df_2022[lista] = df_2022[lista].apply(transform_column)
    fig, axes = plt.subplots(1, 1, figsize = (10, 4))
    fig.suptitle('Distribuição de notas do IPV de 2022')
    df_2022.columns = df_2022.columns.str.replace('_',' ')
    sns.histplot(df_2022['IPV 2022'].dropna(), kde = True)
    st.pyplot(fig)

    st.write("Em todos os anos, a distribuição de notas para IPV se manteve bem equilibrada em torno "+
             "da média e mais próxima do valor máximo.")

    #### Resumo métricas
    df_ipv_2020 = pd.DataFrame()
    df_ipv_2020['IPV'] = df_2020['IPV 2020']
    df_ipv_2020['Ano'] = '2020'
    df_ipv_2021 = pd.DataFrame()
    df_ipv_2021['IPV'] = df_2021['IPV 2021']
    df_ipv_2021['Ano'] = '2021'
    df_ipv_2022 = pd.DataFrame()
    df_ipv_2022['IPV'] = df_2022['IPV 2022']
    df_ipv_2022['Ano'] = '2022'

    df_unify = pd.concat([df_ipv_2020, df_ipv_2021, df_ipv_2022])

    df_unify_grouped = df_unify.groupby('Ano').agg(
        Média = ('IPV', 'mean'),
        Máximo = ('IPV', 'max'),
        Mínimo = ('IPV', 'min'),
    )

    df_unify_grouped['Média'] = df_unify_grouped['Média'].transform(lambda a: round(a,2))

    st.dataframe(df_unify_grouped)

    ## Distribuição por faixa etária
    df_fx_etaria = df_2020.groupby(['indice','FAIXA ETARIA']).agg({
        'IAA 2020': 'mean', 'IPS 2020':'mean', 'IPP 2020' : 'mean', 'IEG 2020':'mean', 'IPV 2020': 'mean'})\
            .sort_values(by='indice', ascending=True)
    df_fx_etaria = arredondar_numericos(df_fx_etaria)

    st.markdown("<h5> A faixa etária da criança influência no seu processo de ponto de virada?</h5>", unsafe_allow_html=True)
    st.write("Observando as médias dos indicadores por faixa etária, não fica tão claro se "+
             "existe alguma relação direta entre a idade do aluno e sua percepção da importância da educação,"+
             "refletida no indicado IPV, isto porque o valor não se diferencia tanto por faixa etária.")
    st.write('**Indicadores de 2020 por faixa etária**')
    st.dataframe(df_fx_etaria)
    st.write("A tabela diz que crianças de 7 a 9 anos são em média mais engajadas. Essa conclusão"+
             " é dada por conta do"+
             " valor do IEG. Mas isso por si só não garante um alto IPV.")
    
    st.markdown("<h5> O aluno que entrou mais cedo tem um valor maior de IPV? </h5>", unsafe_allow_html=True)

    df_ano_ingresso = df_2022.groupby(['ANO INGRESSO 2022']).agg({
        'IAA 2022': 'mean', 'IPS 2022':'mean', 'IPP 2022' : 'mean', 
        'IEG 2022':'mean', 'IPV 2022': 'mean'})\
            .sort_values(by='ANO INGRESSO 2022', ascending=True).reset_index()
    df_ano_ingresso['ANO INGRESSO 2022'] = df_ano_ingresso['ANO INGRESSO 2022'].apply(lambda a: str(a).replace('.0',''))
    df_ano_ingresso.rename(columns={'ANO INGRESSO 2022': 'Ano de Ingresso'}, inplace=True)
    df_ano_ingresso.columns = df_ano_ingresso.columns.str.replace('_',' ')

    df_ano_ingresso = arredondar_numericos(df_ano_ingresso)
    st.bar_chart(data=df_ano_ingresso, x='Ano de Ingresso', y='IPV 2022')
    st.write("O gráfico mostra o valor do indicador IPV de 2022 para alunos que entraram desde de 2016."+
             " É de certa forma esperado que quanto mais tempo o aluno passa na instuição, mais sua percepção "+
             "do valor da educação aumente. Embora os alunos que ingressaram em 2016 possuem o maior valor médio de IPV,"+
             " existe uma diferença muito baixa com relação aos alunos que ingressaram nos outros anos.")
    st.write('**A tabela abaixo mostra o valor dos indicadores em 2022 para alunos que ingressaram a partir de 2016**')

    df_ano_ingresso.columns = df_ano_ingresso.columns.str.replace(' 2022','')
    st.dataframe(df_ano_ingresso)

    st.write('**IAA - Indicador de Autoavaliação**: o indicador apresenta maior média para alunos'+
             " que ingressaram em anos mais recentes;")
    
    st.write('**IPS - Indicador Psicossocial**: o comportamento é similar ao indicador anterior, '+
             'com aumento gradual conforme mais recente é o ano;')
    
    st.write('**IPP - Indicador Psicopedagógico**: esse apresenta um comportamento mais de acordo '+
             'com o esperado, com média maior para alunos que estão a mais tempo na instituição;')
    
    st.write('**IEG - Indicador de Engajamento**: apresenta comportamento sem padrões, '+
             'com valores próximos para todos os anos de ingresso;')
    
    st.write('Visto isso, cabe analisar se o que ajuda o aluno a estar mais perto de seu ponto de '+
             'virada pode ser seu nível de engajamento, ou seu preparo emocional e psicológico. Em uma forma mais técnica,'+
             ' **os demais indicadores afetam o valor do IPV?**')

    st.markdown("<h5> Como o comportamento do aluno afeta o IPV? </h5>", unsafe_allow_html=True)


    image_path = os.path.join(current_dir, 'correlacao.png')

    # Exibir a imagem
    st.image(image_path, caption='Imagem Interna', use_column_width=True)
    
    ##### TRATAMENTO DE VARIAVEIS
    st.write("Observando os indicadores que cruzam com a linha do IPV, alguns apresentam alta correlação, "+
             "ou seja, à medida que uma variável muda, a outra tende a mudar de maneira previsível.")
    st.write("Os indicadores IPP, IEG e IDA apresentam forte correlação com IPV.")
    st.markdown("<h5> E se os indicadores apresentam alguma relação? </h5>", unsafe_allow_html=True)
    st.write("O comportamento do aluno está registrado nos indicadores, e cada ação da "+
             "Passsos Mágicos visa contribuir com o desenvolvimento e percepção do estudante com relação à educação. "+
             "Sendo assim, existe a hipótese de conseguir prever se o aluno está mais próximo "+
             "de seu ponto de virada a partir dos valores dos outros indicadores.")
    
    if st.button("Seguir"):
        navigate_to("Qual é o IPV do aluno?")
    

def show_previsao():
    st.header('Baseado no comportamento, qual é o IPV do aluno?')
    st.write("E se fosse possível, com base nas avaliações registradas do aluno, "+
             "saber se ele está no caminho certo para atingir seu ponto de virada, podendo assim usar a educação para transformar sua vida?")
    
    st.subheader("Prevendo o IPV")

    IAA_value = st.number_input(
        label='**Valor do IAA - Indicador de Autoavaliação**',
        min_value=0.0,                     # Valor mínimo permitido
        max_value=100.0,                   # Valor máximo permitido
        value=0.0,                         # Valor padrão
        step=0.01                          # Incremento permitido
    )

    IPS_value = st.number_input(
        label='**Valor do IPS - Indicador Psicossocial**',
        min_value=0.0,                     # Valor mínimo permitido
        max_value=100.0,                   # Valor máximo permitido
        value=0.0,                         # Valor padrão
        step=0.01                          # Incremento permitido
        )

    IPP_value = st.number_input(
        label='**Valor do IPP - Indicador Psicopedagógico**',
        min_value=0.0,                     # Valor mínimo permitido
        max_value=100.0,                   # Valor máximo permitido
        value=0.0,                         # Valor padrão
        step=0.01                          # Incremento permitido
        )

    IEG_value = st.number_input(
        label='**Valor do IEG - Indicador de Engajamento**',
        min_value=0.0,                     # Valor mínimo permitido
        max_value=100.0,                   # Valor máximo permitido
        value=0.0,                         # Valor padrão
        step=0.01                          # Incremento permitido
    )

    IDA_value = st.number_input(
        label='**Valor do IDA - Indicador de Desempenho Acadêmico**',
        min_value=0.0,                     # Valor mínimo permitido
        max_value=100.0,                   # Valor máximo permitido
        value=0.0,                         # Valor padrão
        step=0.01                          # Incremento permitido
    )

    indicadores = [
        IAA_value, IPS_value, IPP_value, IEG_value, IDA_value
    ]

    X_teste = pd.DataFrame([indicadores], columns=['IAA', 'IPS', 'IPP', 'IEG', 'IDA'])

    if st.button("Prever"):
        y_pred = model_regressor.predict(X_teste)
        #st.write(f"IPV: {round(y_pred[0],2)}")
        st.markdown(f"<h5>IPV: {y_pred[0]}</h5>", unsafe_allow_html=True)
        st.markdown("<small>*Pode apresentar um erro médio de 0.87 para mais ou para menos</small>", unsafe_allow_html=True)
        st.markdown("<small> Caso os indicadores tenham valor 0, a previsão será a média do IPV, que fica em torno de 6.0</small>", unsafe_allow_html=True)
        
        st.write("**Gráfico de influência dos indicadores na previsão do IPV**")
        explainer = shap.TreeExplainer(model_regressor)
        shap_values = explainer.shap_values(X_teste)
        shap_force_plot = shap.force_plot(explainer.expected_value, 
                                          shap_values[0], X_teste.iloc[0,:])
        shap_html = f"<head>{shap.getjs()}</head><body>{shap_force_plot.html()}</body>"
        st.components.v1.html(shap_html, height=150)
        
        st.write("O gráfico apresenta como o valor de cada indicador contribui para a previsão específica.")
        st.write('**Cor Vermelha:** contribuição **positiva** do indicador no valor do IPV ')
        st.write('**Cor Azul:** contribuição **negativa** do indicador no valor do IPV ')
        st.write("Quanto maior a barra, maior a contribuição do indicador no valor da previsão.")
    if st.button("Impacto dos Indicadores"):
        navigate_to("Impacto dos Indicadores")

    #st.write(f"IPV: {y_pred}")

def show_conclusao():
    st.subheader('Análise de impacto dos indicadores nos valores do IPV')
    image_path = os.path.join(current_dir, 'summary_plot.png')
    st.image(image_path, caption='Imagem Interna', use_column_width=True)
    st.write("O gráfico é uma visualização que resume a importância e o efeito de todas as "+
                "variáveis preditoras em todas as previsões do conjunto de dados.")
    st.write('Cada indicador contribui um pouco para a resposta final.'+
             ' SHAP values (SHapley Additive exPlanations)'+
             ' mostram quanto cada um contribuiu para essa previsão.')
    st.write('**Como funcionam:**')
    st.write('**Positivo:** se o SHAP value for positivo, o indicador aumentou a previsão.')
    st.write('**Negativo:** se o SHAP value for negativo, o indicador reduziu a previsão.')
    st.write("**Eixo Y:** Lista todas as variáveis preditoras ordenadas "+
                "pela importância (baseada na magnitude média dos SHAP values)")
    st.write("**Eixo X:** Representa o valor dos SHAP values. Quanto mais à direita, "+
                "mais uma variável aumenta a previsão. Quanto mais à esquerda, mais uma "+
                "variável diminui a previsão.")
    st.write("Cores: As cores indicam o valor da variável para cada previsão:")
    st.write(" **Vermelho:** Valores altos da variável preditora. **Azul:** Valores baixos da variável preditora.")
    st.markdown("<h5>Interpretação</h5>", unsafe_allow_html=True)
    st.write("Se os pontos vermelhos (valores altos) estão predominantemente à direita, "+
                "significa que valores altos dessa variável tendem a aumentar a previsão. "+
                "Se estão à esquerda, valores altos tendem a diminuir a previsão.")
    
    st.write('**IEG - Indicador de Engajamento**: tem a contribuição mais importante para a '+
             'previsão do IPV de forma geral. Valores altos tendem a aumentar o IPV, e '+
             'valores baixos, abaixar')
    
    st.write('**IPP - Indicador Psicopedagógico**: contribui de forma significativa para as '+
             'previsões. Valores altos aumentam o valor do IPV;')
    
    st.write('**Demais indicadores:** por ordem de importância, IDA, IAA e IPS, não possuem grande'+
             'impacto no valor do IPV, mas ainda sim movem o indicador;')
    
    st.subheader("Conclusão")
    st.write("Com os resultados da previsão, fica claro que trabalhar o **engajamento do aluno,** "+
             "**sua percepções, seu controle emocional e outras vertentes psicológicas,** contribuem "+
             "positivamente para que ele reconheça a importância da educação como instrumento de "+
             "transformação de sua vida. Esse é um dos diferenciais mais fortes da passos mágicos, e "+
             "fortificá-lo ajuda a instituição a identificar e antecipar ações de melhoria, para "+
             "que cada vez mais crianças tenham a oportunidade de se desenvolver através da educação.")

# Exibir a página selecionada
if st.session_state.page == "Introdução":
    show_intro()
elif st.session_state.page == "Análise de Indicadores":
    show_indicadores()
elif st.session_state.page == "Qual é o IPV do aluno?":
    show_previsao()
elif st.session_state.page == "Impacto dos Indicadores":
    show_conclusao()
