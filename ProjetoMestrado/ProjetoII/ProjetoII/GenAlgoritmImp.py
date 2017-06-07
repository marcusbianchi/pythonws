# -*- coding: utf-8 -*-
import math
from random import randint
import matplotlib
matplotlib.use('Agg')
from datetime import datetime;
import matplotlib.pyplot as plt;
import random
import string
import itertools
import statistics;

#Método auxiliar para quebra de Lista
def isplit(iterable,splitters):
	return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

#Encontra o indice de um valor
def findItem(searchList,value):
	listLocal = list(searchList)		
	for i in range(len(listLocal)):		 
		if(str(listLocal[i])==str(value)):
				return i;			
	return -1;
	
#Método que prepara a escrito do arquivo.	
def preparaArquivo(numExp,filename,numTrucks,numIndividuos,permiteSobrecarga,chanceRetDeposito,penalidadeSobrecarga,penalizaParada,penalidadeParada,chanceMutacaoTrocaDeRota,totalInteracoes,indiceReproducao,indiceMutacao,trocaTotal):
	#Abre o arquivo para salvar os dados;
	filename =  'Exp_Func2'+str(numExp);
	f1=open('./OutPutFiles/'+filename+'.txt', 'w')
	f1.write('Número de Individuos'+'\t'+'Número de Veiculos'+'\t'+'Permite Sobrecarga'+'\t'+'Chance de Retorno ao Deposito'+'\t'+'Penalidade Sobrecarga'+'\t'+'Penaliza Parada'+'\t'+'Penalidade da Parada'+'\t'+'Chance de Mutação Troca de Rota'+'\t'+'Indice de Reprodução'+'\t'+'Indice de Mutacao'+'\t'+'Limite de Iteração'+'\t'+'Troca Total'+'\n')	
	f1.write(str(numIndividuos)+'\t'+str(numTrucks)+'\t'+str(permiteSobrecarga)+'\t'+str(chanceRetDeposito)+'\t'+str(penalidadeSobrecarga)+'\t'+str(penalizaParada)+'\t'+str(penalidadeParada)+'\t'+str(chanceMutacaoTrocaDeRota)+'\t'+str(indiceReproducao)+'\t'+str(indiceMutacao)+'\t'+str(trocaTotal)+'\t'+str(totalInteracoes)+'\n')		
	return f1;

	
#Método utilizado para encontrar a capacidade dos caminhões
def encontrarCapacidade(inputFileName):
	#Inicia a variável capacidade
	Capacity = 0;
	#Abre o arquivo para leitura
	with open('./_Inputfiles/'+inputFileName) as f:
		#varre as linhas do arquivo
		for content in f:			
			#limpa os espaços do conteudo
			content = ''.join(content);
			content = content.replace(" ", "")
			content = content.split(':');
			#Verifica se a linha se refere ao valor de capacidade
			if(content[0]=='CAPACITY'):
				#se for o valor da Capacidade retorna o valor
				Capacity=content[1]
				break;
	return Capacity;

#Método que encontra as coordenadas dos nós	
def encontraCoordenadas(inputFileName):
	#Inicia o dicionario que armazenará as coordenadas de cada nó
	dicNodes = [];
	saveCoord = False;
	#Abre o arquivo para leitura
	with open('./_Inputfiles/'+inputFileName) as f:
		#varre as linhas do arquivo
		for content in f:	
			content= content.strip();
			#checa se a seção de coordenadas dos nós terminou
			if(saveCoord):
				try:
					val = int(content[0])
				except ValueError:
					break;
			#Adiciona as coordenadas de cada nós no dicionário
			if(saveCoord):
				content = content.split(' ');
				node={};
				node['Name'] = content[0];
				node['Coord'] = [int(content[1]),int(content[2])];
				dicNodes.append(node);
			#Checa se a seção com as coordendas dos nós foi encopntrada
			if(content=='NODE_COORD_SECTION'):
				saveCoord = True;
	return dicNodes;

