import spacy
from spacy.training.example import Example
import random
from spacy.lang.pt import Portuguese
from spacy.lookups import Lookups

# Carrega o modelo em português
nlp = Portuguese()
lookups = Lookups()
lookups.add_table("lexeme_norm", {})
nlp.vocab.lookups.add_table("lexeme_norm", lookups.get_table("lexeme_norm"))

# Define o conjunto de dados de treinamento
TRAIN_DATA = [
        (
        "Nome do pagador é João da Silva e o CPF é 123.456.789-00",
        {"entities": [(17, 30, "PAGADOR"), (39, 53, "CPF")]}
    ),
    (
        "RECEBEMOS DE ITA PECAS PARA VEICULOS COMERCIO E SERVICOS LTDA OS PRODUTOS E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL "
        "ELETRÔNICA INDICADA ABAIXO. EMISSÃO: 17/05/2024 VALOR TOTAL: R$ 630,56 DESTINATÁRIO: VALTER MARQUES SANTOS - "
        "RUA ARICURI LOTE 3, 32 SETOR HAB JARDIM BOTANICO BRASILIA-DF",
        {
            "entities": [
                (13, 55, "EMITENTE"),
                (93, 103, "DATA_EMISSAO"),
                (118, 127, "VALOR_TOTAL"),
                (142, 161, "DESTINATARIO"),
                (164, 213, "ENDERECO_DESTINATARIO")
            ]
        }
    ),
    (
        "NF-e Nº. 000.005.377 Série 010 DATA DE RECEBIMENTO IDENTIFICAÇÃO E ASSINATURA DO RECEBEDOR",
        {
            "entities": [
                (6, 18, "NUMERO_NFE"),
                (25, 28, "SERIE")
            ]
        }
    ),
    (
        "CHAVE DE ACESSO 2525 0506 3528 9300 4299 5501 0000 0053 7719 8482 5896",
        {
            "entities": [
                (16, 60, "CHAVE_ACESSO")
            ]
        }
    ),
    (
        "NATUREZA DA OPERAÇÃO VENDA MERC.SUJEITA A ST",
        {
            "entities": [
                (22, 43, "NATUREZA_OPERACAO")
            ]
        }
    ),
    (
        "CNPJ / CPF 06.352.893/0042-99",
        {
            "entities": [
                (10, 29, "CNPJ_EMITENTE")
            ]
        }
    ),
    (
        "DESTINATÁRIO / REMETENTE NOME / RAZÃO SOCIAL VALTER MARQUES SANTOS CNPJ / CPF 635.896.458-18",
        {
            "entities": [
                (31, 50, "DESTINATARIO"),
                (63, 77, "CPF_DESTINATARIO")
            ]
        }
    ),
    (
        "DATA DA EMISSÃO 17/05/2024",
        {
            "entities": [
                (15, 25, "DATA_EMISSAO")
            ]
        }
    ),
    (
        "VALOR TOTAL DA NOTA 630,56",
        {
            "entities": [
                (20, 26, "VALOR_TOTAL")
            ]
        }
    ),
    (
        "RECEBEMOS DE REDMIL ELETRONICOS S.A. OS PRODUTOS E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL ELETRÔNICA INDICADA ABAIXO. EMISSÃO: 11/05/2023 VALOR TOTAL: R$ 925,27 DESTINATÁRIO: JONATHAS AMORIM - RUA PIAUI, 32 - LAGOINHA BRASILIA-DF",
        {
            "entities": [
                (12, 37, "EMITENTE"),
                (89, 99, "DATA_EMISSAO"),
                (113, 122, "VALOR_TOTAL"),
                (136, 151, "DESTINATARIO"),
                (154, 180, "ENDERECO_DEST")
            ]
        }
    ),
    (
        "NF-e Nº. 000.982.124 Série 006",
        {
            "entities": [
                (6, 18, "NUMERO_NFE"),
                (26, 29, "SERIE")
            ]
        }
    ),
    (
        "CHAVE DE ACESSO 9935 2515 6161 7000 0224 5500 6000 9821 2415 4386 5552",
        {
            "entities": [
                (16, 60, "CHAVE_ACESSO")
            ]
        }
    ),
    (
        "PROTOCOLO DE AUTORIZAÇÃO DE USO 323420103745834 - 11/05/2023 09:57:08",
        {
            "entities": [
                (34, 49, "PROTOCOLO_AUT"),
                (52, 62, "DATA_AUTORIZACAO"),
                (63, 71, "HORA_AUTORIZACAO")
            ]
        }
    ),
    (
        "CNPJ / CPF 03.106.170/0002-24",
        {
            "entities": [
                (10, 27, "CNPJ_EMITENTE")
            ]
        }
    ),
    (
        "DESTINATÁRIO / REMETENTE NOME / RAZÃO SOCIAL JONATHAS AMORIM CNPJ / CPF 874.365.258-69",
        {
            "entities": [
                (31, 46, "DESTINATARIO"),
                (63, 77, "CPF_DEST")
            ]
        }
    ),
    (
        "DATA DA EMISSÃO 11/05/2023",
        {
            "entities": [
                (17, 27, "DATA_EMISSAO")
            ]
        }
    ),
    (
        "FATURA / DUPLICATA Num. 001 Venc. 10/07/2023 Valor R$ 925,27",
        {
            "entities": [
                (31, 41, "DATA_VENCIMENTO"),
                (48, 56, "VALOR_TOTAL")
            ]
        }
    ),

    (
        "TRANSPORTADOR / VOLUMES TRANSPORTADOS NOME / RAZÃO SOCIAL BRASPRESS TRANSPORTES URGENTES LTDA CNPJ / CPF 48.740.351/0127-67",
        {"entities": [
            (44, 79, "TRANSPORTADORA"),
            (89, 107, "CNPJ_TRANSPORTADORA")
        ]}
    ),
    (
        "PESO BRUTO 3,460 PESO LÍQUIDO 2,870",
        {"entities": [
            (11, 16, "PESO_BRUTO"),
            (29, 34, "PESO_LIQUIDO")
        ]}
    ),
    (
        "BLSTAG9630-011 CARREGADOR CELULAR REDMIL vICMSUFDest=9,21",
        {"entities": [
            (0, 13, "COD_PRODUTO"),
            (14, 36, "DESCRICAO_PRODUTO"),
            (48, 53, "ICMS_DEST")
        ]}
    ),
    (
        "BLSTMG-BR8-357 CABO USB-C vICMSUFDest=24,49",
        {"entities": [
            (0, 13, "COD_PRODUTO"),
            (14, 24, "DESCRICAO_PRODUTO"),
            (36, 41, "ICMS_DEST")
        ]}
    ),
    (
        """TERMO DE NOTIFICAÇÃO - CARTA
        Número de Atendimento: 1233127120300401701
        DADOS DO FORNECEDOR
        Fornecedor: Banco do Brasil S.A., Nome Fantasia: Banco do Brasil, CNPJ: 00.000.000/0001-91
        Endereço de Correspondência: Quadra SAUN Quadra 5 - Lote B - Asa Norte - Brasília - DF - 70040-250
        DADOS DO CONSUMIDOR
        Consumidor(a): AMILTON PEREIRA NUNES, CPF/CNPJ: 535.742.353-55, Endereço: Avenida Nossa Senhora
        da Vitória – 136 - Centro - São Judas - MA - 63044-060, Telefone: (98) 88333-5199, E-mail: ...""",
        {
            "entities": [
                (45, 66, "NUM_ATENDIMENTO"),
                (110, 127, "FORNECEDOR"),
                (143, 159, "NOME_FANTASIA"),
                (168, 187, "CNPJ_FORNECEDOR"),
                (215, 278, "ENDERECO_FORNECEDOR"),
                (297, 316, "CONSUMIDOR"),
                (331, 346, "CPF_CONSUMIDOR"),
                (361, 419, "ENDERECO_CONSUMIDOR"),
                (431, 447, "TELEFONE_CONSUMIDOR"),
            ]
        }
    ),
    (
        """Relato:
        DOS FATOS
        O consumidor recorre a este Órgão de Proteção e Defesa do Consumidor – PROCON/MA, no escopo de
        solicitar tutela administrativa em face da reclamada devidamente qualificada.
        Inicialmente cabe relatar que o consumidor AMILTON PEREIRA NUNES possui vínculo com o BANCO DO
        BRASIL através de uma conta corrente de pessoa jurídica cartão 6669********6441.""",
        {
            "entities": [
                (114, 132, "ORGAO"),
                (223, 242, "CONSUMIDOR"),
                (259, 274, "FORNECEDOR"),
                (334, 353, "CARTAO_CONSUMIDOR"),
            ]
        }
    ),
    (
        """DOS DIREITOS
        Art. 6º São direitos básicos do consumidor:
        III - a informação adequada e clara sobre os diferentes produtos e serviços, com
        especificação correta de quantidade, características, composição, qualidade, tributos incidentes e
        preço, bem como sobre os riscos que apresentem; (Redação dada pela Lei nº 12.741, de 2012) Vigência
        Art. 39. É vedado ao fornecedor de produtos ou serviços, dentre outras práticas abusivas:
        II - recusar atendimento às demandas dos consumidores...""",
        {
            "entities": [
                (48, 57, "ARTIGO_CDC"),
                (342, 351, "ARTIGO_CDC"),
            ]
        }
    ),
    
    (
        """PROCON SP
        PROTOCOLO/CIP: 0181284/2023
        São Paulo, 02/07/2023
        A(o) BANCO DO BRASIL S/A
        Trecho SIA Trecho 3, Lote 880, Ed. SIA SHOPPING Zona Industrial (Guará) - Brasília / DF CEP: 71200030
        Ref.: João da Silva
        Nome Social:
        CPF:11853278896 RG:
        Endereço:Rua Aureliano Rodrigues ,156, ,Vila Nova – Monte Dourado / SP CEP: 38522142 Telefone:
        Celular: 17875221458
        Email: joaosilva43@coldmail.com
        Procurador:
        CPF:
        Telefone: Celular:
        E-mail:
        Prezado(s) Senhor(es),
        O(a) consumidor(a) acima identificado(a) recorre a esta Fundação para expor e requerer o que segue:
        Dados da Compra/Contrato
        Forma de Aquisição: Não Comprei / Não Contratei
        Tipo de Contratação:
        Data da Compra/Contratação:
        Nome do Plano/Serviço/Produto:
        Detalhes do Produto/Serviço/Plano:
        Tipo do Documento:
        Nº do Contrato/Serviço/Documento:
        Data da Ocorrência/Serviço/Entrega:
        Data de Cancelamento/Desistência/Negativa:
        Forma de Pagamento:
        Valor da Compra:
        Banco Emissor:
        Número do Banco:
        Agência:
        Conta:
        Cartão:
        SECRETARIA DA JUSTIÇA E CIDADANIA
        FUNDAÇÃO DE PROTEÇÃO E DEFESA DO CONSUMIDOR
        DIRETORIA DE ATENDIMENTO E ORIENTAÇÃO AO CONSUMIDOR
        #interna
        Bandeira:
        Descrição do Problema / Relato do Consumidor:
        Venho por meio desta registrar uma reclamação referente ao atendimento na agência do Banco do Brasil localizada em Monte
        Dourado/SP, no dia 01 de julho de 2023.
        No referido dia, fui à agência para realizar um atendimento e o tempo de espera foi de 32 minutos. Considero esse tempo
        excessivo e incompatível com um atendimento eficiente e respeitoso ao consumidor. Tal demora causou-me transtornos e
        prejuízos, uma vez que precisei reorganizar meus compromissos devido à longa espera.
        Solicito que sejam tomadas as devidas providências para melhorar o tempo de atendimento na referida agência, garantindo
        assim um serviço mais ágil e eficiente para todos os clientes.
        Agradeço pela atenção e aguardo um retorno sobre as medidas que serão adotadas.
        Pedido:
        Providências/melhoria de processo
        Assim sendo, a Fundação Procon SP solicita apreciação do exposto e manifestação expressa no prazo previsto em sistema,
        visando apresentação das considerações necessárias à solução ou elucidação do assunto. Após o prazo de resposta
        poderá ser formalizado Processo Administrativo, nos termos da Lei Federal nº 8.078/90, Lei Estadual nº 9.192/95 e Portaria
        Normativa nº 247, de 10/11/2021, bem como a adoção de outras medidas cabíveis.
        Sem mais para o momento, subscrevemo-nos. Atenciosamente,""",
        {
            "entities": [
                (0, 7, "ORGAO"), 
                (21, 37, "PROTOCOLO_CIP"), 
                (40, 50, "DATA"),
                (55, 73, "DESTINATARIO"),
                (75, 148, "ENDERECO_DESTINATARIO"),
                (155, 168, "CONSUMIDOR"),
                (184, 195, "CPF_CONSUMIDOR"),
                (207, 255, "ENDERECO_CONSUMIDOR"),
                (274, 285, "CELULAR_CONSUMIDOR"),
                (293, 315, "EMAIL_CONSUMIDOR"),
                (987, 1001, "DATA_OCORRENCIA"),
                (1052, 1065, "TEMPO_ESPERA"),
            ]
        }
    ),

    (
        """TERMO DE NOTIFICAÇÃO - CARTA
        Número de Atendimento: 1233127120300401701
        DADOS DO FORNECEDOR
        Fornecedor: Banco do Brasil S.A. , Nome Fantasia: Banco do Brasil , CNPJ: 00.000.000/0001-91
        Endereço de Correspondência: Quadra SAUN Quadra 5 - Lote B - Asa Norte - Brasília - DF - 70040-250
        DADOS DO CONSUMIDOR
        Consumidor(a): AMILTON PEREIRA NUNES, CPF/CNPJ: 535.742.353-55 , Endereço: Avenida Nossa Senhora
        da Vitória – 136 - Centro - São Judas - MA - 63044-060 , Telefone: (98) 88333-5199 , E-mail:
        O(a) consumidor(a) acima qualificado recorre a este Instituto de Promoção e Defesa do Cidadão e Consumidor do
        Estado do Maranhão - PROCON/MA e, na presença do(a) servidor(a) e abaixo subscrito, apresenta os seguintes
        fatos:
        Relato:
        DOS FATOS
        O consumidor recorre a este Órgão de Proteção e Defesa do Consumidor – PROCON/MA, no escopo de
        solicitar tutela administrativa em face da reclamada devidamente qualificada.
        Inicialmente cabe relatar que o consumidor AMILTON PEREIRA NUNES possui vínculo com o BANCO DO
        BRASIL através de uma conta corrente de pessoa jurídica cartão 6669********6441.
        Alude o consumidor que sua conta foi bloqueada, sem qualquer justificativa prévia, e ao tentar utilizar por
        duas vezes seu cartão em estabelecimentos diferentes, foi recusado. Ocorre que atualmente o consumidor
        não consegue movimentar sua conta e solicita o desbloqueio da mesma.
        Destarte, o consumidor recorre a este instituto de Proteção e Defesa do Consumidor no escopo de solicitar
        tutela administrativa em face da reclamada acima qualificada.
        DOS DIREITOS
        Considerando as alegações relatadas, faz-se necessário a citação dos direitos elencados na Lei
        8.078/90 (Código de Defesa do Consumidor) quanto às políticas nacionais acerca das Relações de Consumo.
        Art. 4º A Política Nacional das Relações de Consumo tem por objetivo o atendimento das
        necessidades dos consumidores, o respeito à sua dignidade, saúde e segurança, a proteção de seus
        interesses econômicos, a melhoria da sua qualidade de vida, bem como a transparência e harmonia
        das relações de consumo, atendidos os seguintes princípios:
        I - reconhecimento da vulnerabilidade do consumidor no mercado de consumo;
        III - harmonização dos interesses dos participantes das relações de consumo e
        compatibilização da proteção do consumidor com a necessidade de desenvolvimento econômico e
        tecnológico, de modo a viabilizar os princípios nos quais se funda a ordem econômica (art. 170, da
        Constituição Federal), sempre com base na boa-fé e equilíbrio nas relações entre consumidores e
        fornecedores;
        Art. 6º São direitos básicos do consumidor:
        III - a informação adequada e clara sobre os diferentes produtos e serviços, com
        especificação correta de quantidade, características, composição, qualidade, tributos incidentes e
        preço, bem como sobre os riscos que apresentem; (Redação dada pela Lei nº 12.741, de
        2012) Vigência
        IV - a proteção contra a publicidade enganosa e abusiva, métodos comerciais coercitivos ou
        desleais, bem como contra práticas e cláusulas abusivas ou impostas no fornecimento de produtos e
        serviços;
        VI - a efetiva prevenção e reparação de danos patrimoniais e morais, individuais, coletivos e
        difusos;
        VIII - a facilitação da defesa de seus direitos, inclusive com a inversão do ônus da prova, a
        seu favor, no processo civil, quando, a critério do juiz, for verossímil a alegação ou quando for ele
        hipossuficiente, segundo as regras ordinárias de experiências;
        Art. 14. O fornecedor de serviços responde, independentemente da existência de culpa, pela
        reparação dos danos causados aos consumidores por defeitos relativos à prestação dos serviços, bem
        como por informações insuficientes ou inadequadas sobre sua fruição e riscos.
        § 1° O serviço é defeituoso quando não fornece a segurança que o consumidor dele pode
        esperar, levando-se em consideração as circunstâncias relevantes, entre as quais:
        I - o modo de seu fornecimento;
        II - o resultado e os riscos que razoavelmente dele se esperam;
        III - a época em que foi fornecido.
        Art. 39. É vedado ao fornecedor de produtos ou serviços, dentre outras práticas abusivas:
        II - recusar atendimento às demandas dos consumidores, na exata medida de suas
        disponibilidades de estoque, e, ainda, de conformidade com os usos e costumes;
        III - enviar ou entregar ao consumidor, sem solicitação prévia, qualquer produto, ou
        fornecer qualquer serviço;
        IV - prevalecer-se da fraqueza ou ignorância do consumidor, tendo em vista sua idade,
        saúde, conhecimento ou condição social, para impingir-lhe seus produtos ou serviços;
        V - exigir do consumidor vantagem manifestamente excessiva;
        Da Cobrança de Dívidas
        Art. 42. Na cobrança de débitos, o consumidor inadimplente não será exposto a ridículo,
        nem será submetido a qualquer tipo de constrangimento ou ameaça.
        Parágrafo único. O consumidor cobrado em quantia indevida tem direito à repetição do
        indébito, por valor igual ao dobro do que pagou em excesso, acrescido de correção
        monetária e juros legais, salvo hipótese de engano justificável.
        Art. 42-A. Em todos os documentos de cobrança de débitos apresentados ao
        consumidor, deverão constar o nome, o endereço e o número de inscrição no Cadastro de
        Pessoas Físicas – CPF ou no Cadastro Nacional de Pessoa Jurídica – CNPJ do fornecedor
        do produto ou serviço correspondente.
        Pedido:
        DOS PEDIDOS
        Diante do exposto e, reconhecendo-se a vulnerabilidade dos consumidores, a busca pela efetividade de seus
        direitos, a concretização da Constituição Federal, no que diz respeito a sua proteção e defesa, o que os alça a
        direitos fundamentais, requer-se:
        I. Esclarecimentos plausíveis acerca dos fatos alegados;
        II. Solicita o imediato desbloqueio do limite do cartão, atendendo os dispostos do art. 14º
        do CDC.
        Dispositivos legais aplicáveis:
        Diante do exposto, este Instituto de Promoção e Defesa do Cidadão e Consumidor do Estado do Maranhão -
        PROCON MA, com fundamento no art. 55, § 4º da Lei Federal nº 8.078/90, c/c com o artigo 34 do Decreto Federal
        nº2.181/97, NOTIFICA Vossa Senhoria, para que encaminhe resposta com posicionamento conclusivo acerca da
        reclamação acima relacionada. Para tanto, fica estabelecido o prazo de 10 (dez) dias corridos a contar do
        recebimento desta, sejam apresentadas as devidas informações e/ou soluções pertinentes para o caso em epígrafe.
        Decorrido o prazo, poderá este órgão instaurar processo administrativo para apurar eventual infração à Lei 8.078/90,
        bem como para apreciar a fundamentação da reclamação do consumidor, para efeito de sua inclusão nos Cadastros
        Estadual e Nacional de Reclamação Fundamentada, nos termos do art. 44 da Lei 8.078/90. Adverte, por fim, que a
        ausência de manifestação no prazo concedido ensejará a apuração de eventual crime de desobediência, nos termos
        do art. 55 e 56 do CDC e art. 330 do Código Penal.
        OBS¹: Este Instituto possui sistema eletrônico para protocolizar defesas de CARTA e AUDIÊNCIA via Web, porém é
        necessário a efetivação de cadastro para que possa utilizar a nossa ferramenta. Informe-se através de nosso site:
        https://www.procon.ma.gov.br/adesao-eletronica-do-fornecedor/ .
        OBS²: Ressalta-se que a resposta de reclamações registradas em face de fornecedor(es) que não possui cadastro
        na Plataforma ProConsumidor, deverá ser encaminhada/protocolada, ao Setor de Protocolo deste Instituto de
        Promoção e Defesa do Cidadão e Consumidor do Estado do Maranhão – PROCON/MA, situado Rua Castelo
        Branco, Nº 2238, São José - CEP: 62056-050 - São Judas/MA, que funciona das 08:00 às 18:00, de segunda a
        sexta-feira. O documento deverá mencionar, obrigatoriamente, o número do atendimento, bem como o nome e o
        CPF do consumidor. Caso esses dados não sejam citados, a resposta não será juntada à reclamação e, portanto,
        será desconsiderada. O Procon Maranhão solicita que seja encaminhada cópia da resposta também para o endereço
        do consumidor.
        14 de Março de 2024
        Thais Pereira Barros""",
        {
            "entities": [
                (40, 58, "ID_ATENDIMENTO"),
                (97, 117, "NOME_FORNECEDOR"),
                (119, 134, "NOME_FANTASIA"),
                (143, 161, "CNPJ"),
                (182, 234, "ENDERECO_FORNECEDOR"),
                (266, 285, "NOME_CONSUMIDOR"),
                (287, 300, "CPF_CONSUMIDOR"),
                (312, 380, "ENDERECO_CONSUMIDOR"),
                (393, 407, "TELEFONE_CONSUMIDOR"),
                (416, 431, "DATA_DOCUMENTO"),
                (1371, 1376, "NUMERO_CARTAO"),
                (2210, 2223, "ARTIGO_CDC"),
                (2245, 2266, "LEI_REFERIDA"),
                (2420, 2429, "URL_SITE"),
                (2825, 2874, "ENDERECO_PROTOCOLO_PROCON"),
                (2880, 2901, "HORARIO_FUNCIONAMENTO"),
                (2980, 2999, "DATA_EXPEDICAO"),
                (3000, 3020, "NOME_RESPONSAVEL")
            ]
        }
    ),

    (
        """TERMO DE NOTIFICAÇÃO - CARTA ELETRÔNICA
        Número de Atendimento:
        2702022300100536303,2402036081000566301,4560273230100563332
        DADOS DO FORNECEDOR
        Fornecedor:
        Banco do Brasil S.A.
        BANCO ITAU BBA S.A.
        CAIXA ECONÔMICA FEDERAL
        CNPJ:
        00.000.000/0001-91
        17.298.092/0001-30
        00.360.305/0001-04
        Endereço:
        Quadra SAUN Quadra 5 - Lote B - Asa Norte - Brasília - DF - 70040-250
        Avenida Brigadeiro Faria Lima - - Número 3500, ANDAR: 1-2-3 PARTE 4 E 5; - Itaim Bibi - São
        Paulo - SP - 04538-132
        Quadra SBS Quadra 1 - Bloco L - 11º Andar - Asa Sul - Brasília - DF - 70070-110
        Endereço de Correspondência:
        Telefone Institucional:
        (61) 3493-0000
        (11) 3003-4828
        (61) 3206-9838, (61) 3521-8600
        E-mail Institucional:
        unidadeouvidoria@bb.com.br
        protocolocentralprocon@itau-unibanco.com.br
        ouvid@caixa.gov.br
        DADOS DO CONSUMIDOR
        Consumidor: ZACARIAS PAULINO FRANCO
        CPF/CNPJ: 244.445.665-66
        Endereço: Rua Marechal Bezerra - Ipirapitinga - Juiz de Fora -
        MG – 36333-360
        Telefone: (32) 3454-6414
        Relato:
        O consumidor alega desconhecimentos acerca de algumas contratações referente à
        empréstimos.
        Embora o consumidor já tenha ido até as agências para verificar os lançamentos de
        créditos em sua conta, não foi possível ainda esclarecer, de pleno, os fatos.
        Portanto, faz-se necessária notificação dos bancos reclamados para que preste alguns
        esclarecimentos e apresente documentação pertinente a conta sob titularidade do
        requerente.
        DOS DIREITOS:
        Art 6º - São direitos básicos do consumidor:
        Art 6º, II - a educação e divulgação sobre o consumo adequado dos produtos e serviços,
        asseguradas a liberdade de escolha e a igualdade nas contratações;
        DOS PEDIDOS:
        - Requer apresentação dos extratos bancários completos e detalhados de
        Janeiro de 2020 até a presente data (de todas as possíveis contas que o
        consumidor seja titular).
        PRAZO PARA RESPOSTA: 10/03/2024
        O SEDECON, nos termos da Lei nº 8.078/90, que dispõe sobre a proteção do
        consumidor, NOTIFICA Vossa Senhoria, para que encaminhe resposta com
        posicionamento conclusivo acerca da reclamação acima relacionada. Para tanto, fica
        estabelecido o prazo de 10 (dez) dias corridos para apresentação da resposta
        eletrônica, sendo que em caso de composição amigável, solicitamos a juntada de
        documentação comprobatória do atendimento ao pleito do consumidor.
        Nos casos de reclamações que envolvam outras empresas, ligadas ao serviço ou
        produto adquirido, o fornecedor deverá apresentar documento formal de atendimento
        da demanda. Assim como, na hipótese de haver mais de um fornecedor envolvido,
        pelo princípio da solidariedade, a reclamada deverá interagir com o mesmo e
        apresentar tal resultado.
        A ausência de manifestação no prazo ora estabelecido ou a falta de resposta
        conclusiva, esse órgão apreciará a fundamentação da reclamação do consumidor,
        para efeito de sua inclusão no Cadastro de Reclamações Fundamentadas, nos termos
        do art. 44 da Lei 8.078/90, prosseguindo o trâmite da reclamação, nos termos dos
        artigos 45, 46 e 47 do Decreto 2.181/97, além das possíveis sanções administrativas
        previstas no Código Defesa do Consumidor e legislações correlatas.
        29 de Fevereiro de 2024
        Caroline dos Santos Noise""",
        {
            "entities": [
                (39, 63, "ID_ATENDIMENTO"),
                (87, 105, "NOME_FORNECEDOR"),
                (107, 126, "NOME_FORNECEDOR"),
                (128, 152, "NOME_FORNECEDOR"),
                (161, 179, "CNPJ"),
                (181, 200, "CNPJ"),
                (202, 220, "CNPJ"),
                (231, 287, "ENDERECO_FORNECEDOR"),
                (288, 367, "ENDERECO_FORNECEDOR"),
                (368, 423, "ENDERECO_FORNECEDOR"),
                (472, 487, "TELEFONE_INSTITUCIONAL"),
                (489, 504, "TELEFONE_INSTITUCIONAL"),
                (506, 532, "TELEFONE_INSTITUCIONAL"),
                (546, 575, "EMAIL_INSTITUCIONAL"),
                (577, 617, "EMAIL_INSTITUCIONAL"),
                (619, 636, "EMAIL_INSTITUCIONAL"),
                (650, 673, "NOME_CONSUMIDOR"),
                (686, 700, "CPF_CONSUMIDOR"),
                (711, 764, "ENDERECO_CONSUMIDOR"),
                (766, 777, "CEP_CONSUMIDOR"),
                (789, 803, "TELEFONE_CONSUMIDOR"),
                (1222, 1227, "ARTIGO_CDC"),
                (1315, 1325, "DATA_INICIAL"),
                (1351, 1361, "DATA_ATUAL"),
                (1378, 1388, "DATA_RESPOSTA"),
                (1411, 1421, "LEI_REFERIDA"),
                (2144, 2176, "DATA_DOCUMENTO"),
                (2177, 2198, "NOME_RESPONSAVEL")
            ]
        }
    ),
]


# Define o componente NER no pipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")
ner.add_label("PAGADOR")
ner.add_label("CPF")

# Desabilita outras partes do pipeline para acelerar o treinamento
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  
    # Configura o treinamento
    optimizer = nlp.begin_training()
    for i in range(30):  # 30 épocas
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Perda na época {i}: {losses}")

# Salva o modelo ajustado
output_dir = "./ner_model"
nlp.to_disk(output_dir)
print("Modelo salvo em:", output_dir)
