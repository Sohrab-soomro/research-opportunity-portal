"""API regression tests. In-memory mock only; never connects to MySQL."""
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
import mysql.connector
from app import app
import routes.opportunities as routes
from test_database import test_database


class ApiValidation(unittest.TestCase):
    def setUp(self):
        self.context = test_database('mock')
        self.context.__enter__()
        self.addCleanup(self.context.__exit__, None, None, None)
        self.client = app.test_client()
        self.payload = dict(research_title='Network study', research_description='Study TCP.',
                            research_area='CN', faculty_name='Demo Faculty', department='CS',
                            required_skills='Python', available_positions=2,
                            application_deadline='2026-12-20', status='Open')

    def test_invalid_json(self):
        for body in ['{', 'null', '[]', '42', '"text"']:
            for method in ['post', 'put']:
                with self.subTest(body=body, method=method):
                    url='/api/opportunities' + ('/1' if method=='put' else '')
                    self.assertEqual(getattr(self.client,method)(url,data=body,content_type='application/json').status_code,400)

    def test_required_text(self):
        for field in routes.TEXT_FIELDS:
            for value in ['', ' ', None, 5]:
                with self.subTest(field=field,value=value):
                    self.assertEqual(self.client.post('/api/opportunities',json={**self.payload,field:value}).status_code,400)

    def test_positions(self):
        for value in [0,-1,True,1.5,2147483648,'bad',None]:
            with self.subTest(value=value):
                self.assertEqual(self.client.post('/api/opportunities',json={**self.payload,'available_positions':value}).status_code,400)

    def test_dates(self):
        for value in ['2026-02-30','2026-1-1','0999-12-31','invalid',None]:
            with self.subTest(value=value):
                self.assertEqual(self.client.post('/api/opportunities',json={**self.payload,'application_deadline':value}).status_code,400)

    def test_status(self):
        for value in ['Pending','open',None,[]]:
            with self.subTest(value=value):
                self.assertEqual(self.client.post('/api/opportunities',json={**self.payload,'status':value}).status_code,400)

    def test_lengths(self):
        for field,limit in routes.TEXT_LIMITS.items():
            with self.subTest(field=field):
                self.assertEqual(self.client.post('/api/opportunities',json={**self.payload,field:'x'*(limit+1)}).status_code,400)
        self.assertEqual(self.client.post('/api/opportunities',json={**self.payload,'research_description':'é'*40000}).status_code,400)

    def test_roundtrip(self):
        created=self.client.post('/api/opportunities',json=self.payload)
        self.assertEqual(created.status_code,201)
        url='/api/opportunities/'+str(created.json['data']['id'])
        self.assertEqual(self.client.get(url).json['data'],{**self.payload,'id':created.json['data']['id']})
        self.assertEqual(self.client.put(url,json={'available_positions':4}).status_code,200)
        self.assertEqual(self.client.get(url).json['data']['available_positions'],4)
        self.assertEqual(self.client.put(url,json={'status':'Closed'}).status_code,200)
        self.assertEqual(self.client.get(url).json['data']['status'],'Closed')
        for body in [{},{'nonsense':1},{'available_positions':0}]:
            self.assertEqual(self.client.put(url,json=body).status_code,400)
        self.assertEqual(self.client.delete(url).status_code,200)
        self.assertEqual(self.client.get(url).status_code,404)
        self.assertEqual(self.client.delete(url).status_code,404)
        self.assertEqual(self.client.put(url,json={'status':'Closed'}).status_code,404)

    def test_database_failure_is_sanitized(self):
        with patch.object(routes,'get_connection',side_effect=mysql.connector.Error('PRIVATE_CONNECTION_DETAIL')):
            with redirect_stdout(StringIO()) as output:
                response=self.client.get('/api/opportunities')
            self.assertEqual(response.status_code,500)
            self.assertNotIn('PRIVATE_CONNECTION_DETAIL',response.get_data(as_text=True)+output.getvalue())

    def test_frontend_assets_and_errors(self):
        for path in ['/','/script.js','/style.css']:
            with self.client.get(path) as response:
                self.assertEqual(response.status_code,200)
        self.assertEqual(self.client.patch('/api/opportunities').status_code,405)
        self.assertEqual(self.client.get('/not-found').status_code,404)


if __name__=='__main__':
    unittest.main()