#Método que recebe uma lista de nós e adiciona a demanda a cada um deles caso haja.
def defineDemandas(inputFileName,dicNodes):
	saveDenand = False;
	#Abre o arquivo para leitura
	with open('./_Inputfiles/'+inputFileName) as f:
		#varre as linhas do arquivo
		for content in f:	
			content= content.strip();
			#checa se a seção de coordenadas dos nós terminou
			if(saveDenand):
				try:
					val = int(content[0])
				except ValueError:
					break;
			#Adiciona as coordenadas de cada nós no dicionário
			if(saveDenand):
				content = content.split(' ');
				for node in dicNodes:
					if node['Name'] == content[0]:
						node['Demand'] = int(content[1]);					
			#Checa se a seção com as coordendas dos nós foi encopntrada
			if(content=='DEMAND_SECTION'):
				saveDenand = True;
	return dicNodes;

#Método que encontra os nós que são depositos
def encontraDepositos(inputFileName):
	#Inicia o dicionario que armazenará os Nós que são depositos
	dicDepo = [];
	saveDepo = False;
	#Abre o arquivo para leitura
	with open('./_Inputfiles/'+inputFileName) as f:
		#varre as linhas do arquivo
		for content in f:	
			content= content.strip();
			#checa se a seção de Depositos dos nós terminou
			if(saveDepo):
				if(content=='-1'):
					break;
			#Adiciona os nós deposito a lista
			if(saveDepo):
				dicDepo.append(int(content[0]));
			#Checa se a seção com os depositos foi encopntrada
			if(content=='DEPOT_SECTION'):
				saveDepo = True;
	return dicDepo;

#Método utilizado para calcular a distância entre dois nós
def calcDist(oriNodeID,destNodeID,dicNodes):
	for node in dicNodes:
		if(int(node['Name']) == int(oriNodeID)):
			oriNode = node;
		if(int(node['Name']) == int(destNodeID)):
			destNode = node;
	xi = destNode['Coord'][0];
	xj = destNode['Coord'][1];
	yi = oriNode['Coord'][0];
	yj = oriNode['Coord'][1];
	xd = xi - yi
	yd = xj - yj
	return int(round(math.sqrt(xd**2+yd**2),0));
	
#Calcula a penalidade por ficar parado total para o individuo
def calcPenalidadeParada(individuo,penalidadeParada):
	cromossomo  = list(individuo['Crom']);
	#Quebra a lista quando encontrar as letras que representam as rotas
	posAtual = 0;
	rotalAtual = '';
	rotas = {}
	#Quebra o cromossomo nas rotas de cada caminhão
	while(len(cromossomo)!=0):
		if(not isinstance(cromossomo[posAtual],int)):
			rotalAtual = cromossomo.pop(posAtual);
			rotas[rotalAtual] = [];
		else:
			rotas[rotalAtual].append(cromossomo.pop(posAtual));
	totalParada = 0;
	for rotaID in rotas:
		rota = rotas[rotaID];
		#Como todas as rotas iniciam em 1 e isto não esta no cromossomo, este deve ser adicionado		
		rota.insert(0,1);
		#Todas as rotas terminam no ponto 1 e isto não será representado no cromossomo
		rota.insert(len(rota)-1,1);
		for i in range(len(rota)-1):
					if(rota[i]==rota[i+1]):
						totalParada = totalParada + 1;	
	return totalParada*penalidadeParada

#Método que retorna todas as rotas e subrotas de cada caminhão
def splitRotas(cromossomo,dicDepo):
	#Quebra a lista quando encontrar as letras que representam as rotas
	posAtual = 0;
	rotalAtual = '';
	rotas = {}
	tupleDepo = tuple(dicDepo);
	#Quebra o cromossomo nas rotas de cada caminhão
	while(len(cromossomo)!=0):
		if(not isinstance(cromossomo[posAtual],int)):
			rotalAtual = cromossomo.pop(posAtual);
			rotas[rotalAtual] = [];
		else:
			rotas[rotalAtual].append(cromossomo.pop(posAtual));
	#Quando existe um retorno ao depositó cada caminhão terá duas subrotas, sendo assim é necessário dividi-las
	for rota in rotas:		
		rotas[rota] = isplit(rotas[rota],tupleDepo)	
	return rotas;
		
