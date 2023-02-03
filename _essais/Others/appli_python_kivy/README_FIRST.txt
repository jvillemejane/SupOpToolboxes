/***************************************************************************/
/*	INTERFACE GRAPHIQUE D'ACQUISITION DE DONNEES VIA NUCLEO            */
/***************************************************************************/
/*	Développé par Julien VILLEMEJANE / LEnsE - IOGS - France           */
/*	Début de développement : 15/10/2020			           */
/***************************************************************************/
/* 	Nécessite une carte Nucléo de type L476RG 			   */
/*		et le programme suivant  :				   */
/* 	https://os.mbed.com/users/villemejane/code/PrV_Acquisition/  	   */
/***************************************************************************/
/* 	Dépendances python :	python 3.7				   */
/*		- kivy			(interface graphique)		   */
/*		- pyserial		(communication série)		   */
/***************************************************************************/
/*	Version 0.1	/ non finalisée		           		   */
/*		- Interface graphique fonctionnelle			   */
/*		- Communication avec la carte testée			   */
/***************************************************************************/
/*	TO DO
/*		- Implémenter l'ensemble des fonctionnalités de communication
/*		- Tester l'affichage des données sous forme graphique
/*		- Implémenter test sur valeur maximale Fe
/*		- Côté Nucléo : implémenter synchronisation
/***************************************************************************/

Principe de communication entre le PC et la carte (via RS232 / USB)

	== PC ==				== Nucleo ==		Etat
	init					init			ETAT_STOP
	...					...
	envoie		------ 'a' ----->	attente 'a'
	attente 'o'	<----- 'o' ------	envoie			ETAT_WAIT_PARAM		Attente des paramètres 
	envoie paramètres
	envoie		------ 'n' ----->	attente 'n'		ETAT_WAIT_PARAM_N	Nombre de points à acquérir
	attente 'n'	<----- 'n' ------	envoie	
	envoie		------ '1' ----->	attente chiffre
	envoie		------ '0' ----->	attente chiffre
	envoie		------ 'f' ----->	si f			ETAT_WAIT_PARAM_F	Fréquence d'échantillonnage
	attente 'f'	<----- 'f' ------	envoie	
	envoie		------ '1' ----->	attente chiffre
	envoie		------ '0' ----->	attente chiffre
	envoie		------ 's' ----->	si s			ETAT_WAIT_PARAM_S	Synchronisation
	attente 'f'	<----- 's' ------	envoie
	envoie		----- '0/1' ---->	attente (0 ou 1)	ETAT_WAIT_GO		Attente de lancement de l'acquisition
	envoie		------ 'G' ----->	attente 'G'		ETAT_ACQUIRING		Acquisition en cours
						acquisition
	attente 'd'	<----- 'd' ------	envoie			ETAT_SENDING_DATA
	attente données
			<-- "[0;d[0]]" --	envoie data/data
			<-- "[1;d[1]]" --	envoie data/data
			<-- "[i;d[i]]" --	envoie data/data
	
	fin de données							ETAT_STOP
		


