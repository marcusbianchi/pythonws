# -*- coding: utf-8 -*-
import random;
import matplotlib
matplotlib.use('Agg')
from datetime import datetime;
import matplotlib.pyplot as plt;
import statistics;
from datetime import datetime
import math

#----------------------------------------------Atributos das Classe GenAlgoritmImpl-------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Número do Experimento
numExp = 1;
#Número de Individuos
numIndividuos = 10;
#Parametros de Mutação, Reprodução
indiceMutacao = 0.05;
indiceReproducao = 0.05;
#Tipode CrossOver "Uniforme" ou "DoisPontos"
tipoCrossOver = "DoisPontos";
#Indica a porcentagem de Elistismo na solução, sendo que 0 indica sem elistimo.
porcetagemElitismo = 00;
#Indica qual representação será usada "Real" ou "Binaria"
tipoRepresentacao = 'Binaria'
#Indica qual tipo de mutação será usada "Simples" ou "Multiplos"
qtPontosMutacao = 3;
#Define o critério de Parada podendo ser  "LimFitness" ou o "NumGeracoes"
criterioParada = 'NumGeracoes'
limiteFitness = 175000;
maxInteracoes = 100;
#Indica Troca Total de População (True) ou Troca Combinada (False)
TrocaTotal = True;
#Dimensão do vetor de individuos
D=30;
#Range de Valores para X
minEspaco = -100;
maxEspaco = 100;
eqNum = 2
#Fator de Correção para decimal
FatordeCorrecao = 100

#------------------------------------------------------------Inicializa variáveis-------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
def inicVariaveis(exp,numInv,extIndiceMutacao,extIndiceReproducao,tipCros,pocElit,tipoRep,qtPont,exCriterioParada,exLimiteFitness,exMaxInteracoes,exMinEspaco,exMaxEspaco,ExDD,exTrocaTotal,exEquacaoNumero):
	global numExp;
	global numIndividuos;
	global indiceMutacao;
	global indiceReproducao;
	global tipoCrossOver;
	global porcetagemElitismo;
	global tipoRepresentacao;	
	global qtPontosMutacao;
	global criterioParada;
	global limiteFitness;
	global maxInteracoes;
	global TrocaTotal;
	global D;
	global minEspaco;
	global maxEspaco;
	global eqNum
	numExp = exp;
	numIndividuos = numInv;
	indiceMutacao = extIndiceMutacao;
	indiceReproducao = extIndiceReproducao;
	tipoCrossOver = tipCros;
	porcetagemElitismo = pocElit;
	tipoRepresentacao = tipoRep;	
	qtPontosMutacao = qtPont;
	criterioParada = exCriterioParada;
	limiteFitness = exLimiteFitness;
	maxInteracoes = exMaxInteracoes;
	D=ExDD;
	minEspaco = exMinEspaco*FatordeCorrecao;
	maxEspaco = exMaxEspaco*FatordeCorrecao;
	TrocaTotal = exTrocaTotal;
	eqNum = exEquacaoNumero	
	
#Método que prepara a escrito do arquivo.	
def preparaArquivo():
	#Abre o arquivo para salvar os dados;
	filename =  'Exp_Func2'+str(numExp);
	f1=open('./OutPutFiles/'+filename+'.txt', 'w')
	if(criterioParada == 'NumGeracoes'):
		f1.write('Critério de Parada'+'\t'+criterioParada+'\n')	
		f1.write('Máximo de Gerações'+'\t'+str(maxInteracoes)+'\n')
	else:
		f1.write('Critério de Parada'+'\t'+criterioParada+'\n')	
		f1.write('Limite de Fitness'+'\t'+str(limiteFitness)+'\n')
	f1.write('Número de Individuos'+'\t'+'Indice de Mutação'+'\t'+'Indice de Reprodução'+'\t'+'Indice de Crossover'+'\t'+'Tipo de Crossover'+'\t'+'Procentagem de Elitismo'+'\t'+'Tipo de Representação'+'\t'+'Número de Pontos de Mutação'+'\n')
	
	f1.write(str(numIndividuos)+'\t'+str(indiceMutacao)+'\t'+str(indiceReproducao)+'\t'+str(abs(indiceReproducao+indiceMutacao-1))+'\t'+tipoCrossOver+'\t'+str(porcetagemElitismo)+'\t'+tipoRepresentacao+'\t'+str(qtPontosMutacao)+'\n')		
	return f1;

