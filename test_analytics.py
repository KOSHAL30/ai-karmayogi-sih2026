
import requests

def test():
    # Login as seeded user to get token
    res = requests.post('http://127.0.0.1:8000/api/v1/auth/login', json={
        'email': 'rajesh.kumar@gov.in',
        'password': 'Karmayogi2026!'
    })
    
    if res.status_code != 200:
        print('Login failed!', res.status_code, res.text)
        return
        
    token = res.json()['data']['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Check admin dashboard KPIs
    res = requests.get('http://127.0.0.1:8000/api/v1/admin/dashboard', headers=headers)
    if res.status_code != 200:
        print('Admin dashboard failed', res.status_code)
    else:
        kpis = res.json()['data']['kpis']
        print('KPIs:', {k: v['value'] for k, v in kpis.items()})

    # Check certificates
    res = requests.get('http://127.0.0.1:8000/api/v1/certificates', headers=headers)
    if res.status_code != 200:
        print('Certificates failed', res.status_code)
    else:
        certs = res.json()['data']
        print('Certificates count:', len(certs))

    # Check notifications
    res = requests.get('http://127.0.0.1:8000/api/v1/notifications', headers=headers)
    if res.status_code != 200:
        print('Notifications failed', res.status_code)
    else:
        notifs = res.json()['data']
        print('Notifications count:', notifs['total_notifications'])

test()

