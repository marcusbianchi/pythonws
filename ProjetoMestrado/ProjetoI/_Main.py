# -*- coding: utf-8 -*-
import GenAlgoritmImp; 	
#Número do Experimento
NumExp = 1;
#Número de Individuos
listNumIndividuos = [100];
#Parametros de Mutação, Reprodução
listExtIndiceMutacao = [0.05]#25];
listEextIndiceReproducao = [0.90]#25];
#Tipode CrossOver "Uniforme" ou "DoisPontos"
listTipoCrossOver = ["Uniforme","DoisPontos"];
#Indica a porcentagem de Elistismo na solução, sendo que 0 indica sem elistimo.
listPorcetagemElitismo = [0];
#Indica qual representação será usada "Real" ou "Binaria"
listTipoRepresentacao = [ 'Binaria','Real']
#Indica qual tipo de mutação será usada "Simples" ou "Multiplos"
listQtPontosMutacao = [1,2];
#Define o critério de Parada podendo ser  "NumGeracoes" ou o "LimFitness"
exCriterioParada = 'NumGeracoes'
exLimiteFitness = 300000;
exMaxInteracoes = 100;
#Calcula o Total de experimentos que serão executados
totalExperimentos = len(listNumIndividuos)*len(listTipoCrossOver)*len(listPorcetagemElitismo)*len(listTipoRepresentacao)*len(listQtPontosMutacao)*len(listExtIndiceMutacao)*len(listEextIndiceReproducao);
#Indicador se haverá troca total ou parcial
TrocaTotal = False;
#Equação que será utilizada para calcular o Fitness
eqNum = 4;

#Dimensão do vetor de individuos
ExD=30;
#Range de Valores para X
exMinEspaco = -500.0;
exMaxEspaco = 500.0;
#Inicia arquivo para gravação do experimento
finalFile=open('./FinalTest.txt', 'w')
#Escreve os cabeçalhos no arquivo
finalFile.write('Experimento'+'\t'+'Número de Individuos'+'\t'+'Indice de Mutação'+'\t'+'Indice de Reprodução'+'\t'+'Indice de Crossover'+'\t'+'Tipo de Crossover'+'\t'+'Procentagem de Elitismo'+'\t'+'Tipo de Representação'+'\t'+'Número de Pontos de Mutação'+'\t'+'Troca Total'+'\t'+'Fitness Máximo'+'\n')
	

#Itera entre todos os tipos de CrossOver definidos
for tipCros in listTipoCrossOver:
	#Itera entre todas as procentagens de elitismo
	for pocElit in listPorcetagemElitismo:
		#Itera entre todos os tipos de representação definidos
		for tipoRep in listTipoRepresentacao:
			#Itera entre todas as quantidades de pontos de mutação
			for qtPont in listQtPontosMutacao:
				#Itera entre todas as taxas de mutação
				for extIndiceMutacao in listExtIndiceMutacao:	
					#Itera entre todas as taxas de Reprodução
					for extIndiceReproducao in listEextIndiceReproducao:
						for numInv in listNumIndividuos:
							#Demonstra na tela os valores do experimento
							print str(NumExp)+' '+str(numInv)+' '+str(extIndiceMutacao)+' '+str(extIndiceReproducao)+' '+str(abs(extIndiceReproducao+extIndiceMutacao-1))+' '+tipCros+' '+str(pocElit)+' '+tipoRep+' '+str(qtPont) +' '+str(TrocaTotal);							
							resultParc = [];
							#Inicializa as variáveis do algortimo
							GenAlgoritmImp.inicVariaveis(NumExp,numInv,extIndiceMutacao,extIndiceReproducao,tipCros,pocElit,tipoRep,qtPont,exCriterioParada,exLimiteFitness,exMaxInteracoes,exMinEspaco,exMaxEspaco,ExD,TrocaTotal,eqNum);	
							#executa o Algortimo			
							resultParc.append(GenAlgoritmImp.excGenAlgor(False,True));							
							result = resultParc[0]['MaxFitness'];
							#Demonstra na tela os resultados do experimento
							print resultParc[0]['MaxFitness'];
							#Salva os resultados no arquivo
							finalFile.write(str(NumExp)+'\t'+str(numInv)+'\t'+str(extIndiceMutacao)+'\t'+str(extIndiceReproducao)+'\t'+str(abs(extIndiceReproducao+extIndiceMutacao-1))+'\t'+tipCros+'\t'+str(pocElit)+'\t'+tipoRep+'\t'+str(qtPont)+'\t'+str(TrocaTotal)+'\t'+str(result)+'\n')
							NumExp = NumExp + 1;

							