#--------------------------------------------------Métodos Auxiliares--------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

#Método auxiliar para conversão de Inteiro para Array de Binários de tamanho Fixo 8 sendo que o primeiro bit indica o sinal
def inteiroParaArrayBits(valor):
	valorInt = int(abs(valor))
	valorConvertido ='{0:b}'.format(int(abs(valor)))
	valorTrim = valorConvertido.replace(" ", "")
	teste = False;
	while(len(valorTrim)!=16):
		valorTrim = '0'+valorTrim		
	if(valor>0):
		valorTrim="0"+valorTrim
	else:
		valorTrim="1"+valorTrim
	return list(valorTrim);

#Método auxiliar para conversão de Array de Binários para inteiro o tamanho Fixo 8 sendo que o primeiro bit indica o sinal
def arrayBitsParaInteiro(valor):	
	valorString= ''.join(valor);
	valorConvertido = int(valorString[1:],2)
	if(valor[0]=="0"):
		valorConvertido=valorConvertido
	else:
		valorConvertido=-valorConvertido	
	return valorConvertido;

		
#Método para a quebra do cromossomo quandome representação binária
def splitList(list):
	inicio = 0;
	fim = inicio + 17;
	splitedList = [];
	while(fim<=len(list)):
		splitedList.append(list[inicio:fim]);
		inicio = fim;
		fim = inicio + 17;
	return splitedList;
	
#--------------------------------------------------Métodos para Operadores Genéticos---------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------



def inicPopulacao(listIndividuos):
	#Cada Individuo na Lista será representado por um par [Crom:valor,Fit:valor]
	#Onde Crom é uma lista de 30 valores aleatórios  entre minEspaço e MaxEspaço
	for i in range(numIndividuos):
		Crom =[];
		for j in range(D):			
			randomGen = random.uniform(minEspaco, maxEspaco) ;		
			if(tipoRepresentacao == "Binaria"):
				randomNum = inteiroParaArrayBits(randomGen);	
				for number in randomNum:
					Crom.append(number);
			else:
				randomNum = randomGen;
				Crom.append(randomNum);
		individuo={'Crom':Crom,'Fit':0.0};
		listIndividuos.append(individuo);		
	return listIndividuos;

#Definindo a funçãoFitness que será utilizada
def calcFitness(listIndividuos):	
	for ind in listIndividuos:
		fit = 0.0;
		#Calcula o Fitness na representação Binária 
		if(tipoRepresentacao == "Binaria"):
			#Pega o cromossomo do inviduo
			cromList = ind['Crom'];			
			#Divide o cromossomo em tamanhos iguais para conversão binária
			valuesCrom = splitList(cromList);
			#Calcula o Fitness para cada valor encontrado			
			#utilizando a equação 1
			if(eqNum==1):				
				convHelper = [];				
				for value in valuesCrom:					
					valueConv = arrayBitsParaInteiro(value);					
					valueConv = valueConv/float(FatordeCorrecao);
					convHelper.append(valueConv);
				x = (convHelper[0]);
				y = (convHelper[1]);	
				zx = x**2 - 10 * math.cos(2*math.pi*x)+10;
				zy = y**2 - 10 * math.cos(2*math.pi*y)+10;
				z = zx+zy
				fit = - z;
			else:				
				for value in valuesCrom:					
					valueConv = arrayBitsParaInteiro(value);					
					valueConv = valueConv/float(FatordeCorrecao);	
					#utilizando a equação 2					
					if(eqNum==2):					
						fit = fit + (valueConv)**2;
					#utilizando a equação 3				
					if(eqNum==3):
						fit = fit + (abs(valueConv+0.5))**2;
					if(eqNum==4):
					#utilizando a equação 4					
						fit = fit - math.sin(math.sqrt(abs(valueConv)));						
		else:
			#utilizando a equação 1					
			if(eqNum==1):				
				x = ind['Crom'][0]/(FatordeCorrecao);			
				y = ind['Crom'][1]/(FatordeCorrecao);				
				zx = x**2 - 10 * math.cos(2*math.pi*x)+10;
				zy = y**2 - 10 * math.cos(2*math.pi*y)+10;
				z = zx+zy
				fit = - z;
			else:
				for value in ind['Crom']:	
					value = (value/FatordeCorrecao)
					#utilizando a equação 2
					if(eqNum==2):
						fit = fit + value**2;
					#utilizando a equação 3					
					if(eqNum==3):								
						fit = fit + (abs(value+0.5))**2;
					#utilizando a equação 4		
					if(eqNum==4):					
						fit = fit - math.sin(math.sqrt(abs(value)));
		ind['Fit'] = fit;
	#Ordena a lista de Individuos pelos Fitness Crescente	
	listIndividuos = sorted(listIndividuos, key=lambda indiv: indiv['Fit'])
	return listIndividuos;
	
