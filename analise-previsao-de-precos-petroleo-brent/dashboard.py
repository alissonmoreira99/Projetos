import joblib
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


df = pd.read_csv('analise-previsao-de-precos-petroleo-brent\precos.csv') 

# Converter a coluna 'Data' para datetime, se necessário
df['Data'] = pd.to_datetime(df['Data'])

if 'page' not in st.session_state:
    st.session_state.page = 'Introdução'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Menu de navegação na barra lateral
st.sidebar.header("Navegação")
menu_items = ["Introdução", "Visão Geral", "Análise de Preço", "Prevendo valores"]
page = st.sidebar.selectbox("Selecione a Página", menu_items, index=menu_items.index(st.session_state.page))
st.sidebar.write('Dados de 20/05/1987 a 10/06/2024')
st.sidebar.write('***Fonte:***')
st.sidebar.write('http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view')
 
# Atualizar a página atual no estado da sessão apenas se for diferente da atual
if page != st.session_state.page:
    navigate_to(page)

# Importando modelo
model_prophet = joblib.load('modelo_prophet.joblib')
    
def format_date(date_str):
    # Converter a string de data para um objeto datetime
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    # Formatar o objeto datetime para a string desejada
    formatted_date = date_obj.strftime('%d/%m/%Y')
    return formatted_date

def format_price(price):
    # Formatar o preço para o formato R$ 10,00
    formatted_price = "$ {:,.2f}".format(price).replace(',', 'X').replace('.', ',').replace('X', '.')
    return formatted_price


