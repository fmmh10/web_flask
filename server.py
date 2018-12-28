#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 4
Grupo: 11
Números de aluno: 39034, 45795, 32169
"""


import sqlite3
from os.path import isfile
from flask import Flask, make_response, request
import json

app = Flask(__name__)
def connect(db_name):
	db_exists = isfile(db_name)
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()

	if not db_exists:
		f = open('bd.sql', 'r')
		cursor.executescript(f.read())
		connection.commit()
	else:
		cursor.execute("PRAGMA foreign_keys = ON;")
	return connection, cursor
#------------------------------------------------ UTILIZADORES #
@app.route('/utilizadores', methods=['PUT', 'GET', 'DELETE'])
@app.route('/utilizadores/<int:id>', methods=['GET', 'DELETE'])
def utilizadores(id = None):
	conn, cursor = connect('bd.db')
	data = json.loads(request.data)
	if request.method == 'PUT':
		print 'next'
		print cursor.execute("PRAGMA foreign_keys")
		sql = 'INSERT INTO users VALUES (?,?,?,?)'
		cursor.execute(sql, [None, data['name'], data['username'], data['password']])
		conn.commit()
		cursor.execute(GET_LAST_ID_SQL + 'users')
		id_utilizador = cursor.fetchone()[0]
		r = make_response('utilizador %s adicionado' % data['name'])
		r.status_code = CREATED
		r.headers['location'] = '/utilizadores/%d' % id_utilizador
	if request.method == 'GET':
		code = OK
		if data['tipo'] == 'user':
			sql = 'SELECT * FROM users WHERE id = %d' % id
			cursor.execute(sql)
			resp = cursor.fetchone()
			if resp == None:
				resp = 'Nao existe um utilizador com o id %d' % id
				code = NOK
		elif data['tipo'] == 'episodio':
			sql = 'SELECT DISTINCT users.* FROM users, list_series WHERE list_series.id_episodio = %d AND list_series.id_utilizador = utilizadores.id' % id
			cursor.execute(sql)
			resp = cursor.fetchall()
		elif data['tipo'] == 'serie':
			sql = 'SELECT DISTINCT users.* FROM users, list_series, episode WHERE list_series.id_episodio = episodio.id AND episodio.id_serie = %d AND utilizadores.id = list_series.id_utilizador' % id
			cursor.execute(sql)
			resp = cursor.fetchall()
		elif data['tipo'] == 'users':
			sql = 'SELECT * FROM users'
			cursor.execute(sql)
			resp = cursor.fetchall()
			if resp == []:
				resp = 'Nao existe utilizadores'
				code = NOK
		elif data['tipo'] == 'utilizador_inscri':
			sql = 'SELECT * FROM list_series WHERE id_utilizador = %s AND id_episodio = %s' % (data['id_utilizador'], id)
			cursor.execute(sql)
			resp = cursor.fetchone()
			if resp == None:
				resp = 'Nao existe essa inscricao'
				code = NOK
		if resp == []:
			resp = 'Nao tem ninguem inscrito'
			code = NOK
		r = make_response(json.dumps(resp))
		r.status_code = code
	if request.method == 'DELETE':
		if data['tipo'] == 'user':
			sql = 'DELETE FROM users WHERE id = %d' % id
			N = cursor.execute(sql).rowcount
			if N != 0:
				conn.commit()
				r = make_response('utilizador %d foi removido' % id)
				r.status_code = OK
			else:
				r = make_response('Nao existe um utilizador com o id %d' % id)
				r.status_code = NOK
		elif data['tipo'] == 'utilizadores':
			sql = 'DELETE FROM users'
			cursor.execute(sql)
			conn.commit()
			r = make_response('utilizadores removidos')
			r.status_code = OK
		elif data['tipo'] == 'episodio':
			sql = 'DELETE FROM list_series WHERE id_episodio = %d' % id
			N = cursor.execute(sql).rowcount
			if N != 0:
				conn.commit()
				r = make_response('utilizadores removidos da episodio %d' % id)
				r.status_code = OK
			else:
				r = make_response('Nao existe utilizadores inscritos na episodio %d' % id)
				r.status_code = NOK
		elif data['tipo'] == 'serie':
			sql = 'SELECT DISTINCT episodio.id FROM users, list_series, episode WHERE list_series.id_episodio = episodio.id AND episodio.id_serie = %d AND utilizadores.id = list_series.id_utilizador' % id
			cursor.execute(sql)
			quer = cursor.fetchall()
			sql = 'DELETE FROM list_series WHERE id_episodio = ?'
			N = cursor.executemany(sql, quer).rowcount
			if N != 0:
				conn.commit()
				r = make_response('utilizadores removidos da serie %d' % id)
				r.status_code = OK
			else:
				r = make_response('Nao existe utilizadores inscritos na serie %d' % id)
				r.status_code = NOK
		elif data['tipo'] == 'utilizador_inscri':
			id_utilizador = int(data['id_utilizador'])
			sql = 'DELETE FROM list_series WHERE id_utilizador = %d AND id_episodio = %s' % (id_utilizador, id)
			N = cursor.execute(sql).rowcount
			if N != 0:
				conn.commit()
				r = make_response('utilizador %d removido' % id_utilizador)
				r.status_code = OK
			else:
				r = make_response('Ocorreu um erro, invalida episodio ou utilizador')
				r.status_code = NOK
	return r

#------------------------------------------------ SERIES #
@app.route('/series', methods=['PUT', 'GET', 'DELETE', 'POST'])
@app.route('/series/<int:id>', methods=['GET', 'DELETE'])
def series(id = None):
	conn,cursor = connect('bd.db')
	data = json.loads(request.data)
	if request.method == 'PUT':
		sql = 'INSERT INTO serie VALUES (?,?,?,?,?)'
		cursor.execute(sql, [None, data['nome da serie'], data['data de inicio'], data['synopse'], data['categoria']])
		conn.commit()
		cursor.execute(GET_LAST_ID_SQL + 'serie')
		id_serie = cursor.fetchone()[0]
		r = make_response('serie adicionada')
		r.status_code = CREATED
		r.headers['location'] = '/series/%d' % id_serie
	if request.method == 'POST':
		try:
			#id_class =

			cursor.execute('SELECT * FROM classification')
			print cursor.fetchall()

			sql = 'INSERT INTO list_series VALUES (?,?,?)'
			try:
				cursor.execute(sql, [data['id_user'], data['id da serie'], data['iniciais da classificacao']])
			except Exception as e:
				print e
			conn.commit()
			r = make_response('classificacao %s adicionada a serie %s' % (data['iniciais da classificacao'], data['id da serie']))
			r.status_code = OK
		except:
			cursor.execute('SELECT * FROM users where id = %s' % data['id_user'])
			f = cursor.fetchone()
			cursor.execute('SELECT * FROM episode where id = %s' % data['id da serie'])
			f2 = cursor.fetchone()
			if f == None or f2 == None:
				r = make_response('Nao existe o id da episodio ou do utilizador')
			else:
				r = make_response('Iniciais da classificação erradas')
			r.status_code = NOK
	if request.method == 'GET':
		code = OK
		if data['tipo'] == 'serie':
			sql = 'SELECT * FROM serie WHERE id = %d' % id
			cursor.execute(sql)
			resp = cursor.fetchone()
		elif data['tipo'] == 'series':
			sql = 'SELECT * FROM serie'
			cursor.execute(sql)
			resp = cursor.fetchall()

		if resp == None:
			resp = 'Nao existe nenhuma serie com o id %d' % id
			code = NOK
		elif resp == []:
			resp = 'Nao existem series'
			code = NOK
		r = make_response(json.dumps(resp))
		r.status_code = code
	if request.method == 'DELETE':
		if data['tipo'] == 'serie':
			sql = 'DELETE FROM serie WHERE id = %d' % id
			N = cursor.execute(sql).rowcount
			if N != 0:
				conn.commit()
				r = make_response('serie %d removida' % id)
				r.status_code = OK
			else:
				r = make_response('Nao existe uma serie com id %d' % id)
				r.status_code = NOK
		elif data['tipo'] == 'series':
			sql = 'DELETE FROM serie'
			cursor.execute(sql)
			conn.commit()
			r = make_response('series removidas')
	return r

#------------------------------------------------ EPISODIOS #
@app.route('/episodios', methods=['PUT', 'GET', 'DELETE'])
@app.route('/episodios/<int:id>', methods=['GET', 'DELETE'])
def episodios(id=None):
	conn,cursor = connect('bd.db')
	data = json.loads(request.data)
	print data
	if request.method == 'PUT':
		try:
			data = json.loads(request.data)
			sql = 'INSERT INTO episode VALUES (?,?,?,?)'
			cursor.execute(sql, [None, data['nome do episodio'], data['descricao'], data['id da serie']])
			conn.commit()
			cursor.execute(GET_LAST_ID_SQL + 'episode')
			id_episodio = cursor.fetchone()[0]
			r = make_response('Episodio adicionado')
			r.status_code = CREATED
			r.headers['location'] = '/episodios/%d' % id_episodio
		except:
			r = make_response('Nao existe uma serie com esse id')
			r.status_code = NOK

	if request.method == 'GET':
		code = OK
		if data['tipo'] == 'episodio':
			sql = 'SELECT * FROM episode WHERE id = %d' % id
			cursor.execute(sql)
			resp = cursor.fetchone()
			if resp == None:
				resp = 'Nao existe uma episodio com id %d' % id
				code = NOK
		elif data['tipo'] == 'serie':
			try:
				sql = 'SELECT * FROM episode WHERE serie_id = %d' % id
				cursor.execute(sql)
				resp = cursor.fetchall()
				if resp == []:
					resp = 'Nao existe episodios associadas a serie %d' % id
					code = NOK
			except:
				resp = 'Nao existe uma serie com id %d' % id
				code = NOK

		elif data['tipo'] == 'episodios':
			sql = 'SELECT * FROM episode'
			cursor.execute(sql)
			resp = cursor.fetchall()
			if resp == []:
				resp = 'Nao existe episodios'
				code = NOK
		r = make_response(json.dumps(resp))
		r.status_code = code

	if request.method == 'DELETE':
		if data['tipo'] == 'episodio':
			sql = 'DELETE FROM episode WHERE id = %d' % id
			N = cursor.execute(sql).rowcount
			if N != 0:
				conn.commit()
				r = make_response('episodio %d removida' % id)
				r.status_code = OK
			else:
				r = make_response('Nao existe a episodio %d' % id)
				r.status_code = NOK
		elif data['tipo'] == 'serie':
			sql = 'DELETE FROM episode WHERE id_serie = %d' % id
			N = cursor.execute(sql).rowcount
			if N != 0:
				conn.commit()
				r = make_response('Todas as episodios da serie %d foram removidas' % id)
				r.status_code = OK
			else:
				r = make_response('Nao existe serie com id %d' % id)
				r.status_code = NOK
		elif data['tipo'] == 'episodios':
			sql = 'DELETE FROM episode'
			cursor.execute(sql)
			conn.commit()
			r = make_response('episodios removidas')
			r.status_code = OK

	return r

if __name__ == '__main__':
	GET_LAST_ID_SQL = 'SELECT MAX(id) FROM '
	OK = 200
	CREATED = 201
	NOK = 404

	app.run(debug = True, threaded = True)