#Calcula se o Individuo resultado da operação genética é viável de acordo com as condições de contorno definidas
#True Indica Inviável e False Indica viável
def calcViabilidade(Individuo):
	if(tipoRepresentacao == 'Binaria'):
		#Pega o cromossomo do inviduo
		cromList = Individuo['Crom'];
		#Divide o cromossomo em tamanhos iguais para conversão binária
		valuesCrom = splitList(cromList);
		#verifica se nenhum valor dentro do cromossomo ultrapassou os limiares, tornado-o inviável
		for value in valuesCrom:
			valueConv = arrayBitsParaInteiro(value);	
			if(valueConv>maxEspaco or valueConv<minEspaco):
				return True;
		return False;
	else:
		return False;

#Retorna o Individuo escolhido através do método roleta
def RetornIndvRoleta(listIndividuos):
	#Quando existe a possibilidade de Fitness negativo é necessário fazer um deslocamento em janela
	#Ou seja, Soma-se a todos os valores de Fitness o Módulo do menor valor de Fitness
	#Isso faz com que 0 seja novamente o número mais a esquerda permitindo assim a seleção em roleta
	minimumFit =  min(listIndividuos, key=lambda indiv: indiv['Fit'])['Fit']
	if(minimumFit<0):
		for individuo in listIndividuos:
			individuo['Fit'] = individuo['Fit'] + abs(minimumFit)
	totalFit  = 0
	for individuo in listIndividuos:
		totalFit = totalFit + individuo['Fit'];
	selectVal  = random.uniform(0, totalFit);
	totalFit=0;
	for indiv in listIndividuos:
		totalFit = totalFit + indiv['Fit'];
		if(totalFit>=selectVal):
			return indiv;

#Define o operador de mutação simples	
def perfMutacao(listIndividuos):	
	inViavel = True;
	#Executa o loop até que seja gerado um individuo viável para as condicoes de contorno
	while(inViavel):
		if(qtPontosMutacao == 1):
			#seleciona o individuo de acordo com a roleta
			selectedIndv = RetornIndvRoleta(listIndividuos);
			#seleciona um valor aleatório dentro do cromossomo e altera seu valor para um valor dentro dos possíveis
			#ou seja uma mutação simples em um único gene do cromossomo
			selecId = random.randint(0, D-1);	
			if(tipoRepresentacao == "Binaria"):
				value = '';
				if(bool(random.getrandbits(1))):
					value = '1'
				else:
					value = '0'
				selectedIndv['Crom'][selecId] = value;
			else:
				selectedIndv['Crom'][selecId] = random.uniform(minEspaco, maxEspaco) ;
		else:
			#seleciona o individuo de acordo com a roleta
			selectedIndv = RetornIndvRoleta(listIndividuos);		
			if(tipoRepresentacao == "Binaria"):
				#Executa a operação de mutação em multiplos pontos
				for i in range(qtPontosMutacao): 
					#seleciona um valor aleatório dentro do cromossomo e altera seu valor para um valor dentro dos possíveis
					#ou seja uma mutação simples em um único gene do cromossomo
					selecId = random.randint(0, D-1);	
					value = '';
					if(bool(random.getrandbits(1))):
						value = '1'
					else:
						value = '0'
					selectedIndv['Crom'][selecId] = value;
			else:
				#Executa a operação de mutação em multiplos pontos
				for i in range(qtPontosMutacao): 
					#seleciona um valor aleatório dentro do cromossomo e altera seu valor para um valor dentro dos possíveis
					#ou seja uma mutação simples em um único gene do cromossomo
					selecId = random.randint(0, D-1);	
					selectedIndv['Crom'][selecId] = random.uniform(minEspaco, maxEspaco) ;
		#Calcula a Viabilidade do Individuo
		inViavel = calcViabilidade(selectedIndv);

	return selectedIndv;