#Método que Calcula a carga máxima de cada rota/caminhão
#Quando existem subrotas a demanda da maior é considerada
def calcCarga(cromossomo,dicDepo,dicNodes):
	localCrom = list(cromossomo)
	rotasCrom = splitRotas(localCrom,dicDepo);
	maxCarga = 0;
	#Procura dentro da cada Rota do Cromossomo
	for rota in rotasCrom:
		#Procura dentro da cada subrota para cada caminhão
		for subrota in rotasCrom[rota]:
			#Verifica qual é a demanda para cada nó dentro da Rota
			demandaTotalSubRota = 0;
			for item in subrota:				
				for node in dicNodes:				
					if int(node['Name']) == int(item):
						demandaTotalSubRota = demandaTotalSubRota + node['Demand']
			if(demandaTotalSubRota>maxCarga):
				maxCarga = demandaTotalSubRota;
	return maxCarga;

#Método que Inicializa o Indviduo de acordo com alfabeto e a regra de sobrecarga
def initCromIndividuo(dicNodes,dicDepo,numTrucks,chanceRetDeposito):
	listNodes = [];
	for node in dicNodes:
		listNodes.append(int(node['Name']))
	lisrDepo = [];
	for depo in dicDepo:
		lisrDepo.append(int(depo))
	for i in range(len(listNodes)):	
		selectRandom = random.uniform(0,1)
		if(selectRandom<chanceRetDeposito):
			listNodes.append(random.choice(lisrDepo));
	random.shuffle(listNodes);
	truckPositions = random.sample(range(1, len(listNodes)), numTrucks-1)
	truckPositions.sort()
	letters = list(string.ascii_lowercase);
	listNodes.insert(0,letters[0])
	letterPos = 1;
	for pos in truckPositions:
		listNodes.insert(pos,letters[letterPos])
		letterPos += 1; 
	#print listNodes
	return listNodes;

#Inicializa a população e retorna a lista de Individuos
def initPopulacao(dicNodes,dicDepo,permiteSobrecarga,numTrucks,capacidade,chanceRetDeposito,numIndividuos):
	#Inicializa os individuos até que a população esteja completa
	listPopulacao =[];
	while(len(listPopulacao)<numIndividuos):
		isViable = False;
		while(not isViable):
			cromossomo =  initCromIndividuo(dicNodes,dicDepo,numTrucks,chanceRetDeposito)
			carga = calcCarga(cromossomo,dicDepo,dicNodes);
			if(permiteSobrecarga):
				novoIndividuo = {};
				novoIndividuo['Crom'] = cromossomo;
				novoIndividuo['maxCarga'] = carga;
				novoIndividuo['Fitness'] = 0;
				listPopulacao.append(novoIndividuo);
				isViable = True;
			else:
				if(int(carga)<int(capacidade)):
					novoIndividuo = {};
					novoIndividuo['Crom'] = cromossomo;
					novoIndividuo['maxCarga'] = carga;
					novoIndividuo['Fitness'] = 0;
					listPopulacao.append(novoIndividuo);
					isViable = True;
	return listPopulacao;

#Calcula o Fitness de cada Individuo considerando as penalidades
def calcFitness(listPopulacao,dicNodes,permiteSobrecarga,capacidade,penalidadeSobrecarga,penalizaParada,penalidadeParada):
	#Calcula o o Fitness de cada individuo
	for individuo in listPopulacao:
		cromossomo = list(individuo['Crom'])
		#Quebra a lista quando encontrar as letras que representam as rotas
		posAtual = 0;
		rotalAtual = '';
		rotas = {}
		#Quebra o cromossomo nas rotas de cada caminhão
		while(len(cromossomo)!=0):
			if(not isinstance(cromossomo[posAtual],int)):
				rotalAtual = cromossomo.pop(posAtual);
				rotas[rotalAtual] = [];
			else:
				rotas[rotalAtual].append(cromossomo.pop(posAtual));
		#Calcula o Fitness total de cada rota, ou seja a distância total percorrida para ir de nó em nó
		TotalFit = 0
		for rotaID in rotas:
			rota = rotas[rotaID]
			#Como todas as rotas começam em 1 esta distância deve ser computada, porém não será considerada no cromossomo
			if(len(rota)>0):
				TotalFit= TotalFit + calcDist(1,rota[0],dicNodes)
			for i in range(len(rota)-1):
				TotalFit= TotalFit + calcDist(rota[i],rota[i+1],dicNodes)
			if(len(rota)>0):
				TotalFit= TotalFit + calcDist(rota[len(rota)-1],1,dicNodes)
		if(permiteSobrecarga):
			if(int(individuo['maxCarga'])>int(capacidade)):
				TotalFit = TotalFit + penalidadeSobrecarga*(int(individuo['maxCarga'])-int(capacidade)) 
		if(penalizaParada):
			TotalFit = TotalFit + calcPenalidadeParada(individuo,penalidadeParada)
		individuo['Fitness'] = TotalFit;
	listPopulacao = sorted(listPopulacao, key=lambda indiv: indiv['Fitness'])
	return listPopulacao

