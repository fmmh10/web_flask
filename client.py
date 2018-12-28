#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 3
Grupo:
Números de aluno:
"""


import requests
import json
import shlex

def showUser(l, tipo = 1):
	if tipo == 1:
		print "Name: %s" % l[1]
		print "Username: %s" % l[2]
		print "Password: %s" % l[3]
	else:
		for i in l:
			print "Name: %s" % i[1]
			print "Username: %s" % i[2]
			print "Password: %s\n" % i[3]

def showEpisode(l, tipo = 1):
	if tipo == 1:
		print "Name: %s" % l[1]
		print "Description: %s" % l[2]
	else:
		for i in l:
			print "Name: %s" % i[1]
			print "Description: %s\n" % i[2]

def showSerie(l, tipo = 1):
	if tipo == 1:
		print "Name: %s" % l[1]
		print "Start_date: %s" % l[2]
		print "Synopse: %s" % l[3]
	else:
		for i in l:
			print "Name: %s" % i[1]
			print "Start_date: %s" % i[2]
			print "Synopse: %s\n" % i[3]

if __name__ == "__main__":
	req = requests.Session()
	while True:
		try:
			comando = raw_input('Comando ->')
			comando = shlex.split(comando)
			print comando

			if comando[0] == 'EXIT':
				exit()

			if comando[0] == 'ADD':
				if comando[1] == 'USER':
					r = req.put('http://localhost:5000/utilizadores', data=json.dumps({'name' : comando[2], 'username' : comando[3], 'password' : comando[4]})) 
					#FIX1: Em username tinha int(comando[3] mas o username pode uncuir letras)
					#FIX2: Tinha 'nome' em vez de 'name' o que originava um KeyError no server
					print r.status_code
					print r.content
				elif comando[1] == 'SERIE':
					print comando[2], comando[3], comando[4], comando[5]
					r = req.put('http://localhost:5000/series', data=json.dumps({'nome da serie' : comando[2], 'data de inicio' : comando[3], 'synopse' : comando[4], 'categoria' : comando[5]}))
					print r.status_code
					print r.content
				elif comando[1] == 'EPISODIO':
					print comando[3]
					r = req.put('http://localhost:5000/episodios', data=json.dumps({'nome do episodio' : comando[2], 'descricao' : comando[3], 'id da serie' : int(comando[4])}))
					print r.status_code
					print r.content
				elif comando[1].isdigit():
					r = req.post('http://localhost:5000/series', data=json.dumps({'id_user' : int(comando[1]), 'id da serie' : int(comando[2]), 'iniciais da classificacao' : comando[3]}))
					print r.status_code
					print r.content
				else:
					print "COMANDO ENVIADO INVALIDO"
			elif comando[0] == 'SHOW':
				if comando[1] == 'USER':
					r = req.get('http://localhost:5000/utilizadores/%s' % comando[2], data=json.dumps({'tipo' : 'user'}))
					print r.status_code
					res = json.loads(r.content)
					if r.status_code == 200:
						showUser(res)   #chama função para mostrar
					else:
						print res
				elif comando[1] == 'SERIE':
					r = req.get('http://localhost:5000/series/%s' % comando[2], data=json.dumps({'tipo' : 'serie'}))
					print r.status_code
					res = json.loads(r.content)
					showSerie(res)
				elif comando[1] == 'EPISODIO':
					r = req.get('http://localhost:5000/episodios/%s' % comando[2], data=json.dumps({'tipo' : 'episodio'}))
					print r.status_code
					res = json.loads(r.content)
					if r.status_code == 200:
						showEpisode(res)
					else:
						print res

				elif comando[1] == 'ALL':
					if comando[2] == 'SERIE':

						r = req.get('http://localhost:5000/series', data=json.dumps({'tipo' : 'series'}))
						print r.status_code
						res = json.loads(r.content)
						if r.status_code == 200:
							showSerie(res, 0)
						else:
							print res

					elif comando[2] == 'SERIE_U':
						r = req.get('http://localhost:5000/utilizadores/%s' % comando[4], data=json.dumps({'tipo' : 'serie'}))
						print r.status_code
						res = json.loads(r.content)
						if r.status_code == 200:
							showSerie(res, 0)
						else:

							print res
					elif comando[2] == 'SERIE_C':
						r = req.get('http://localhost:5000/series/%s' % comando[4], data=json.dumps({'tipo' : 'categoria'}))
						print r.status_code
						res = json.loads(r.content)
						if r.status_code == 200:
							showSerie(res, 0)
						else:
							print res

					elif comando[2] == 'USERS':
						r = req.get('http://localhost:5000/utilizadores', data=json.dumps({'tipo' : 'users'}))
						print r.status_code
						res = json.loads(r.content)
						if r.status_code == 200:
							showUser(res, 0)
						else:
							print res
					elif comando[2] == 'EPISODIO':
						if len(comando) == 3:
							r = req.get('http://localhost:5000/episodios', data=json.dumps({'tipo' : 'episodios'}))
							print r.status_code
							res = json.loads(r.content)
							if r.status_code == 200:
								showEpisode(res, 0)
							else:
								print res
						elif len(comando) == 4:
							r = req.get('http://localhost:5000/episodios/%s' % comando[3], data=json.dumps({'tipo' : 'serie'}))
							print r.status_code
							res = json.loads(r.content)
							if r.status_code == 200:
								showEpisode(res, 0)
							else:
								print res
					else:
						print "COMANDO ENVIADO INVALIDO"
				else:
					print "COMANDO ENVIADO INVALIDO"
			elif comando[0] == 'REMOVE':
				if comando[1] == 'USER':
					r = req.delete('http://localhost:5000/utilizadores/%s' % comando[2], data=json.dumps({'tipo' : 'user'}))
					print r.status_code
					print r.content
				elif comando[1] == 'SERIE':
					r = req.delete('http://localhost:5000/series/%s' % comando[2], data=json.dumps({'tipo' : 'serie'}))
					print r.status_code
					print r.content
				elif comando[1] == 'EPISODIO':
					r = req.delete('http://localhost:5000/episodios/%s' % comando[2], data=json.dumps({'tipo' : 'episodio'}))
					print r.status_code
					print r.content
				elif comando[1] == 'ALL':
					if comando[2] == 'USERS':
						if len(comando) == 3:
							r = req.delete('http://localhost:5000/utilizadores', data=json.dumps({'tipo' : 'utilizadores'}))
							print r.status_code
							print r.content

					elif comando[2] == 'SERIE':
						r = req.delete('http://localhost:5000/series', data=json.dumps({'tipo' : 'series'}))
						print r.status_code
						print r.content


					elif comando[3] == 'SERIE_U':
						r = req.delete('http://localhost:5000/utilizadores/%s' % comando[4], data=json.dumps({'tipo' : 'utilizadores'}))
						print r.status_code
						print r.content

					elif comando[3] == 'SERIE_C':
						r = req.delete('http://localhost:5000/series/%s' % comando[4], data=json.dumps({'tipo' : 'categoria'}))
						print r.status_code
						print r.content

					elif comando[2] == 'EPISODIO':
						if len(comando) == 3:
							r = req.delete('http://localhost:5000/episodios', data=json.dumps({'tipo' : 'episodios'}))
							print r.status_code
							print r.content
						elif len(comando) == 4:
							r = req.delete('http://localhost:5000/episodios/%s' % comando[3], data=json.dumps({'tipo' : 'serie'}))
							print r.status_code
							print r.content
					else:
						print "COMANDO ENVIADO INVALIDO"
				else:
					print "COMANDO ENVIADO INVALIDO"
			else:
				print "COMANDO ENVIADO INVALIDO"
		except ValueError:
			print "ARGUMENTOS ENVIADOS INVALIDOS"
		except IndexError:
			print "FALTAM ARGUMENTOS"