#Define o operador de reproduçao
def perfReproducao(listIndividuos):
	#seleciona o individuo de acordo com a roleta
	selectedIndv = RetornIndvRoleta(listIndividuos);
	return selectedIndv;

#define o operador de CrossOver
def perfCrossOver(listIndividuos):
	inViavel = True;
	#Executa o loop até que seja gerado um individuo viável para as condicoes de contorno
	result = [];
	while(len(result)==0):
		#seleciona o individuo 1 de acordo com a roleta
		selectedIndv1 = RetornIndvRoleta(listIndividuos);
		#seleciona o individuo 2 de acordo com a roleta
		selectedIndv2 = RetornIndvRoleta(listIndividuos);	
		if(tipoCrossOver=="Uniforme"):
			#Seleciona o ponto de CrossOever
			selectCrossPoint = random.randint(0,len(selectedIndv1['Crom']));
			subCrom1_1 = selectedIndv1['Crom'][:selectCrossPoint];
			subCrom1_2 = selectedIndv1['Crom'][selectCrossPoint:];
			subCrom2_1 = selectedIndv2['Crom'][selectCrossPoint:];
			subCrom2_2 = selectedIndv2['Crom'][:selectCrossPoint];
			novoIndividuo1={'Crom':subCrom1_1+subCrom2_1,'Fit':0.0};
			novoIndividuo2={'Crom':subCrom1_2+subCrom2_2,'Fit':0.0};
		else:
			#CrossOver de Dois Pontos
			selectCrossPoint1 = random.randint(0,len(selectedIndv1['Crom']));
			selectCrossPoint2 = random.randint(selectCrossPoint1,len(selectedIndv1['Crom']));
			subCrom1_1 = selectedIndv1['Crom'][:selectCrossPoint1];
			subCrom1_2 = selectedIndv1['Crom'][selectCrossPoint2:];
			subCrom1 = selectedIndv1['Crom'][selectCrossPoint1:selectCrossPoint2];
			subCrom2 = selectedIndv2['Crom'][selectCrossPoint1:selectCrossPoint2];
			subCrom2_1 = selectedIndv2['Crom'][:selectCrossPoint1];
			subCrom2_2 = selectedIndv2['Crom'][selectCrossPoint2:];
			novoIndividuo1={'Crom':subCrom1_1+subCrom2+subCrom1_2,'Fit':0.0};
			novoIndividuo2={'Crom':subCrom2_1+subCrom1+subCrom2_2,'Fit':0.0};
		#Calcula a Viabilidade dos Individuos
		inViavel1 = calcViabilidade(novoIndividuo1);
		inViavel2 = calcViabilidade(novoIndividuo2);
		if(inViavel1==False):			
			result.append(novoIndividuo1)
		if(inViavel2==False):
			result.append(novoIndividuo2)	
		
	return result;


#Define se deve haver uma nova execução (True) ou não  (False)
def calcCriterioParada(intAtual,listMaxFitness):	
	if(criterioParada == 'NumGeracoes'):
		return (maxInteracoes>intAtual)
	else:		
		if(len(listMaxFitness)==0):
			return True;
		else: 
			#print listMaxFitness[len(listMaxFitness)-1]
			return (limiteFitness>listMaxFitness[len(listMaxFitness)-1] and 500>intAtual)