# Funções para cada página
def show_overview():
    st.subheader("Introdução ao Petróleo Brent")
    st.write("O petróleo Brent é uma das principais referências globais para a precificação do petróleo bruto, desempenhando um papel fundamental na determinação dos preços no mercado internacional. Originário do Mar do Norte, próximo às Ilhas Shetland, o Brent é uma mistura de diferentes tipos de petróleo extraídos dessa região, sendo reconhecido por sua qualidade e características específicas.")
    st.subheader("Origem e Produção")
    st.write("O petróleo Brent é extraído principalmente dos campos petrolíferos situados no Mar do Norte, incluindo os campos Brent, Forties, Oseberg, Ekofisk e Troll. Estes campos estão localizados em águas territoriais do Reino Unido e da Noruega, o que contribui para a sua relevância no mercado europeu e mundial.")
    st.subheader("Importância como Benchmark")
    st.write("Utilizado como referência para a precificação de aproximadamente dois terços do petróleo bruto mundial, o Brent é um dos benchmarks mais importantes do mercado, ao lado do West Texas Intermediate (WTI) dos EUA e do Dubai/Oman do Oriente Médio. Sua cotação influencia diretamente o preço de outras variedades de petróleo, bem como dos produtos derivados.")
    st.subheader("Características")
    st.write("O petróleo Brent é classificado como leve (light) e doce (sweet), devido ao seu baixo teor de enxofre e densidade relativamente baixa. Essas características tornam o Brent mais fácil e menos custoso de refinar em produtos derivados, como gasolina e diesel, em comparação com petróleos mais pesados e com maior teor de enxofre.")
    st.subheader("Mercado e Negociação")
    st.write("Os preços do petróleo Brent são amplamente negociados nos mercados futuros, particularmente na Intercontinental Exchange (ICE). O valor do Brent é influenciado por uma série de fatores, incluindo a oferta e demanda global, tensões geopolíticas, políticas de produção da OPEP (Organização dos Países Exportadores de Petróleo) e dados econômicos relevantes.")
    st.subheader("Impacto Econômico")
    st.write("As flutuações nos preços do Brent têm um impacto significativo na economia global, afetando desde os custos de transporte e produção até os preços de energia e bens de consumo. Países que são grandes produtores ou consumidores de petróleo monitoram de perto os preços do Brent para ajustar suas políticas econômicas e estratégias de mercado.")
    st.write("O papel central do petróleo Brent como referência global torna-o um indicador crucial das condições do mercado de petróleo, influenciando decisões econômicas e políticas em escala mundial. A análise de seus preços e tendências é essencial para a compreensão e planejamento estratégico no setor energético e na economia global.")
    
    st.markdown("""
    <div style="margin-top: 20px; margin-bottom: 15px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
        <h4>Próximo Conteúdo</h4>
        <p>Visão geral da análise desenvolvida</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Adicionar botão para navegação
    if st.button("Seguir"):
        navigate_to("Visão Geral")

def show_about():
    st.subheader("Sobre a Análise Desenvolvida")
    st.subheader("Comportamento histórico")
    st.write("O objetivo é realizar uma análise detalhada do comportamento histórico dos preços do petróleo Brent, correlacionando suas variações com eventos significativos, como crises econômicas, mudanças na demanda global por energia e outros fatores geopolíticos e econômicos relevantes. Compreender essas dinâmicas é fundamental para delinear um panorama claro das influências externas e internas que moldam o mercado do petróleo.")
    st.subheader("Modelo de Previsão de Preços")
    st.write("Além da análise histórica, será desenvolvido também um modelo preditivo para os preços futuros do petróleo Brent. Para isso, será utilizado o Prophet, que é uma ferramenta de previsão de séries temporais desenvolvida pela equipe de pesquisa de dados do Facebook. É especialmente projetada para lidar com dados que exibem padrões sazonais, eventos pontuais e tendências de longo prazo")
    st.markdown("""
    <div style="margin-top: 20px; margin-bottom: 15px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
        <h4>Próximo Conteúdo</h4>
        <p>Explore a Análise Temporal do Preço do Petróleo Brent.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Adicionar botão para navegação
    if st.button("Seguir"):
        st.session_state.page = "Análise de Preço"
        st.experimental_rerun()

def show_analysis():
    st.header("Análise da evolução do preço")
    
    ### Preparação dos dados
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Dia'] = df['Data'].dt.day
    
    # Usar st.columns para colocar os componentes lado a lado
    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox("Selecione o Mês", sorted(df['Data'].dt.month.unique()), 
                                      index=None)

    with col2:
        selected_year = st.selectbox("Selecione o Ano", sorted(df['Data'].dt.year.unique()), 
                                     index=None)
    #selected_month = st.selectbox("Selecione o Mês", df['Data'].dt.month.unique())
    #selected_year = st.selectbox("Selecione o Ano", df['Data'].dt.year.unique())
    date_range = st.date_input("Selecione o Intervalo de Data", [df['Data'].min(), df['Data'].max()])

    # Filtrar DataFrame com base nos filtros selecionados
    filtered_df = df[
    (df['Data'].dt.month == selected_month) &
    (df['Data'].dt.year == selected_year) &
    (df['Data'] >= pd.to_datetime(date_range[0])) &
    (df['Data'] <= pd.to_datetime(date_range[1]))
    ]
    
    df_to_show = pd.DataFrame()
    if filtered_df.empty:
        df_to_show = df
    else:
        df_to_show = filtered_df
    
    fig = px.line(df_to_show, x='Data', y='Preço', title='Variação do preço pelo tempo')
    st.plotly_chart(fig)

    st.write('Observando o gráfico acima (sem filtros), nota-se que o preço do petróleo começou a subir um pouco antes dos anos 2000, e teve seu maior pico em meados de 2008')

    st.write('Aproximando um pouco mais, é possível observar que, apesar da queda em meados de 2008 e 2009, houve aumento do preço de 2000 a 2010')

    ### Faixa 5 anos
    df['faixa_cinco_anos'] = pd.cut(df['Ano'], bins=[1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
                          labels=['1985-1990','1990-1995', '1995-2000', '2000-2005', '2005-2010', '2010-2015', '2015-2020',
                                  '2020-2025'])
    df['decada'] = pd.cut(df['Ano'], bins=[1980, 1990, 2000, 2010, 2020, 2025],
                            labels=['1980-1990','1990-2000', '2000-2010', '2010-2020', '2020-2025'])
    
    df_five = df.groupby('faixa_cinco_anos')['Preço'].mean().reset_index()
    df_five.rename(columns={'faixa_cinco_anos':'Faixa cinco anos'}, inplace=True)

    fig = px.line(df_five, x='Faixa cinco anos', y='Preço', title='Preço médio a cada 5 anos', 
                  markers=True)
    st.plotly_chart(fig)
    
    df_decada = df.groupby('decada')['Preço'].mean().reset_index()
    
    fig = px.line(df_decada, x='decada', y='Preço', title='Preço médio a cada 10 anos', markers=True)
    st.plotly_chart(fig)

    st.subheader('Principais causadores do aumento do preço do petróleo entre 2000 e 2010')
    st.write("Durante a década de 2000 a 2010, os preços do petróleo Brent passaram por aumentos significativos devido a alguns eventos e fatores chave. Aqui estão os acontecimentos mais impactantes dessa década, com descrições detalhadas sobre como cada um influenciou os preços do petróleo.")
    st.write("**Guerra do Iraque (2003)**")
    st.write("A invasão do Iraque pelos Estados Unidos e seus aliados em março de 2003 foi um dos eventos geopolíticos mais significativos da década. O conflito teve como objetivo derrubar o regime de Saddam Hussein sob a alegação de que o Iraque possuía armas de destruição em massa e apoiava o terrorismo.")
    st.write("**Impacto nos Preços do Petróleo:**")
    st.write("Incerteza na Oferta: O Iraque é um dos maiores produtores de petróleo do mundo. A invasão e a subsequente instabilidade no país criaram uma grande incerteza sobre a continuidade da produção e exportação de petróleo iraquiano.\n"+
            "Disrupção na Produção: Os ataques a infraestruturas petrolíferas e a insegurança generalizada causaram "+
            "interrupções na produção, limitando a oferta global.\n"+
            "Preços Aumentados: Como resultado, os preços do petróleo começaram a subir devido à percepção de risco e às reais "+
            "limitações na oferta.")
    st.write("**Aumento da Demanda Global (2000-2008)**")
    st.write("O rápido crescimento econômico de países como China e Índia, juntamente com a recuperação econômica global após a crise financeira asiática de 1997-1998, levou a um aumento substancial na demanda por petróleo.")
    st.write("**Impacto nos Preços do Petróleo:**")
    st.write("Crescimento Chinês: A China, em particular, experimentou um crescimento econômico explosivo, com a industrialização e "+
             "urbanização aumentando drasticamente a demanda por energia e, consequentemente, por petróleo.\n"+
             "Pressão na Oferta: A capacidade de produção global lutou para acompanhar o rápido aumento da demanda, "+
             "criando uma pressão ascendente nos preços.\n"+
             "Preços Elevados: Entre 2000 e 2008, os preços do petróleo Brent subiram consistentemente, alcançando picos "+
             "históricos devido à demanda crescente superando a oferta.")
    ############################################
    st.markdown("<h4>Crise Financeira Global (2007-2008)</h4>", unsafe_allow_html=True)
    st.write("**Variação do preço de 07/2007 a 07/2008**")
    df_ano = df.groupby(['Ano','Mes'])['Preço'].mean().reset_index()
    df_ano['Variacao'] = round((df_ano['Preço'] / df_ano['Preço'].shift(1) - 1) * 100, 2)
    df_ano['Preço'] = df_ano['Preço'].round(2)
    df_ano['Variacao'].fillna(0, inplace=True)
    df_ano.index = [''] * len(df_ano)
    condition = ((df_ano['Ano'] == 2007) & (df_ano['Mes'] >= 7)) | ((df_ano['Ano'] == 2008) & (df_ano['Mes'] <= 7)) 
    st.dataframe(df_ano[condition])

    st.write("A crise financeira global, desencadeada pelo colapso do mercado imobiliário dos EUA e pela falência de grandes instituições financeiras, levou a uma recessão econômica global.")
    st.write("**Impacto nos Preços do Petróleo**")
    st.write("Observando a tabela acima, nota-se um aumento de 75% na média mensal do preço do petróleo. Ademais, em Julho de 2008, "+
             "o valor máximo de 143,95 foi atingido, e foi o maior da história.")
    st.write("Queda Inicial na Demanda: A crise econômica reduziu drasticamente a atividade econômica global, diminuindo a demanda por "+
             "petróleo e levando a uma queda abrupta nos preços.<br>"+
             "Recuperação e Volatilidade: Após a queda inicial, os preços do petróleo começaram a se recuperar em 2009 à medida "+
             "que os pacotes de estímulo econômico foram implementados em várias economias, particularmente nos EUA e na China. "+
             "Esta recuperação levou a um aumento na demanda e, consequentemente, nos preços.<br>"+
             "Recorde de Preços: Em julho de 2008, antes do colapso total dos mercados financeiros, "+
             "o preço do petróleo Brent atingiu um recorde histórico de cerca de $147 por barril devido à especulação, "+
             "alta demanda e preocupações com a oferta.", unsafe_allow_html=True)
    st.write("Em resumo, os preços do petróleo Brent entre 2000 e 2010 foram fortemente influenciados por três principais "+
             "fatores: a Guerra do Iraque, o aumento da demanda global liderado pela China e a crise financeira global. "+
             "Cada um desses eventos contribuiu significativamente para a volatilidade e o aumento dos preços do petróleo"+
             " durante a década. A compreensão desses eventos ajuda a contextualizar as flutuações no mercado de petróleo e"+
             " a importância da estabilidade geopolítica e econômica para a segurança energética global.")
    st.markdown("**Avançando no tempo...**")
    st.write("O preço do petróleo teve grandes oscilações após a alta de 2008, atingindo mais uma marca histórica.")
    st.markdown("<h4>A Queda Histórica dos Preços do Petróleo em 2020</h4>", unsafe_allow_html=True)

    condition = df['Ano'] >= 2015

    df_ano_filtered = df[condition]

    fig = px.line(df_ano_filtered, x='Data', y='Preço')
    st.plotly_chart(fig)

    st.write("Em 2020, o preço do petróleo Brent atingiu níveis historicamente baixos, devido a uma combinação de fatores "+
             "econômicos e geopolíticos, principalmente relacionados à pandemia de COVID-19. Aqui estão os principais motivos que "+
             "levaram a essa queda significativa nos preços:")
    st.markdown("<h5>Pandemia COVID-19</h5>", unsafe_allow_html=True)
    st.write("A pandemia de COVID-19, que começou no final de 2019 e se espalhou globalmente em 2020, teve um impacto profundo na "+
             "economia mundial. Governos em todo o mundo implementaram medidas rigorosas de quarentena e restrições de viagem para "+
             "conter a propagação do vírus.")
    st.write("**Impacto nos Preços do Petróleo**")
    st.write("Redução na Demanda: As medidas de lockdown e a diminuição das atividades econômicas globais levaram a uma queda drástica "+
             "na demanda por petróleo. Setores como aviação, transporte e manufatura foram severamente afetados, reduzindo a necessidade "+
             "de combustíveis fósseis. <br>Excesso de Oferta: Com a demanda global caindo rapidamente, os produtores de petróleo enfrentaram "+
             "um excesso significativo de oferta. As instalações de armazenamento rapidamente se encheram, exacerbando a crise.", unsafe_allow_html=True)
    st.markdown("<h5>Guerra de Preços entre a Arábia Saudita e a Rússia</h5>", unsafe_allow_html=True)
    st.write("Em março de 2020, as negociações entre a OPEP (liderada pela Arábia Saudita) e a Rússia sobre cortes "+
             "na produção de petróleo falharam. A falta de acordo levou a uma guerra de preços entre esses grandes produtores de petróleo.")
    st.write("**Impacto nos Preços do Petróleo**")
    st.write("Aumento na Produção: A Arábia Saudita anunciou que aumentaria sua produção de petróleo e ofereceria grandes descontos "+
             "aos compradores, tentando ganhar participação de mercado. A Rússia respondeu com medidas semelhantes.<br>"+
             "Queda nos Preços: O aumento na produção e os descontos significativos agravaram o excesso de oferta já "+
             "causado pela redução na demanda devido à pandemia, levando os preços a cair ainda mais.", unsafe_allow_html=True)
    st.write("**Mas a única coisa que não era tão óbvia...**")
    st.markdown("<h4>Colapso dos Mercados Futuros do Petróleo em Abril de 2020</h4>", unsafe_allow_html=True)
    st.write("O colapso dos mercados futuros do petróleo em abril de 2020 foi um evento sem precedentes, onde os contratos "+
             "futuros do petróleo WTI (West Texas Intermediate) para entrega em maio caíram abaixo de zero pela primeira "+
             "vez na história. Esse evento foi causado por uma combinação de fatores relacionados à pandemia de COVID-19 e "+
             "à dinâmica do mercado de futuros de commodities.", unsafe_allow_html=True)
    st.markdown("<h5>Excesso de oferta e falta de demanda</h5>", unsafe_allow_html=True)
    st.write("Redução na Demanda: A pandemia de COVID-19 levou a uma queda dramática na demanda global por "+
             "petróleo, devido a medidas de lockdown, restrições de viagem e a redução da atividade econômica.<br>"+
             "Aumento na Produção: Simultaneamente, a guerra de preços entre a Arábia Saudita e a Rússia resultou em "+
             "um aumento na produção de petróleo, exacerbando o excesso de oferta.", unsafe_allow_html=True)
    st.markdown("<h5>Limitações de Armazenamento:</h5>", unsafe_allow_html=True)
    st.write("Capacidade de Armazenamento: Com a queda na demanda, as instalações de armazenamento de petróleo ao "+
             "redor do mundo rapidamente se encheram. Nos EUA, os tanques de armazenamento em Cushing, Oklahoma "+
             "(o principal ponto de entrega dos contratos futuros do WTI), estavam quase totalmente ocupados.<br>"+
             "Custo de Armazenamento: Com a capacidade de armazenamento esgotada, os custos de armazenar "+
             "petróleo aumentaram significativamente, contribuindo para a crise.", unsafe_allow_html=True)
    st.write("Com esse cenário, Em 20 de abril de 2020, um dia antes do vencimento dos contratos futuros de maio, os "+
             "preços do WTI caíram dramaticamente para -$37,63 por barril. Isso significa que os vendedores estavam "+
             "pagando aos compradores para aceitarem os contratos e evitarem a entrega física.")
    st.write("Ao longo de 2020, à medida que os cortes de produção entraram em vigor e as restrições de lockdown começaram a ser "+
             "levantadas, os preços do petróleo começaram a se recuperar lentamente. No entanto, a recuperação total levou mais "+
             "tempo devido à persistente incerteza econômica e à lenta recuperação da demanda.")
    st.markdown("<h4>Principais pontos de foco </h4>", unsafe_allow_html=True)
    st.markdown("<h5>Volatilidade Devida a Conflitos Geopolíticos</h5>", unsafe_allow_html=True)
    st.write("Conflitos e tensões no Oriente Médio, como a Guerra Irã-Iraque, a Guerra do Golfo e a invasão do Iraque, frequentemente resultam em aumentos abruptos nos preços do petróleo devido às preocupações com a oferta.")
    st.markdown("<h5>Influência das Crises Econômicas</h5>", unsafe_allow_html=True)
    st.write("Crises econômicas, como a crise financeira asiática e a crise financeira global, têm um impacto significativo na demanda por petróleo, levando a quedas nos preços devido à redução na atividade econômica global.")
    st.markdown("<h5>Aumento da Demanda Global e Crescimento Econômico</h5>", unsafe_allow_html=True)
    st.write("O crescimento econômico em países como China e Índia durante a década de 2000 levou a um aumento substancial na demanda por petróleo, contribuindo para o aumento dos preços durante esse período.")
    st.markdown("<h5>Decisões Estratégicas da OPEP</h5>", unsafe_allow_html=True)
    st.write("As decisões da OPEP sobre cortes ou aumentos na produção têm um impacto direto nos preços do petróleo. A falta de acordo entre os membros da OPEP+ pode resultar em guerras de preços que desestabilizam o mercado, como visto em 2020.")
    st.markdown("<h5>Impacto de Eventos Específicos</h5>", unsafe_allow_html=True)
    st.write("Eventos como o furacão Katrina e a pandemia de COVID-19 destacam como fatores específicos e inesperados podem causar disrupções significativas na oferta e demanda de petróleo, resultando em volatilidade nos preços.")
    st.markdown("<h5>Desafios de Armazenamento</h5>", unsafe_allow_html=True)
    st.write("A capacidade de armazenamento e os custos associados desempenham um papel crucial na dinâmica dos "+
             "preços do petróleo, como evidenciado pelo colapso dos mercados futuros em 2020.")
    st.markdown("<h4>Conclusão</h4>", unsafe_allow_html=True)
    st.write("A análise histórica dos preços do petróleo Brent revela que os preços são altamente sensíveis a uma "+
             "combinação de fatores geopolíticos, econômicos e específicos do mercado. Conflitos no Oriente Médio, crises "+
             "econômicas globais, crescimento na demanda, decisões estratégicas da OPEP e eventos inesperados como desastres "+
             "naturais ou pandemias têm um impacto profundo na oferta e demanda de petróleo, resultando em "+
             "volatilidade significativa nos preços. Compreender essas dinâmicas é essencial para prever e gerenciar "+
             "futuras flutuações no mercado de petróleo.")
    
    st.markdown("""
    <div style="margin-top: 20px; margin-bottom: 15px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
        <h4>Próximo Conteúdo</h4>
        <p>Prevendo valores com o modelo Meta Prophet</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Adicionar botão para navegação
    if st.button("Seguir"):
        st.session_state.page = "Prevendo valores"
        st.experimental_rerun()


def show_predictive_model():
    st.subheader('Prevendo valores')
    st.write('Devido aos dados históricos apresentarem desvios importantes '+
             'como consequencia de diversos fatos externos, é necessário um modelo que consiga '+
             'lidar especialmente com tais variações. E das opções disponíveis, o Meta Prophet é um dos'+
             ' que apresentam um ótimo desempenho.')
    st.markdown("<h5>PROPHET</h5>", unsafe_allow_html=True)
    st.write('O Prophet é uma poderosa ferramenta de modelagem de séries temporais desenvolvida '+
             'pela equipe de engenharia do Facebook. Ele foi projetado para lidar com dados de '+
             'séries temporais com padrões sazonais e é especialmente útil para negócios que '+
             'precisam fazer previsões baseadas em dados históricos. O Prophet se destaca por '+
             'ser robusto, fácil de usar e capaz de lidar com grandes quantidades de dados '+
             'com eficiência.')
    st.markdown("<h5>Análise de desempenho</h5>", unsafe_allow_html=True)
    st.write("Duas métricas serão utilizadas para mensurar o desempenho do modelo, são elas:")
    st.write("**MAPE**")
    st.write("Mean Absolute Percentage Error (Erro Percentual Absoluto Médio) "+
             "é calculada como a média dos erros percentuais absolutos entre os valores "+
             "previstos e os valores reais. A MAPE é expressa como uma porcentagem, o que facilita "+
             "a interpretação e comparação entre diferentes modelos e conjuntos de dados.")
    st.write('**RMSE**')
    st.write("O RMSE (Root Mean Square Error) é uma métrica que mede a diferença entre os valores "+
             "previstos pelo modelo e os valores observados. Ela calcula a raiz quadrada da "+
             "média dos quadrados dos erros (diferenças entre os valores previstos e os valores "+
             "observados).")
    st.write('**Gráfico de previsão**')
    st.write("Analisando o desempenho das previsões do PROPHET, utilizando 20% dos dados como teste,"+
             "observa-se que o modelo é mais sensível a quedas ou altas bruscas resultantes de fatores"+
              "externos incomuns, como é o caso de 2008 e 2020 (olhar no gráfico)")
    

    image_path = 'grafico.png'  

    # Exibir a imagem
    st.image(image_path, caption='Imagem Interna', use_column_width=True)

    st.write("Mesmo com grandes erros nos períodos incomuns, as métricas de erro continuam satisfatórias")

    metricas = {'MAE':['10.90'],"MAPE %":["13.71"], 'RMSE':['10.67']}

    metricas = pd.DataFrame(metricas)
    st.table(metricas)

    st.write('**Prever valores**')

    input_dias = int(st.slider('Quantidade de dias', 1, 90))
    
    if st.button('Prever'):
        future = model_prophet.make_future_dataframe(periods=input_dias, freq='D')
        forecast = model_prophet.predict(future)
        final_table = forecast.tail(20)
        final_table = final_table[['ds','yhat','yhat_lower','yhat_upper']]
        final_table.rename(columns={'ds':'Data', 'yhat':'Valor previsto','yhat_lower': 'Mínimo previsto',
                                    'yhat_upper':'Máximo previsto'}, inplace=True)
        final_table.Data = final_table.Data.transform(lambda x: format_date(str(x)))
        final_table['Valor previsto'] = final_table['Valor previsto']\
            .transform(lambda x: format_price(x))
        final_table['Mínimo previsto'] = final_table['Mínimo previsto']\
            .transform(lambda x: format_price(x))
        final_table['Máximo previsto'] = final_table['Máximo previsto']\
            .transform(lambda x: format_price(x))
        st.write(final_table)


# Exibir a página selecionada
if st.session_state.page == "Introdução":
    show_overview()
elif st.session_state.page == "Visão Geral":
    show_about()
elif st.session_state.page == "Análise de Preço":
    show_analysis()
elif st.session_state.page == "Prevendo valores":
    show_predictive_model()

