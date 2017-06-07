# -*- coding: utf-8 -*-
import GenAlgoritmImp; 	

#Nome do Arquivo  de entrada deve estar na Pasta _InputFiles
inputFileName = 'P-n16-k8.vrp';
#Número de Caminhões a ser utilizada
numTrucks = 8;
#Número de Individuos na População
numIndividuos = 100;
#Indica se será permitida a criação de rotas com caminhões rodando com um valor maior do que a capacidade
permiteSobrecarga = False;
#Na criação de um novo individuo indica a chance de inserir um retorno ao deposito no meio do cromossomo
chanceRetDeposito = 0.1;
#Penalidade a ser aplicada sobre a sobrecarga (Carga-Capacidade)*penalidadeSobrecarga
penalidadeSobrecarga = 20;	
#Um veiculo é considerado parado se o mesmo nó aparecer duas vezes seguidas no mesmo cromossomo
#Existe a possibilidade de isto ocorrer devido a mutações, esta flag indica se esta parada será penalizada
penalizaParada = True;
#A penalidade por parada será calcula da seguinte forma (Número de Passos parado)*penalidadeParada
penalidadeParada = 50;
#Foram implementadas dois tipos de mutação
#1 Troca de rota, onde um nó é escolhido aleatoriamente e sua posição é alterada para outro ponto no cromossomo
#2 Troca de Rota com retorno a origem, neste caso o nó  é selecionado aletoriamente e trocado de rota e no seu lugar de origem
#é adicionado um nó deposito. Se o no selecionado for um deposito ele é retirado do cromossomo
#Esta variável se refere a chance de ser executada a mutação do tipo 1
chanceMutacaoTrocaDeRota = 0.75
#Indica se será feita uma troca total ou seja Nova população substitui inteiramente a antiga
#Ou troca parcial onde os melhores individuos da população combinada, nova e antiga são colocados
trocaTotal = False;
#Chance de ser executada uma mutação
indiceMutacao = 0.125;
#Chance de ser executada uma reprodução
indiceReproducao = 0.125;
#Total de Iterações do algoritmo
totalInteracoes = 100
#Indica se será salvo arquivo ao final
saveFile = True;
#Indica se será salvo gráfico ao final
saveFigure=True;
#Código do experimento
codExp = 1;
#Nome do arquivo de saida
outputFileName = 'Saida-'

#Executa o algoritmo com todos os parâmetros
GenAlgoritmImp.ExecutaAlgortimoGenetico(inputFileName,numTrucks,numIndividuos,permiteSobrecarga,chanceRetDeposito,penalidadeSobrecarga,penalizaParada,penalidadeParada,chanceMutacaoTrocaDeRota,totalInteracoes,saveFile,saveFigure,codExp,outputFileName,trocaTotal,indiceReproducao,indiceMutacao)