#Executa algoritmo genético indicando se deve ser salvado um arquivo e se devem ser geradas figuras
def excGenAlgor(saveFile,saveFigure):
	#Inicializa Interação atual
	intAtual = 1;
	
	#Lista para plotar a progressão do gráfico
	listMaxFitness =[];
	listStdFitness =[];
	listAvgFitness =[];
	listMelhorIndividuo = [];
	listIteracoes =[];
	listFistness = [];
	listNovaPopulacao = [];
	#Lista de Individuos no Ambiente
	listIndividuos = [];
	listElite = [];	
	if(saveFile):
		f1 = preparaArquivo();
	listIndividuos = inicPopulacao(listIndividuos);
	#Define a quantidade de Individuos na elite
	qtdElite = round(porcetagemElitismo * len(listIndividuos));
	qtdElite = int(round(qtdElite));	
	

	#Verifica Critério de Parada
	while(calcCriterioParada(intAtual,listMaxFitness)):	
		print intAtual;
		#Calula o Fitness de cada Individuo através da função Fitness
		listIndividuos = calcFitness(listIndividuos);
		#Adiciona o Fitness do melhor indivuo a lista que será plotada
		listMaxFitness.append(listIndividuos[len(listIndividuos)-1]['Fit']);
		#print listIndividuos[len(listIndividuos)-1]['Fit']
		#Adiciona o melhor indivuo a lista que será mostrada ao usuário
		listMelhorIndividuo.append(listIndividuos[len(listIndividuos)-1]['Crom']);
		#Gera uma lista do fitness de todos os individuos
		for indv in listIndividuos:
			listFistness.append(indv['Fit']);	
		#salva os valores de Fitness médio e o valor da iteração atual em uma lista para ser mostrado no gráfico
		listAvgFitness.append(statistics.mean(listFistness));
		listStdFitness.append(statistics.stdev(listFistness));
		listIteracoes.append(intAtual);
		#Escreve os dados em um arquivo
		if(saveFile):
			f1.write(str(intAtual)+'\t'+str(max(listFistness))+'\t'+str(statistics.mean(listFistness))+'\n')	
		#Gera uma nova população de acordo com os operadores genéticos	
		listNovaPopulacao = [];	
		listElite = [];				
		#Preenche a lista com a Elite considerado que a Lista de Individuos já esta ordenada pelo Fitness os maiores estando no final
		if(TrocaTotal):
			for j in range(qtdElite):
				listElite.append(listIndividuos[-j])
			#Preenche a lista de manutenção que retirá os piores da nova geração		
			while(len(listNovaPopulacao)<numIndividuos-qtdElite):
				selectOp = random.random();
				#seleciona o operador genético a ser executad de acordo com as probabildades definidas
				if(selectOp<=indiceMutacao):
					#Realiza o operador de mutação e adiciona o individuo resultante na nova população
					listNovaPopulacao.append(perfMutacao(listIndividuos));
				elif(selectOp>indiceMutacao and selectOp<=indiceMutacao+indiceReproducao):
					#Realiza o operador de reprodução e adicina o individuo na nova população
					listNovaPopulacao.append(perfReproducao(listIndividuos));
				else:
					#Realiza o operador de crossOever e adicina os individuos na nova população
					novosIndividuos = perfCrossOver(listIndividuos);				
					for indv in novosIndividuos:
						listNovaPopulacao.append(indv);
			#Conbina a população gerada pelos métodos genéticos com a elite
			listIndividuos = listElite+ listNovaPopulacao;
		else:
			listComb = []
			while(len(listNovaPopulacao)<numIndividuos):
				selectOp = random.random();
				#seleciona o operador genético a ser executad de acordo com as probabildades definidas
				if(selectOp<=indiceMutacao):
					#Realiza o operador de mutação e adiciona o individuo resultante na nova população
					listNovaPopulacao.append(perfMutacao(listIndividuos));
				elif(selectOp>indiceMutacao and selectOp<=indiceMutacao+indiceReproducao):
					#Realiza o operador de reprodução e adicina o individuo na nova população
					listNovaPopulacao.append(perfReproducao(listIndividuos));
				else:
					#Realiza o operador de crossOever e adicina os individuos na nova população
					novosIndividuos = perfCrossOver(listIndividuos);				
					for indv in novosIndividuos:
						listNovaPopulacao.append(indv);
			#Combina as populações nova e Antiga
			listTotal = listNovaPopulacao+listIndividuos
			#Calcula e Ordena pelo Fitness da nova população
			listTotal = calcFitness(listTotal);
			#Retira os melhores individuos para manter o tamanho da população
			for i in range(numIndividuos):
				listComb.append(listTotal[-i]);
			#define a nova população;
			listIndividuos = listComb;
		
		intAtual = intAtual + 1;

	#calcula o Fitness dos individuos da última geração
	listIndividuos = calcFitness(listIndividuos);
	#Retorna o maior valor de Fitness após um determinado número de interações
	#print 'Melhor Fitness: ' + str(listMaxFitness[len(listMaxFitness)-1])

	#Retorna o valor de Fitness para este X
	#print 'Melhor valor de X:' + str(listMelhorIndividuo[len(listMelhorIndividuo)-1])

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
	MelhorResultado={'MaxFitness':listMaxFitness[len(listMaxFitness)-1],'Interacoes':intAtual};		
	return MelhorResultado;

		