#Realiza a mutação no individuo selecionado
def perfMutacao(listPopulacao,dicDepo,dicNodes,capacidade,chanceMutacaoTrocaDeRota,permiteSobrecarga):
	listDepo = [];
	isInviavel = True;
	while(isInviavel):
		individuo = selectRoleta(listPopulacao)
		for depo in range(len(dicDepo)):
			listDepo.append(dicDepo[depo])
		individuoCrom = individuo['Crom'];
		#seleciona qual das operações de Mutação será executada de acordo com um valor aletório
		selectTipoMutacao = random.uniform(0,1);	
		selectNode = int(random.randint(0,len(individuoCrom)-1));
		selectDestRota = int(random.randint(0,len(individuoCrom)-1));
		while(selectNode==selectDestRota or not isinstance(individuoCrom[selectDestRota],int) or not isinstance(individuoCrom[selectNode],int) ):
			if(not isinstance(individuoCrom[selectDestRota],int)):
				selectDestRota = random.randint(0,len(individuoCrom)-1);
			elif(not isinstance(individuoCrom[selectNode],int)):
				selectNode = random.randint(0,len(individuoCrom)-1);
			else:
				selectNode = int(random.randint(0,len(individuoCrom)-1));
				selectDestRota = int(random.randint(0,len(individuoCrom)-1));
		#Seleciona mutação que troca o nó  de rota	
		if(selectTipoMutacao<=chanceMutacaoTrocaDeRota):
			 individuoCrom[selectDestRota], individuoCrom[selectNode] = individuoCrom[selectNode], individuoCrom[selectDestRota]
		#seleciona a mutação que troca o item de rota e adiciona o retorno a uma origem aleatória no seu lugar
		#se o nó selecionado for um retorno a origem ele apenas retira ele do cromossomo
		else:			
			if(individuoCrom[selectNode] in listDepo):
				individuoCrom.pop(selectNode);
			else:	
				node = individuoCrom[selectNode];				
				individuoCrom.insert(selectDestRota,node);
				depo = random.choice(listDepo);
				individuoCrom[selectNode] = depo
		individuo['maxCarga'] = calcCarga(individuoCrom,dicDepo,dicNodes)
		if(not permiteSobrecarga):
			if(int(individuo['maxCarga'])<int(capacidade)):				
				isInviavel = False;
		else:
			isInviavel = False;
		individuo['Crom'] = individuoCrom;
	return individuo

