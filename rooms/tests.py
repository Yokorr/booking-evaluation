import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rooms.models import Room
from rooms.serializers import RoomSerializer
from rooms.reports import export_city_summary

class SerializerEvaluationTests(TestCase):
    def test_serializer_fields(self):
        room = Room.objects.select_related('location').get(code='lyo-desk')
        self.assertEqual(dict(RoomSerializer(room).data), {
            'code': 'lyo-desk', 'name': 'Open desk', 'capacity': 4, 'location_city': 'Lyon',
        })

    def test_serializer_many(self):
        data = RoomSerializer(Room.objects.select_related('location').order_by('code'), many=True).data
        self.assertEqual(len(data), 5)
        self.assertTrue(all(set(item) == {'code','name','capacity','location_city'} for item in data))

    def test_read_only_fields(self):
        serializer = RoomSerializer(data={'code':'x','name':'X','capacity':20,'location_city':'Paris'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data, {})

class ApiEvaluationTests(TestCase):
    def test_list_all_sorted(self):
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([r['code'] for r in response.json()], [
            'lyo-desk','lyo-room','nan-room','par-desk','par-room'
        ])

    def test_city_filter_case_insensitive_trimmed(self):
        response = self.client.get('/api/rooms/', {'city':'  lYoN  '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([r['code'] for r in response.json()], ['lyo-desk','lyo-room'])

    def test_city_no_match_empty_list(self):
        response = self.client.get('/api/rooms/', {'city':'Rennes'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_blank_city_400(self):
        response = self.client.get('/api/rooms/', {'city':'    '})
        self.assertEqual(response.status_code, 400)

    def test_endpoint_read_only(self):
        response = self.client.post('/api/rooms/', data={}, content_type='application/json')
        self.assertEqual(response.status_code, 405)

class ReportEvaluationTests(TestCase):
    def test_lyon_summary(self):
        result = export_city_summary('Lyon')
        self.assertIsInstance(result, str)
        self.assertEqual(json.loads(result), {
            'city':'Lyon', 'total_rooms':2, 'total_capacity':10,
            'room_codes':['lyo-desk','lyo-room'],
        })

    def test_city_is_normalized_from_database(self):
        result = json.loads(export_city_summary('  lyon  '))
        self.assertEqual(result['city'], 'Lyon')
        self.assertEqual(result['total_capacity'], 10)

    def test_unknown_city_empty_report(self):
        result = json.loads(export_city_summary('Rennes'))
        self.assertEqual(result, {
            'city':'Rennes', 'total_rooms':0, 'total_capacity':0, 'room_codes':[],
        })

    def test_invalid_city_rejected(self):
        for bad in ['', '   ', None, 13]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                export_city_summary(bad)

    def test_report_is_read_only(self):
        before = Room.objects.count()
        export_city_summary('Paris')
        self.assertEqual(Room.objects.count(), before)


class TemplateEvaluationTests(TestCase):
    """M4 DTL: output must depend on context and escape user-supplied names."""

    def test_catalogue_renders_database_rooms(self):
        response = self.client.get('/rooms/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lyo-desk')
        self.assertContains(response, 'Open desk')
        self.assertContains(response, 'Lyon')
        self.assertContains(response, '4 seats')

    def test_empty_state_uses_template_empty_tag(self):
        from django.template.loader import render_to_string
        content = render_to_string('rooms/catalogue.html', {'rooms': []})
        self.assertIn('No rooms available.', content)

    def test_template_autoescapes_room_names(self):
        from rooms.models import Location
        location = Location.objects.get(code='lyo')
        Room.objects.create(code='lyo-html', name='<script>alert(1)</script>', capacity=1, location=location)
        response = self.client.get('/rooms/')
        self.assertNotIn('<script>alert(1)</script>', response.content.decode())
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')
