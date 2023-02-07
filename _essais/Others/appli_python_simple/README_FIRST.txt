/***************************************************************************/
/*	INTERFACE GRAPHIQUE D'ACQUISITION DE DONNEES VIA NUCLEO            */
/*		Version simple / console			           */
/***************************************************************************/
/*	Développé par Julien VILLEMEJANE / LEnsE - IOGS - France           */
/*	Début de développement : 15/02/2020			           */
/***************************************************************************/
/* 	Nécessite une carte Nucléo de type L476RG 			   */
/*		et le programme fourni dans le répertoire		   */
/***************************************************************************/
/* 	Dépendances python :	python 3.7				   */
/*		- pyserial		(communication série)		   */
/***************************************************************************/
/*	Version 1.0				           		   */
/*		- Communication avec la carte testée			   */
/*		- envoi d'un 'a' pour allumer la LED			   */
/*		- envoi d'un 'e' pour allumer la LED			   */
/***************************************************************************/

Principe de communication entre le PC et la carte (via RS232 / USB)

	== PC ==				== Nucleo ==		
	init					init
	saisie port à utiliser			
	...					...
	envoie		------ 'a' ----->	attente 'a'
	attente 'o'	<----- 'o' ------	envoie	

	
	envoie		------ 'e' ----->	attente 'e'
	attente 'b'	<----- 'b' ------	envoie	