#Método que realiza o crossover de um ponto entre dois individuos
def perfCrossOver(listPopulacao,dicDepo,dicNodes,permiteSobrecarga,capacidade,numTrucks):	
	isInviavel = True;
	listNodes = [];
	for node in dicNodes:
		listNodes.append(int(node['Name']))
	letters = list(string.ascii_lowercase);
	for y in range(numTrucks):
		listNodes.append(letters[y])
	while(isInviavel):
		Indiv1 = selectRoleta(listPopulacao)
		Indiv2 = selectRoleta(listPopulacao)
		indOne = Indiv1.copy();
		indTwo = Indiv2.copy();		
		 
		#removendo os caminhões do cromossomo
		cromOne = list(indOne['Crom']);
		cromTwo = list(indTwo['Crom']);
		#Realizando o CrossOver chamado Order crossover (OX)
		selectNode1 = random.randint(1,len(indOne['Crom']));	
		#Quebra ambos os pais em um ponto aletório
		subCrom1_1 = cromOne[:selectNode1];		
		subCrom2_1 = cromTwo[:selectNode1];
		#Inicializa o novo cromossomo com parte de um dos pais
		novoCrom1 = subCrom1_1
		novoCrom2 = subCrom2_1
		#Completa o cromnossomo com os nós que ainda precisam ser atendidos
		#Na ordem que eles aparecem no segundo pai
		listFind1 = [];
		#print novoCrom1
		#print novoCrom2
		for node in listNodes:
			index =  findItem(novoCrom1,node)
			if(index == -1):
				indexCrom =  findItem(cromTwo,node)
				listFind1.append([indexCrom,node]);
		listFind1 = sorted(listFind1, key=lambda i: i[0]);
		for item in listFind1:
			novoCrom1.append(item[1]);
		listFind2 = [];
		for node in listNodes:
			index =  findItem(novoCrom2,node)
			if(index == -1):
				indexCrom =  findItem(cromOne,node)
				listFind2.append([indexCrom,node]);
		listFind2 = sorted(listFind2, key=lambda i: i[0]);
		for item in listFind2:
			novoCrom2.append(item[1]);
		novoIndv1 = {};
		novoIndv2 = {};
		novoIndv1['Crom'] = novoCrom1;		
		novoIndv2['Crom'] = novoCrom2
		#print novoCrom1
		#print novoCrom2
		novoIndv1['Fitness'] = 0 ;
		novoIndv1['maxCarga'] = calcCarga(novoIndv1['Crom'],dicDepo,dicNodes)
		novoIndv2['Fitness'] = 0 ;
		novoIndv2['maxCarga'] = calcCarga(novoIndv2['Crom'],dicDepo,dicNodes)
		#ind1vServTodos = checaServindoTodos(novoIndv1['Crom'],dicNodes) ;
		#ind2ServTodos = checaServindoTodos(novoIndv2['Crom'],dicNodes );
				
		#Se o sistema não permite sobrecarga ele gerara novos filhos até que seja possível
		if(not permiteSobrecarga):			
			listFilhos = [];
			if(int(novoIndv1['maxCarga'])<int(capacidade)):		
				#if(ind1vServTodos):		
				listFilhos.append(novoIndv1);
			if(int(novoIndv2['maxCarga'])<int(capacidade)):				
				listFilhos.append(novoIndv2);
			if(len(listFilhos)>0):
				return listFilhos;
		else:
			return novoIndv1,novoIndv2
	
#Retorna uma cópia do Individuo selecionado
def pefReproducao(listPopulacao):
	Indiv1 = selectRoleta(listPopulacao)
	return Indiv1.copy();

def checaServindoTodos(extCromossomo,dicNodes,):
	cromossomo = list(extCromossomo);
	posAtual = 0;
	posicoesTrucks1 = [];		
	while(len(cromossomo)>posAtual):
		if(not isinstance(cromossomo[posAtual],int)):
			posicoesTrucks1.append(cromossomo[posAtual]);
		posAtual = posAtual+1;
	posAtual = 0;		
	for i in posicoesTrucks1:
		cromossomo.remove(i);
	total = 0; 
	for node in dicNodes:
		if int(node['Name']) in cromossomo:
			total += 1;
	if(total!=len(dicNodes)):
		return False;
	else:
		print "serve Todos"
		return True;
	
#Seleciona um individuo utilizando o metodo Roleta
#Onde o menor Fitness tem melhores chances
def selectRoleta(listPopulacao):
	listFitness = [];
	for individuo in listPopulacao:
		listFitness.append(int(individuo['Fitness']));
	listProb = [];
	for fit in listFitness:
		listProb.append(1/float(fit));
	sumProb = sum(listProb)
	randomVal = random.uniform(0,sumProb)
	currentSum = 0;	
	selectedIndex = 0;
	for i in range(len(listProb)):
		currentSum = currentSum + listProb[i];		
		if(currentSum>=randomVal):
			selectedIndex = i;
			break;
	return listPopulacao[selectedIndex]

#Executa o Algoritmo genético
def ExecutaAlgortimoGenetico(inputFileName,numTrucks,numIndividuos,permiteSobrecarga,chanceRetDeposito,penalidadeSobrecarga,penalizaParada,penalidadeParada,chanceMutacaoTrocaDeRota,totalInteracoes,saveFile,saveFigure,numExp,filename,trocaTotal,indiceReproducao,indiceMutacao):
	capacidade = encontrarCapacidade(inputFileName);	
	dicNodes =  encontraCoordenadas(inputFileName);	
	dicNodes =  defineDemandas(inputFileName,dicNodes);
	dicDepo = encontraDepositos(inputFileName);
	listPopulacao = initPopulacao(dicNodes,dicDepo,permiteSobrecarga,numTrucks,capacidade,chanceRetDeposito,numIndividuos);
	listPopulacao = calcFitness(listPopulacao,dicNodes,permiteSobrecarga,capacidade,penalidadeSobrecarga,penalizaParada,penalidadeParada)
	intAtual = 0;
	#Lista para plotar a progressão do gráfico
	listMaxFitness =[];
	listStdFitness =[];
	listAvgFitness =[];
	listMelhorIndividuo = [];
	listIteracoes =[];
	listFistness = [];
	listNovaPopulacao = [];
	#Lista de Individuos no Ambiente
	listElite = [];	
	if(saveFile):
		f1 = preparaArquivo(numExp,filename,numTrucks,numIndividuos,permiteSobrecarga,chanceRetDeposito,penalidadeSobrecarga,penalizaParada,penalidadeParada,chanceMutacaoTrocaDeRota,totalInteracoes,indiceReproducao,indiceMutacao,trocaTotal);
	while(intAtual<totalInteracoes):
		print intAtual
		listNovaPopulacao = [];
		#Adiciona o Fitness do melhor indivuo a lista que será plotada
		listMaxFitness.append(listPopulacao[0]['Fitness']);			
		#Adiciona o melhor indivuo a lista que será mostrada ao usuário
		listMelhorIndividuo.append(listPopulacao[0]['Crom']);
		#salva os valores de Fitness médio e o valor da iteração atual em uma lista para ser mostrado no gráfico
		for indv in listPopulacao:
			listFistness.append(indv['Fitness']);
		listAvgFitness.append(statistics.mean(listFistness));
		listStdFitness.append(statistics.stdev(listFistness));
		listIteracoes.append(intAtual);
		#Escreve os dados em um arquivo
		if(saveFile):
			f1.write(str(intAtual)+'\t'+str(max(listFistness))+'\t'+str(statistics.mean(listFistness))+'\n')	
		for i in range(numIndividuos):			
			selectOp = random.random();
			#seleciona o operador genético a ser executad de acordo com as probabildades definidas
			if(selectOp<=indiceMutacao):
				#Realiza o operador de mutação e adiciona o individuo resultante na nova população
				listNovaPopulacao.append(perfMutacao(listPopulacao,dicDepo,dicNodes,capacidade,chanceMutacaoTrocaDeRota,permiteSobrecarga));
			elif(selectOp>indiceMutacao and selectOp<=indiceMutacao+indiceReproducao):
				#Realiza o operador de reprodução e adicina o individuo na nova população
				listNovaPopulacao.append(pefReproducao(listPopulacao));
			else:
				#Realiza o operador de crossOever e adicina os individuos na nova população
				novosIndividuos = perfCrossOver(listPopulacao,dicDepo,dicNodes,permiteSobrecarga,capacidade,numTrucks);				
				for indv in novosIndividuos:
					listNovaPopulacao.append(indv);
		if(trocaTotal):
			listNovaPopulacao = calcFitness(listNovaPopulacao,dicNodes,permiteSobrecarga,capacidade,penalidadeSobrecarga,penalizaParada,penalidadeParada)
			listPopulacao = listNovaPopulacao
		else:
			listComb = []
			#Combina as populações nova e Antiga
			listTotal = listNovaPopulacao+listPopulacao
			#Calcula e Ordena pelo Fitness da nova população
			listTotal = calcFitness(listTotal,dicNodes,permiteSobrecarga,capacidade,penalidadeSobrecarga,penalizaParada,penalidadeParada)
			#Retira os melhores individuos para manter o tamanho da população
			for i in range(numIndividuos):
				listComb.append(listTotal[i]);
			#define a nova população;
			listPopulacao = listComb;
			
		intAtual +=1;
		print listPopulacao[0]

		
	if(saveFile):
		f1.close();	
	#Se Salvar Figura esta habilitado gera a Figura
	if(saveFigure):
		plt.ioff();
		plt.plot(listIteracoes, listMaxFitness, 'r',  label='Max Fitness');
		plt.plot(listIteracoes, listAvgFitness, 'b', label='Avg Fitness');
		plt.plot(listIteracoes, listStdFitness,'g', label='Std Deviation Fitness');
		plt.legend(loc='best', shadow=True)
		figname = './OutPutFigures/'+'Exp_Func2_'+str(numExp)+'.png' ;
		plt.savefig(figname);
		plt.clf();
		plt.show();



